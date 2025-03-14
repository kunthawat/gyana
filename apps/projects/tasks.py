import json
import re
from graphlib import CycleError, TopologicalSorter
from uuid import uuid4

from celery import shared_task
from celery_progress import backend
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.integrations.models import Integration
from apps.integrations.tasks import run_integration_task
from apps.nodes.models import Node
from apps.projects.emails import send_duplicate_email
from apps.runs.models import GraphRun, JobRun
from apps.tables.models import Table
from apps.users.models import CustomUser
from apps.workflows import tasks as workflow_tasks
from apps.workflows.models import Workflow

from .models import Project


def _update_progress_from_job_run(progress_recorder, run_info, job_run):
    if progress_recorder:
        run_info[job_run.source_obj.entity_id] = job_run.state
        progress_recorder.set_progress(0, 0, description=json.dumps(run_info))


def _get_entity_from_input_table(table: Table):
    if table.source == Table.Source.WORKFLOW_NODE:
        return table.workflow_node.workflow
    else:
        return table.integration


@shared_task(bind=True)
def run_project_task(self, graph_run_id: int, scheduled_only=False):

    # ignore progress recorder when used as a function
    progress_recorder = backend.ProgressRecorder(self) if self.request.id else None

    graph_run = GraphRun.objects.get(pk=graph_run_id)
    project = graph_run.project

    # Run all the workflows and sheets in a project. The python graphlib library will build
    # a topological sort for any graph of hashables and raises a cycle error if
    # there is a circularity.

    # one query per workflow, in future we would optimize into a single query
    graph = {
        workflow: [
            _get_entity_from_input_table(node.input_table)
            for node in workflow.nodes.filter(
                kind=Node.Kind.INPUT,
            )
            .filter(
                Q(input_table__integration__kind__in=Integration.KIND_RUN_IN_PROJECT)
                | Q(input_table__source=Table.Source.WORKFLOW_NODE)
            )
            .select_related("input_table__workflow_node__workflow")
            .select_related("input_table__integration")
            .all()
        ]
        for workflow in project.workflow_set.all()
    }

    graph.update(
        {
            integration: []
            for integration in project.integration_set.filter(
                kind__in=Integration.KIND_RUN_IN_PROJECT
            ).all()
        }
    )

    if scheduled_only:
        graph = {
            entity: [parent for parent in parents if parent.is_scheduled]
            for entity, parents in graph.items()
            if entity.is_scheduled
        }

    job_runs = {
        entity: JobRun.objects.create(
            source=JobRun.Source.INTEGRATION
            if isinstance(entity, Integration)
            else JobRun.Source.WORKFLOW,
            integration=entity if isinstance(entity, Integration) else None,
            workflow=entity if isinstance(entity, Workflow) else None,
            user=graph_run.user,
            graph_run=graph_run,
        )
        for entity in graph
    }

    run_info = {
        job_run.source_obj.entity_id: job_run.state for job_run in job_runs.values()
    }
    if progress_recorder:
        progress_recorder.set_progress(0, 0, description=json.dumps(run_info))

    ts = TopologicalSorter(graph)

    try:
        for entity in ts.static_order():

            job_run = job_runs[entity]
            job_run.state = JobRun.State.RUNNING
            job_run.started_at = timezone.now()
            _update_progress_from_job_run(progress_recorder, run_info, job_run)
            job_run.save()

            try:
                if isinstance(entity, Integration):
                    run_integration_task(entity.kind, job_run.id)
                elif isinstance(entity, Workflow):
                    workflow_tasks.run_workflow_task(job_run.id)
                job_run.state = JobRun.State.SUCCESS

            except Exception:
                job_run.state = JobRun.State.FAILED

            finally:
                _update_progress_from_job_run(progress_recorder, run_info, job_run)
                job_run.completed_at = timezone.now()
                job_run.save()

    except CycleError:
        Exception("Your integrations and workflows have a circular dependency")

    if graph_run.runs.filter(state=JobRun.State.FAILED).exists():
        raise Exception(
            "Not all of your integrations or workflows completed successfully"
        )


def run_project(project: Project, user: CustomUser):
    graph_run = GraphRun.objects.create(
        project=project,
        task_id=uuid4(),
        state=GraphRun.State.RUNNING,
        started_at=timezone.now(),
        user=user,
    )
    run_project_task.apply_async((graph_run.id,), task_id=str(graph_run.task_id))
    return graph_run


@shared_task
def duplicate_project(project_id, user_id):
    from apps.nodes.models import Node
    from apps.tables.models import Table
    from apps.widgets.models import Widget

    user = CustomUser.objects.get(pk=user_id)
    project = Project.objects.get(pk=project_id)

    with transaction.atomic():
        new_project_name = f"Copy of {project.name}"
        name_regex = f"{new_project_name} ([0-9]+)"
        team_project_names = [
            int(match.group(1)) if (match := re.search(name_regex, p.name)) else 1
            for p in project.team.project_set.filter(
                name__startswith=new_project_name
            ).all()
        ]

        if team_project_names:
            new_project_name += f" {max(team_project_names)+1}"

        clone = project.make_clone({"name": new_project_name})

        # Replace the table dependencies of input_nodes
        tables = Table.objects.filter(project=clone).all()
        input_nodes = Node.objects.filter(
            workflow__project=clone,
            kind=Node.Kind.INPUT,
            input_table__isnull=False,
        ).all()

        for node in input_nodes:
            node.input_table = next(
                filter(lambda t: t.copied_from == node.input_table.id, tables)
            )
        Node.objects.bulk_update(input_nodes, ["input_table"])

        # Replace the widget dependencies
        widgets = Widget.objects.filter(
            page__dashboard__project=clone, table__isnull=False
        ).all()
        for widget in widgets:
            widget.table = next(
                filter(lambda t: t.copied_from == widget.table.id, tables)
            )
        Widget.objects.bulk_update(widgets, ["table"])

    send_duplicate_email(user, clone)
