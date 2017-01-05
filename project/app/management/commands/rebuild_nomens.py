# Django
from django.core.management.base import BaseCommand
from django.apps import apps as api_apps


class Command(BaseCommand):
    help = "Command to build nomens."

    def handle(self, *args, **options):
        config = api_apps.get_app_config('app')

        primitives = [
            'Award',
            'Catalog',
            'Chapter',
            'Convention',
            'Group',
            'Organization',
            'Person',
            'Venue',
        ]

        for primitive in primitives:
            model = config.get_model(primitive)
            for i in model.objects.all():
                i.calculate_nomen()
                i.save()

        branches = [
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

        for branch in branches:
            model = config.get_model(branch)
            for i in model.objects.all():
                i.calculate_nomen()
                i.save()

        return "Rebuilt nomens."
