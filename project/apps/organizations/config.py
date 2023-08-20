
# Django
from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    name = 'apps.organizations'
    verbose_name = 'Organizations'

    def ready(self):
        return