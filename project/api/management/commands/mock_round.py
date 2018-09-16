

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
        appearances = round.appearances.exclude(
            status=Appearance.STATUS.verified,
        )
        for appearance in appearances:
            prelim = appearance.competitor.entry.prelim
            if not prelim:
                prelim = randint(65, 80)
            if prelim:
                songs = appearance.songs.all()
                for song in songs:
                    scores = song.scores.all()
                    for score in scores:
                        d = randint(-4,4)
                        score.points = prelim + d
                        score.save()
            if appearance.status == appearance.STATUS.new:
                raise RuntimeError("Out of state")
            if appearance.status == appearance.STATUS.built:
                appearance.start()
                appearance.finish()
                appearance.verify()
                appearance.save()
                continue
            if appearance.status == appearance.STATUS.started:
                appearance.finish()
                appearance.verify()
                appearance.save()
                continue
            if appearance.status == appearance.STATUS.finished:
                appearance.verify()
                appearance.save()
                continue
        self.stdout.write("Mocked round")
        return
