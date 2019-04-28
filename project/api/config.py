

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
        from .indexes import ChartIndex
        from .indexes import ConventionIndex
        # from .indexes import PersonIndex
        from .indexes import GroupIndex
        Award = self.get_model('award')
        Chart = self.get_model('chart')
        Convention = self.get_model('convention')
        # Person = self.get_model('person')
        Group = self.get_model('group')
        algoliasearch.register(Award, AwardIndex)
        algoliasearch.register(Chart, ChartIndex)
        algoliasearch.register(Convention, ConventionIndex)
        # algoliasearch.register(Person, PersonIndex)
        algoliasearch.register(Group, GroupIndex)
        return
