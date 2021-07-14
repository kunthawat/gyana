import datetime
import os
import time
import uuid

import analytics
import coreapi
from apps.projects.mixins import ProjectMixin
from apps.tables.models import Table
from apps.utils.segment_analytics import (INTEGRATION_CREATED_EVENT,
                                          NEW_INTEGRATION_START_EVENT)
from apps.utils.table_data import get_table
from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
from django_tables2.views import SingleTableMixin
from lib.bigquery import query_table
from lib.clients import DATASET_ID, get_bucket
from rest_framework.decorators import api_view, schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from turbo_response.stream import TurboStream
from turbo_response.views import TurboCreateView, TurboUpdateView

from .bigquery import query_integration
from .fivetran import FivetranClient
from .forms import (FORM_CLASS_MAP, CSVCreateForm, FivetranForm,
                    GoogleSheetsForm, IntegrationForm)
from .models import Integration
from .tables import IntegrationTable, StructureTable
from .tasks import (poll_fivetran_historical_sync,
                    start_fivetran_integration_task,
                    update_integration_fivetran_schema)
from .utils import get_service_categories, get_services

# CRUDL


class IntegrationList(ProjectMixin, SingleTableView):
    template_name = "integrations/list.html"
    model = Integration
    table_class = IntegrationTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["integration_count"] = Integration.objects.filter(
            project=self.project
        ).count()

        context_data["integration_kinds"] = Integration.Kind.choices

        return context_data

    def get_queryset(self) -> QuerySet:
        queryset = Integration.objects.filter(project=self.project)
        # Add search query if it exists
        if query := self.request.GET.get("q"):
            queryset = (
                queryset.annotate(
                    similarity=TrigramSimilarity("name", query),
                )
                .filter(similarity__gt=0.05)
                .order_by("-similarity")
            )
        if (kind := self.request.GET.get("kind")) and kind in Integration.Kind.values:
            queryset = queryset.filter(kind=kind)

        return queryset.prefetch_related("table_set").all()


class IntegrationUpload(ProjectMixin, TurboCreateView):
    template_name = "integrations/upload.html"
    model = Integration

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["integration_kind"] = Integration.Kind.CSV

        return context_data

    def get_initial(self):
        initial = super().get_initial()
        initial["kind"] = Integration.Kind.CSV
        initial["project"] = self.project

        return initial

    def get_form_class(self):
        analytics.track(
            self.request.user.id,
            NEW_INTEGRATION_START_EVENT,
            {"type": Integration.Kind.CSV},
        )

        return CSVCreateForm

    def form_valid(self, form):
        instance_session_key = uuid.uuid4().hex

        if not form.is_valid():
            return HttpResponseBadRequest()

        self.request.session[instance_session_key] = {
            **form.cleaned_data,
            "project": form.cleaned_data["project"].id,
        }

        analytics.track(
            self.request.user.id,
            INTEGRATION_CREATED_EVENT,
            {
                "id": form.instance.id,
                "type": form.instance.kind,
                "name": form.instance.name,
            },
        )

        return (
            TurboStream("create-container")
            .append.template(
                "integrations/_create_flow.html",
                {
                    "instance_session_key": instance_session_key,
                    "file_input_id": "id_file",
                    "stage": "upload",
                },
            )
            .response(self.request)
        )

    def get_success_url(self) -> str:
        return reverse(
            "project_integrations:detail", args=(self.project.id, self.object.id)
        )


class IntegrationNew(ProjectMixin, TemplateView):
    template_name = "integrations/new.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["integration_kind"] = Integration.Kind
        context_data["services"] = get_services()
        context_data["service_categories"] = get_service_categories()

        return context_data


class IntegrationCreate(ProjectMixin, TurboCreateView):
    template_name = "integrations/create.html"
    model = Integration

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["integration_kind"] = Integration.Kind
        context_data["services"] = get_services()
        context_data["service_categories"] = get_service_categories()

        return context_data

    def get_initial(self):
        initial = super().get_initial()
        initial["kind"] = self.request.GET.get("kind")
        initial["service"] = self.request.GET.get("service")
        initial["project"] = self.project

        return initial

    def get_form_class(self):
        if (kind := self.request.GET.get("kind")) is not None:
            analytics.track(
                self.request.user.id, NEW_INTEGRATION_START_EVENT, {"type": kind}
            )

            if kind == Integration.Kind.GOOGLE_SHEETS:
                return GoogleSheetsForm
            elif kind == Integration.Kind.FIVETRAN:
                return FivetranForm

        return GoogleSheetsForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        analytics.track(
            self.request.user.id,
            INTEGRATION_CREATED_EVENT,
            {
                "id": form.instance.id,
                "type": form.instance.kind,
                "name": form.instance.name,
            },
        )

        if form.instance.kind == Integration.Kind.FIVETRAN:
            client = FivetranClient(form.instance)
            client.create()
            internal_redirect = reverse(
                "integrations:authorize-fivetran-redirect", args=(form.instance.id,)
            )
            redirect = client.authorize(f"{settings.EXTERNAL_URL}{internal_redirect}")
            return redirect

        if form.instance.kind == Integration.Kind.GOOGLE_SHEETS:
            form.instance.start_sync()

        return response

    def get_success_url(self) -> str:
        return reverse(
            "project_integrations:detail", args=(self.project.id, self.object.id)
        )


