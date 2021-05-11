from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from google.cloud.exceptions import NotFound
from lib.clients import bigquery_client


class Command(BaseCommand):
    help = "Creates a BigQuery dataset with the slugified CLOUD_NAMESPACE"

    def handle(self, *args, **options):
        dataset = slugify(settings.CLOUD_NAMESPACE)
        client = bigquery_client()

        try:
            client.get_dataset(dataset)
            self.stdout.write(
                self.style.WARNING(
                    f"BigQuery dataset with slug '{dataset}' already exists"
                )
            )
        except NotFound:
            client.create_dataset(dataset)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created BigQuery dataset with slug '{dataset}'"
                )
            )
