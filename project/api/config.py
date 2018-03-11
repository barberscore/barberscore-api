# Django
import os
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'api'

    def ready(self):
        if os.environ['DJANGO_SETTINGS_MODULE'] != 'project.settings.base':
            from .signals import (
                user_pre_delete,
            )
            import algoliasearch_django as algoliasearch
            from .indexes import ChartIndex
            Chart = self.get_model('chart')
            algoliasearch.register(Chart, ChartIndex)
        return
