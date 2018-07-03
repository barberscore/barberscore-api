# Django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime
from random import randint

from api.models import Appearance

class Command(BaseCommand):
    help = "Command to rebuild denorms."

    def add_arguments(self, parser):
        parser.add_argument(
            'appearance_id',
            nargs='?',
        )

    def handle(self, *args, **options):
        # Set Cursor
        appearance = Appearance.objects.get(id=options['appearance_id'])
        prelim = appearance.competitor.entry.prelim
        if not prelim:
            prelim = 75
        if prelim:
            songs = appearance.songs.all()
            for song in songs:
                scores = song.scores.all()
                for score in scores:
                    d = randint(-5,5)
                    score.points = prelim + d
                    score.save()
            self.stdout.write("Scored")
        return
