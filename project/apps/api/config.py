from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Sets the configuration for the api app.
    """

    name = 'apps.api'

    def ready(self):
        # import apps.api.signals
        from apps.api.signals import (
            # session_post_save,
            certification_post_save,
        )
        pass
