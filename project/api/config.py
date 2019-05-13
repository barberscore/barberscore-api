

# Standard Library
import os

# Django
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Sets the configuration for the api app."""

    name = 'api'

    def ready(self):
        import algoliasearch_django as algoliasearch
        import api.signals
        from .indexes import AwardIndex
        from .indexes import ConventionIndex
        Award = self.get_model('award')
        Convention = self.get_model('convention')
        algoliasearch.register(Award, AwardIndex)
        algoliasearch.register(Convention, ConventionIndex)
        return
