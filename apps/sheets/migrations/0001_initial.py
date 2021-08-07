# Generated by Django 3.2.5 on 2021-08-06 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("integrations", "0011_auto_20210721_1256"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sheet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "integration",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="integrations.integration",
                    ),
                ),
                ("url", models.URLField()),
                ("cell_range", models.CharField(blank=True, max_length=64, null=True)),
                ("external_table_sync_task_id", models.UUIDField(null=True)),
                ("has_initial_sync", models.BooleanField(default=False)),
                ("last_synced", models.DateTimeField(null=True)),
            ],
            options={
                "ordering": ("-created",),
                "abstract": False,
            },
        ),
        migrations.RunSQL(
            """
        INSERT INTO sheets_sheet
            (integration_id, url, cell_range, external_table_sync_task_id, has_initial_sync, last_synced, created, updated)
        SELECT id, url, cell_range, external_table_sync_task_id, has_initial_sync, last_synced, created, updated
        FROM integrations_integration
        where kind = 'google_sheets'
        ;
        """
        ),
    ]
