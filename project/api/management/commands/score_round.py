# Django
# Standard Libary
import json
import random
from itertools import chain
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

# First-Party
from api.models import (
    Appearance,
    Round,
)


class Command(BaseCommand):
    help="Command to seed convention."
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-r',
            '--round',
            dest='round',
            default=None,
            help='Score round.',
        )

    def handle(self, *args, **options):
        # Create Admin
        round_id = options['round']
        try:
            round = Round.objects.get(id=round_id)
        except Round.DoesNotExist:
            raise CommandError("Can not find Round.")
        for appearance in round.appearances.filter(
            status=Appearance.STATUS.scheduled,
        ):
            appearance.start()
            for song in appearance.songs.all():
                song.chart = appearance.entry.entity.repertories.order_by('?').first().chart
                song.save()
            appearance.finish()
            scores = Score.objects.filter(
                song__appearance=appearance,
            )
            center = random.randint(70,80)
            for score in song.scores.all():
                offset = random.randint(-5,5)
                score.points = center + offset
                score.save()
            appearance.confirm()
            appearance.save()
