from apps.projects.mixins import ProjectMixin
from django.urls.base import reverse
from django.views.generic.edit import DeleteView
from django_tables2.views import SingleTableView

from .models import Table
from .tables import TableTable


class TableList(ProjectMixin, SingleTableView):
    template_name = "integrations/fivetran_tables/list.html"
    model = Table
    table_class = TableTable
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        return context_data

    def get_queryset(self):
        queryset = Table.objects.filter(project=self.project)

        return queryset


class TableDelete(ProjectMixin, DeleteView):
    template_name = "integrations/fivetran_tables/list.html"
    model = Table

    def get_success_url(self) -> str:
        if self.request.GET.get("on-integration"):
            return reverse(
                "project_integrations:tables",
                args=(self.project.id, self.get_object().integration.id),
            )

        return reverse(
            "project_tables:list",
            args=(self.project.id,),
        )
