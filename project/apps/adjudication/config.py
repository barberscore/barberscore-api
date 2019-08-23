from django.apps import AppConfig


class AdjudicationConfig(AppConfig):
    name = 'apps.adjudication'
    verbose_name = 'Contest Scoring Manager'

    def ready(self):
        from apps.adjudication import signals
        return
