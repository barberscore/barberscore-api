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

        singer = self.get_model("Singer")
        watson.register(singer)

        contest = self.get_model("Contest")
        watson.register(contest)

        convention = self.get_model("Convention")
        watson.register(convention)

        district = self.get_model("District")
        watson.register(district)
