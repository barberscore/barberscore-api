from django.apps import AppConfig


class SmanagerConfig(AppConfig):
    name = 'apps.smanager'
    verbose_name = 'Contest Entry Manager'

    def ready(self):
        return
