from django.apps import AppConfig


class SmanagerConfig(AppConfig):
    name = 'apps.smanager'
    verbose_name = 'Session Manager'

    def ready(self):
        # import algoliasearch_django as algoliasearch
        # from .indexes import ConventionIndex
        # Convention = self.get_model('convention')
        # algoliasearch.register(Convention, ConventionIndex)
        return
