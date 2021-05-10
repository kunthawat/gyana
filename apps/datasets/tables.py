import django_tables2 as tables
from apps.utils.table import NaturalDatetimeColumn

from .models import Dataset


class DatasetTable(tables.Table):
    class Meta:
        model = Dataset
        fields = ("name", "kind", "last_synced", "created", "updated")

    name = tables.Column(linkify=True)
    last_synced = NaturalDatetimeColumn()
    created = NaturalDatetimeColumn()
    updated = NaturalDatetimeColumn()
