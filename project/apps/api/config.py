from django.apps import AppConfig
import watson


class ApiConfig(AppConfig):
    """
    Sets the configuration for the api app.
    """

    name = 'apps.api'

    def ready(self):
        chorus = self.get_model("Chorus")
        watson.register(chorus)

        quartet = self.get_model("Quartet")
        watson.register(quartet)

        convention = self.get_model("Convention")
        watson.register(convention)
