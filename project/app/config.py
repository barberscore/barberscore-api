# Django
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'app'

    def ready(self):
        from .signals import (
            user_post_save,
        )
