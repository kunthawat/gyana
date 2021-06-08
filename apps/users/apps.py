import analytics
from django.apps import AppConfig
from django.conf import settings


class UserConfig(AppConfig):
    name = "apps.users"
    label = "users"

    def ready(self):
        from . import signals

        if settings.SEGMENT_ANALYTICS_WRITE_KEY:
            analytics.debug = settings.DEBUG
            analytics.write_key = settings.SEGMENT_ANALYTICS_WRITE_KEY
