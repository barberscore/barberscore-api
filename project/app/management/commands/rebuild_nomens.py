# Django
from django.apps import apps as api_apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to build nomens."

    def handle(self, *args, **options):
        config = api_apps.get_app_config('app')

        models = [
            # Primitives
            'Entity',
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
            'Member',
            'Officer',
            'Performance',
            'Entry',
            'Repertory',
            'Round',
            'Score',
            'Session',
            'Slot',
            'Song',
            'Submission',
        ]

        for model in models:
            Model = config.get_model(model)
            for instance in Model.objects.all():
                instance.save()
            self.stdout.write("Rebuilt {0}".format(Model.__name__))

        return
