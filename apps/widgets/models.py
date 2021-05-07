from typing import Union

from apps.dashboards.models import Dashboard
from apps.dataflows.models import Node
from apps.datasets.models import Dataset
from django.db import models

WidgetSource = Union[Node, Dataset, None]


class Widget(models.Model):
    class Kind(models.TextChoices):
        # using fusioncharts name for database
        COLUMN = "column2d", "Column"
        LINE = "line", "Line"
        PIE = "pie2d", "Pie"

    name = models.CharField(max_length=255)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    # A widget can point to either a dataset or node
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True)
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)

    kind = models.CharField(max_length=32, choices=Kind.choices)
    # maximum length of bigquery column name
    label = models.CharField(max_length=300, null=True, blank=True)
    value = models.CharField(max_length=300, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    @property
    def source(self) -> WidgetSource:
        return self.dataset or self.node

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name
