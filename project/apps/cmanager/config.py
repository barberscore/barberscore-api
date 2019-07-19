from django.apps import AppConfig


class CmanagerConfig(AppConfig):
    name = 'apps.cmanager'
    verbose_name = 'Convention Manager'

    def ready(self):
        # import algoliasearch_django as algoliasearch
        # from .indexes import ConventionIndex
        # Convention = self.get_model('convention')
        # algoliasearch.register(Convention, ConventionIndex)
        return
