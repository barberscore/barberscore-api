# Django
from django.apps import apps as api_apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to build nomens."

    def handle(self, *args, **options):
        config = api_apps.get_app_config('api')

        models = [
            # Primitives
            'Organization',
            'Group',
            'Chart',
            'Office',
            'Person',
            'Venue',
            'Award',
            'Convention',
            # Joins
            'Assignment',
            'Contest',
            'Contestant',
            'Grantor',
            'Member',
            'Officer',
            'Appearance',
            'Entry',
            'Repertory',
            'Round',
            'Score',
            'Session',
            'Panelist',
            'Song',
        ]

        for model in models:
            Model = config.get_model(model)
            for instance in Model.objects.all():
                instance.save()
            self.stdout.write("Rebuilt {0}".format(Model.__name__))

        return
