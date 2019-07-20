
# Django
from django.apps import AppConfig


class BhsConfig(AppConfig):
    name = 'apps.bhs'
    verbose_name = 'BHS Member Center/Chart & Award Manager'

    def ready(self):
        # from .signals import user_post_save
        # import algoliasearch_django as algoliasearch
        # from .indexes import AwardIndex
        # from .indexes import ChartIndex
        # from .indexes import PersonIndex
        # from .indexes import GroupIndex
        # Award = self.get_model('award')
        # Chart = self.get_model('chart')
        # Person = self.get_model('person')
        # Group = self.get_model('group')
        # algoliasearch.register(Award, AwardIndex)
        # algoliasearch.register(Chart, ChartIndex)
        # algoliasearch.register(Person, PersonIndex)
        # algoliasearch.register(Group, GroupIndex)
        return
