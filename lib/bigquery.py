from datetime import datetime

from apps.datasets.models import Dataset
from apps.filters.models import Filter
from apps.widgets.models import Widget, WidgetSource
from django.conf import settings
from google.cloud import bigquery

from lib.clients import DATASET_ID, bigquery_client, ibis_client

DEFAULT_LIMIT = 10


def sync_table(dataset: Dataset):

    client = bigquery_client()

    external_config = create_external_config(dataset)
    job_config = bigquery.QueryJobConfig(
        table_definitions={dataset.external_table_id: external_config}
    )

    client.query(
        f"CREATE OR REPLACE TABLE {DATASET_ID}.{dataset.table_id} AS SELECT * FROM {DATASET_ID}.{dataset.external_table_id}",
        job_config=job_config,
    ).result()

    if not dataset.has_initial_sync:
        dataset.has_initial_sync = True
    dataset.last_synced = datetime.now()
    dataset.save()


def create_external_config(dataset: Dataset):
    if dataset.kind == Dataset.Kind.GOOGLE_SHEETS:
        # https://cloud.google.com/bigquery/external-data-drive#python
        external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
        external_config.source_uris = [dataset.url]
    elif dataset.kind == Dataset.Kind.CSV:
        external_config = bigquery.ExternalConfig("CSV")
        external_config.source_uris = [
            f"gs://{settings.GS_BUCKET_NAME}/{dataset.file.name}"
        ]

    external_config.autodetect = True

    return external_config


def create_external_table(dataset: Dataset):

    client = bigquery_client()

    bq_dataset = client.get_dataset(DATASET_ID)

    external_table = bigquery.Table(bq_dataset.table(dataset.external_table_id))

    external_config = create_external_config(dataset)

    external_table.external_data_configuration = external_config
    external_table = client.create_table(external_table, exists_ok=True)


def query_dataset(dataset: Dataset):

    if not dataset.has_initial_sync:
        create_external_table(dataset)
        sync_table(dataset)

    conn = ibis_client()
    table = conn.table(dataset.table_id)

    return conn.execute(table.limit(DEFAULT_LIMIT))


def query_widget(widget: Widget):

    conn = ibis_client()

    source = widget.dataset or widget.node
    table = source.get_query()

    for filter in widget.filter_set.all():
        if filter.type == Filter.Type.INTEGER:
            if filter.integer_predicate == Filter.IntegerPredicate.EQUAL:
                table = table[table[filter.column] == filter.integer_value]
            elif filter.integer_predicate == Filter.IntegerPredicate.EQUAL:
                table = table[table[filter.column] != filter.integer_value]
        elif filter.type == Filter.Type.STRING:
            if filter.string_predicate == Filter.StringPredicate.STARTSWITH:
                table = table[table[filter.column].str.startswith(filter.string_value)]
            elif filter.string_predicate == Filter.StringPredicate.ENDSWITH:
                table = table[table[filter.column].str.endswith(filter.string_value)]

    return conn.execute(table.group_by(widget.label).count(widget.value))


def get_columns(source: WidgetSource):
    return source.get_schema()
