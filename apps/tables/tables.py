from apps.utils.table import NaturalDatetimeColumn
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_tables2 import Column
from django_tables2 import Table as DjangoTable

from .models import Table


class TableTable(DjangoTable):
    class Meta:
        model = Table
        fields = (
            "bq_table",
            "num_rows",
            "created",
            "updated",
        )
        attrs = {"class": "table"}

    bq_table = Column(verbose_name="Name")
    created = NaturalDatetimeColumn()
    updated = NaturalDatetimeColumn()
    delete = Column(verbose_name="", empty_values=(), orderable=False)

    def render_delete(self, value, record):
        text = "Delete this integration table"
        template = loader.get_template("tables/_delete.html")
        return template.render(
            {"object": record, "integration": record.integration}, self.request
        )

        return render(
            None,
            "tables/_delete.html",
        )

        mark_safe(
            delete_html.format(
                href=reverse(
                    "project_tables:delete",
                    args=(
                        record.project.id,
                        record.id,
                    ),
                ),
                text=text,
            )
        )
