from apps.dataflows.nodes import NODE_FROM_CONFIG
from apps.projects.models import Project
from apps.tables.models import Table
from django.conf import settings
from django.db import models


class Dataflow(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    last_run = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name


class Node(models.Model):
    class Kind(models.TextChoices):
        INPUT = "input", "Input"
        OUTPUT = "output", "Output"
        SELECT = "select", "Select"
        JOIN = "join", "Join"
        GROUP = "group", "Group"

    dataflow = models.ForeignKey(Dataflow, on_delete=models.CASCADE)
    kind = models.CharField(max_length=16, choices=Kind.choices)
    x = models.FloatField()
    y = models.FloatField()
    parents = models.ManyToManyField(
        "self", symmetrical=False, related_name="children", blank=True
    )

    # ======== Node specific columns ========= #

    # Input
    input_table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)

    # Output
    output_name = models.CharField(max_length=100, null=True)

    # Select
    # columns exists on Column as FK

    # Join
    join_how = models.CharField(
        max_length=12,
        choices=[
            ("inner", "Inner"),
            ("outer", "Outer"),
            ("left", "Left"),
            ("right", "Right"),
        ],
        default="inner",
    )
    join_left = models.CharField(
        max_length=settings.BIGQUERY_COLUMN_NAME_LENGTH, null=True, blank=True
    )
    join_right = models.CharField(
        max_length=settings.BIGQUERY_COLUMN_NAME_LENGTH, null=True, blank=True
    )

    def get_query(self):
        func = NODE_FROM_CONFIG[self.kind]
        return func(self)

    def get_schema(self):
        return self.get_query().schema()

    def get_table_name(self):
        return f"Dataflow:{self.dataflow.name}:{self.output_name}"


class Column(models.Model):
    name = models.CharField(max_length=settings.BIGQUERY_COLUMN_NAME_LENGTH)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="columns")


class FunctionColumn(models.Model):
    class Functions(models.TextChoices):
        SUM = "sum", "Sum"
        COUNT = "count", "Count"

    name = models.CharField(max_length=settings.BIGQUERY_COLUMN_NAME_LENGTH)
    function = models.CharField(max_length=20, choices=Functions.choices)
    node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="aggregations"
    )
