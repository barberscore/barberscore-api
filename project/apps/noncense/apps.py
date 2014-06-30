from django.apps import AppConfig


class NoncenseConfig(AppConfig):
    """
    Sets the configuration for the noncense app.
    """

    name = 'apps.noncense'

    def ready(self):
        pass
