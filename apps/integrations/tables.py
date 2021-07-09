from apps.utils.table import NaturalDatetimeColumn
from django_tables2 import Column, Table

from .models import Integration


class IntegrationTable(Table):
    class Meta:
        model = Integration
        fields = (
            "name",
            "kind",
            "num_rows",
            "last_synced",
            "created",
            "updated",
        )
        attrs = {"class": "table"}

    name = Column(linkify=True)
    kind = Column(accessor="display_kind")
    last_synced = NaturalDatetimeColumn()
    created = NaturalDatetimeColumn()
    updated = NaturalDatetimeColumn()


class StructureTable(Table):
    class Meta:
        fields = ("name", "type")
        attrs = {"class": "table-data"}

    type = Column()
    name = Column()


class UsedInTable(Table):
    class Meta:
        model = Integration
        attrs = {"class": "table"}
        fields = (
            "name",
            "kind",
            "created",
            "updated",
        )

    name = Column(linkify=True)