class IntegrationDetail(ProjectMixin, TurboUpdateView):
    template_name = "integrations/detail.html"
    model = Integration
    form_class = IntegrationForm

    def get_context_data(self, **kwargs):
        from .tables import UsedInTable

        context = super().get_context_data(**kwargs)
        context["table"] = UsedInTable(self.object.used_in)

        return context

    def get_success_url(self) -> str:
        return reverse(
            "project_integrations:detail", args=(self.project.id, self.object.id)
        )


class IntegrationUpdate(ProjectMixin, TurboUpdateView):
    template_name = "integrations/update.html"
    model = Integration

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["integration_kind"] = Integration.Kind
        context_data["service_account"] = settings.GCP_BQ_SVC_ACCOUNT

        return context_data

    def get_form_class(self):
        return FORM_CLASS_MAP[self.object.kind]

    def get_success_url(self) -> str:
        return reverse(
            "project_integrations:settings", args=(self.project.id, self.object.id)
        )


class IntegrationDelete(ProjectMixin, DeleteView):
    template_name = "integrations/delete.html"
    model = Integration

    def get_success_url(self) -> str:
        return reverse("project_integrations:list", args=(self.project.id,))


class IntegrationStructure(ProjectMixin, DetailView):
    template_name = "integrations/structure.html"
    model = Integration
    table_class = StructureTable

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["tables"] = []

        for table in self.object.table_set.all():
            table_data = [
                {"type": str(field_type), "name": field_name}
                for field_name, field_type in table.schema.items()
            ]
            context_data["tables"].append(
                {"title": table.bq_table, "table_struct": StructureTable(table_data)}
            )

        return context_data


class IntegrationData(ProjectMixin, DetailView):
    template_name = "integrations/data.html"
    model = Integration

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["tables"] = self.object.table_set.all()

        return context_data


class IntegrationSchema(ProjectMixin, DetailView):
    template_name = "integrations/schema.html"
    model = Integration

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["integration"] = self.get_object()
        context_data["schemas"] = FivetranClient(
            context_data["integration"]
        ).get_schema()

        return context_data

    def post(self, request, *args, **kwargs):
        integration = self.get_object()
        client = FivetranClient(integration)
        client.update_schema(
            [key for key in request.POST.keys() if key != "csrfmiddlewaretoken"]
        )

        return TurboStream(f"{integration.id}-schema-update-message").replace.response(
            f"""<p id="{ integration.id }-schema-update-message" class="ml-4 text-green">Successfully updated the schema</p>""",
            is_safe=True,
        )


class IntegrationSetup(ProjectMixin, DetailView):
    template_name = "integrations/setup.html"
    model = Integration

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["integration"] = self.get_object()
        context_data["service"] = get_services()[self.get_object().service]
        context_data["schemas"] = FivetranClient(
            context_data["integration"]
        ).get_schema()

        return context_data

    def post(self, request, *args, **kwargs):
        integration = self.get_object()

        task_id = update_integration_fivetran_schema.delay(
            self.kwargs.get(self.pk_url_kwarg),
            [key for key in request.POST.keys() if key != "csrfmiddlewaretoken"],
        )

        return (
            TurboStream("integration-setup-container")
            .replace.template(
                "integrations/fivetran_setup/_flow.html",
                {
                    "table_select_task_id": task_id,
                    "turbo_url": reverse(
                        "integrations:start-fivetran-integration",
                        args=(integration.id,),
                    ),
                },
            )
            .response(request)
        )


class IntegrationSettings(ProjectMixin, TurboUpdateView):
    template_name = "integrations/settings.html"
    model = Integration

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["integration_kind"] = Integration.Kind
        context_data["service_account"] = settings.GCP_BQ_SVC_ACCOUNT

        return context_data

    def get_form_class(self):
        return FORM_CLASS_MAP[self.object.kind]

    def get_success_url(self) -> str:
        return reverse(
            "project_integrations:settings", args=(self.project.id, self.object.id)
        )


