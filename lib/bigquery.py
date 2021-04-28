from functools import lru_cache

from django.conf import settings
from google.cloud import bigquery


@lru_cache
def bigquery_client():
    return bigquery.Client(project=settings.GCP_PROJECT)
