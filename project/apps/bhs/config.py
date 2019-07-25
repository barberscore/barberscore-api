
# Django
from django.apps import AppConfig


class BhsConfig(AppConfig):
    name = 'apps.bhs'
    verbose_name = 'BHS Member Center/Chart & Award Manager'

    def ready(self):
        # from .signals import user_post_save
        import algoliasearch_django as algoliasearch

        from .indexes import AwardIndex
        Award = self.get_model('award')
        algoliasearch.register(Award, AwardIndex)

        from .indexes import ChartIndex
        Chart = self.get_model('chart')
        algoliasearch.register(Chart, ChartIndex)

        from .indexes import GroupIndex
        Group = self.get_model('group')
        algoliasearch.register(Group, GroupIndex)

        from .indexes import PersonIndex
        Person = self.get_model('person')
        algoliasearch.register(Person, PersonIndex)
        return
