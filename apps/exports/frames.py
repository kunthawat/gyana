from django.http import FileResponse
from django.urls.base import reverse
from django.utils.functional import cached_property
from django.views.generic import DetailView

from apps.base.views import CreateView
from apps.exports.tasks import run_export_task
from apps.nodes.models import Node
from apps.tables.models import Table

from .models import Export


class ExportCreate(CreateView):
    template_name = "exports/create.html"
    model = Export
    fields = []

    def form_valid(self, form):
        export = form.instance
        self.save_parent(export)
        run_export_task.delay(export.id, self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_id"] = self.parent.id
        context["target_url"] = self.success_url

        # Get context should only be called when triggered after the click
        context["show_alert"] = True
        return context

    def get_success_url(self) -> str:
        return reverse(
            self.success_url,
            args=(self.parent.id,),
        )


class ExportCreateNode(ExportCreate):
    success_url = "exports:create_node"

    @cached_property
    def parent(self):
        return Node.objects.get(pk=self.kwargs["parent_id"])

    def save_parent(self, export):
        export.node = self.parent
        export.save()


class ExportCreateIntegrationTable(ExportCreate):
    success_url = "exports:create_integration_table"

    @cached_property
    def parent(self):
        return Table.objects.get(pk=self.kwargs["parent_id"])

    def save_parent(self, export):
        export.integration_table = self.parent
        export.save()


class ExportDownload(DetailView):
    model = Export

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        res = FileResponse(object.file)
        res["Content-Type"] = "application/octet-stream"
        res["Content-Disposition"] = f'attachment; filename="{object.file.name}"'
        return res
