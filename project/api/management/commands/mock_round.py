

# Standard Library
import datetime
from random import randint

# Django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import timezone

# First-Party
from api.models import Appearance
from api.models import Round


class Command(BaseCommand):
    help = "Command to mock remaining round appearances."

    def add_arguments(self, parser):
        parser.add_argument(
            'round_id',
            nargs='?',
        )

    def handle(self, *args, **options):
        round = Round.objects.get(id=options['round_id'])
        if round.status < Round.STATUS.started:
            raise RuntimeError("Round not started")
        appearances = round.appearances.exclude(
            status=Appearance.STATUS.verified,
        )
        for appearance in appearances:
            appearance.mock()
            appearance.save()
        self.stdout.write("Mocked round")
        return