# Turbo frames


class IntegrationGrid(SingleTableMixin, TemplateView):
    template_name = "integrations/grid.html"
    paginate_by = 15

    def get_table_kwargs(self):
        return {"attrs": {"class": "table-data"}}

    def get_context_data(self, **kwargs):
        self.integration = Integration.objects.get(id=kwargs["pk"])

        table_id = self.request.GET.get("table_id")
        try:
            self.table_instance = (
                self.integration.table_set.get(pk=table_id)
                if table_id
                else self.integration.table_set.first()
            )
        except (Table.DoesNotExist, ValueError):
            self.table_instance = self.integration.table_set.first()

        context_data = super().get_context_data(**kwargs)
        context_data["table_instance"] = self.table_instance
        return context_data

    def get_table(self, **kwargs):
        query = query_table(
            self.table_instance.bq_table,
            self.integration.schema
            if self.integration.kind == Integration.Kind.FIVETRAN
            else DATASET_ID,
        )
        table = get_table(query.schema(), query, **kwargs)

        return RequestConfig(
            self.request, paginate=self.get_table_pagination(table)
        ).configure(table)


class IntegrationSync(TurboUpdateView):
    template_name = "integrations/sync.html"
    model = Integration
    fields = []

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data[
            "external_table_sync_task_id"
        ] = self.object.external_table_sync_task_id

        return context_data

    def form_valid(self, form):
        self.object.start_sync()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("integrations:sync", args=(self.object.id,))


# Turbo frames


class IntegrationAuthorize(DetailView):

    model = Integration
    template_name = "integrations/authorize.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        integration = context["integration"]

        if integration.fivetran_id is None:
            FivetranClient(integration).create()

        return context


# Endpoints


@api_view(["POST"])
@schema(
    AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="filename",
                required=True,
                location="form",
            ),
        ]
    )
)
def generate_signed_url(request: Request, session_key: str):
    filename = request.data["filename"]
    filename, file_extension = os.path.splitext(filename)
    path = f"{settings.CLOUD_NAMESPACE}/integrations/{filename}-{slugify(time.time())}{file_extension}"

    blob = get_bucket().blob(path)
    # This signed URL allows the client to create a Session URI to use as upload pointer.
    # Delegating this to the client, because geographic location matters when starting a session
    # https://cloud.google.com/storage/docs/access-control/signed-urls#signing-resumable
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="RESUMABLE",
    )

    request.session[session_key] = {**request.session[session_key], "file": path}

    return Response({"url": url})


@api_view(["POST"])
def start_sync(request: Request, session_key: str):
    form_data = request.session[session_key]

    integration = CSVCreateForm(data=form_data).save()
    integration.file = form_data["file"]
    integration.created_by = request.user
    integration.save()
    integration.start_sync()

    return (
        TurboStream("integration-validate-flow")
        .replace.template(
            "integrations/_create_flow.html",
            {
                "instance_session_key": session_key,
                "file_input_id": "id_file",
                "stage": "validate",
                "external_table_sync_task_id": integration.external_table_sync_task_id,
                "redirect_url": reverse(
                    "project_integrations:detail",
                    args=(integration.project.id, integration.id),
                ),
            },
        )
        .response(request)
    )


@api_view(["GET"])
def start_fivetran_integration(request: HttpRequest, pk: int):
    integration = get_object_or_404(Integration, pk=pk)

    task_id = start_fivetran_integration_task.delay(pk)

    return (
        TurboStream("integration-setup-container")
        .replace.template(
            "integrations/fivetran_setup/_flow.html",
            {
                "connector_start_task_id": task_id,
                "redirect_url": reverse(
                    "project_integrations:detail",
                    args=(integration.project.id, integration.id),
                ),
            },
        )
        .response(request)
    )


def authorize_fivetran(request: HttpRequest, pk: int):

    integration = get_object_or_404(Integration, pk=pk)
    uri = reverse("integrations:authorize-fivetran-redirect", args=(pk,))
    redirect_uri = (
        f"{settings.EXTERNAL_URL}{uri}?original_uri={request.GET.get('original_uri')}"
    )

    return FivetranClient(integration).authorize(redirect_uri)


def authorize_fivetran_redirect(request: HttpRequest, pk: int):

    integration = get_object_or_404(Integration, pk=pk)
    integration.fivetran_authorized = True

    result = poll_fivetran_historical_sync.delay(integration.id)
    integration.fivetran_poll_historical_sync_task_id = result.task_id

    integration.save()

    return redirect(
        reverse(
            "project_integrations:setup", args=(integration.project.id, integration.id)
        )
    )
