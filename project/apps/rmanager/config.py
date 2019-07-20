from django.apps import AppConfig


class RmanagerConfig(AppConfig):
    name = 'apps.rmanager'
    verbose_name = 'Contest Scoring Manager'

    def ready(self):
        from apps.rmanager import signals
        return
