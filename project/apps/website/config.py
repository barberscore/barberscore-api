from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """
    Sets the configuration for the website app.
    """

    name = 'apps.website'

    def ready(self):
        pass
