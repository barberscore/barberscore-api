# Django
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'apps.api'

    def ready(self):
        from .signals import (
            session_post_save,
            performance_post_save,
        )
        # pass
