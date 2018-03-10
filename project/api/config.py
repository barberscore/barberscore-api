# Django
import os
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'api'

    def ready(self):
        pass
        # if os.environ['DJANGO_SETTINGS_MODULE'] != 'settings_ci':
        #     from .signals import (
        #         user_pre_delete,
        #     )
        #     import algoliasearch_django as algoliasearch
        #     from .indexes import ChartIndex
        #     Chart = self.get_model('chart')
        #     algoliasearch.register(Chart, ChartIndex)
        # return
