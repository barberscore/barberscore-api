# Django
from django.core.management.base import BaseCommand
from django.apps import apps as api_apps


class Command(BaseCommand):
    help = "Command to build nomens."

    def handle(self, *args, **options):
        config = api_apps.get_app_config('app')

        models = [
            'Award',
            'Catalog',
            'Chapter',
            'Convention',
            'Group',
            'Organization',
            'Person',
            'Venue',
            # Branches,
            'Host',
            'Session',
            'Judge',
            'Assignment',
            'Member',
            'Role',
            'Round',
            'Contest',
            'Performer',
            'Slot',
            'Submission',
            'Contestant',
            'Performance',
            'Song',
            'Score',
        ]

        for model in models:
            Model = config.get_model(model)
            for instance in Model.objects.all():
                instance.save()

        return "Rebuilt nomens."
