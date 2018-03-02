# Django
from django.apps import AppConfig
import algoliasearch_django as algoliasearch


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'api'

    def ready(self):
        from .signals import (
            user_pre_delete,
        )
        from .indexes import ChartIndex
        Chart = self.get_model('chart')
        algoliasearch.register(Chart, ChartIndex)
