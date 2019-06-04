from django.apps import AppConfig


class CmanagerConfig(AppConfig):
    name = 'apps.cmanager'
    verbose_name = 'Convention Manager'

    def ready(self):
        from apps.cmanager import signals
        import algoliasearch_django as algoliasearch
        from .indexes import AwardIndex
        from .indexes import ConventionIndex
        Award = self.get_model('award')
        Convention = self.get_model('convention')
        algoliasearch.register(Award, AwardIndex)
        algoliasearch.register(Convention, ConventionIndex)
        return
