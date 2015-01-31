from django.apps import AppConfig

from utilities.signals import (
    contestant_pre_save,
    contest_pre_save,
)


class ConventionConfig(AppConfig):
    """
    Sets the configuration for the convention app.
    """

    name = 'convention'

    def ready(self):
        contestant_pre_save,
        contest_pre_save,
        pass
