# Django
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'api'

    def ready(self):
        from .signals import (
            user_post_save,
            person_post_save,
            user_pre_delete,
        )
