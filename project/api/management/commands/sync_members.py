# Standard Libary
import datetime

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Member
from bhs.models import SMJoin
from api.updaters import update_or_create_member_from_smjoin

from django.utils import (
    timezone,
)

class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Update all members.',
        )

    def handle(self, *args, **options):
        self.stdout.write("Updating members...")
        duplicates = SMJoin.objects.filter(
            structure__kind__in=[
                'quartet',
                'chapter',
            ],
        ).values(
            'structure__id',
            'subscription__human_id',
        ).order_by(
        ).annotate(
            count_id=models.Count('id')
        ).filter(count_id__gt=1)

        i = 0
        total = duplicates.count()
        for d in duplicates:
            i += 1
            j = SMJoin.objects.filter(
                structure=d['structure__id'],
                subscription__human=d['subscription__human_id'],
            ).order_by(
                'status',
                'created_ts',
            ).last()
            update_or_create_member_from_smjoin(j)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated members.")
