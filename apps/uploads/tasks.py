import analytics
from apps.base.analytics import INTEGRATION_SYNC_SUCCESS_EVENT
from apps.base.time import catchtime
from apps.integrations.emails import (
    integration_ready_email,
    send_integration_ready_email,
)
from apps.integrations.models import Integration
from apps.tables.models import Table
from apps.uploads.bigquery import import_table_from_upload
from celery import shared_task
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Upload


@shared_task(bind=True)
def run_upload_sync_task(self, upload_id: int):

    upload = get_object_or_404(Upload, pk=upload_id)
    integration = upload.integration

    # we need to save the table instance to get the PK from database, this ensures
    # database will rollback automatically if there is an error with the bigquery
    # table creation, avoids orphaned table entities

    try:

        with transaction.atomic():

            table, created = Table.objects.get_or_create(
                integration=integration,
                source=Table.Source.INTEGRATION,
                bq_table=upload.table_id,
                bq_dataset=integration.project.team.tables_dataset_id,
                project=integration.project,
            )

            with catchtime() as get_time_to_sync:
                import_table_from_upload(table=table, upload=upload)

            table.sync_updates_from_bigquery()

            upload.last_synced = timezone.now()
            upload.save()

            integration.state = Integration.State.DONE
            integration.save()

    except Exception as e:
        integration.state = Integration.State.ERROR
        integration.save()
        raise e

    if created:
        send_integration_ready_email(integration, get_time_to_sync())

    return integration.id


def run_upload_sync(upload: Upload):

    upload.integration.state = Integration.State.LOAD
    upload.integration.save()

    result = run_upload_sync_task.delay(upload.id)
    upload.sync_task_id = result.task_id
    upload.sync_started = timezone.now()
    upload.save()
