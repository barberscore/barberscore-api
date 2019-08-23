from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    name = 'apps.registration'
    verbose_name = 'Contest Entry Manager'

    def ready(self):
        return
