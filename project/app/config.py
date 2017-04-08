# Django
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'app'

    def ready(self):
        from .signals import (
            contest_post_save,
            contestant_post_save,
            appearance_post_save,
            entry_post_save,
            song_post_save,
            user_post_save,
        )
