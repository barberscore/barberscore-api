from django.apps import AppConfig

from .signals import (
    contestant_pre_save,
)


class ConventionConfig(AppConfig):
    name = 'apps.convention'

    def ready(self):
        contestant_pre_save
        pass
