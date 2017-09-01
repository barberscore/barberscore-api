# Standard Libary
import datetime

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Group
from bhs.models import Structure
from bhs.updaters import update_or_create_group_from_structure

from django.utils import (
    timezone,
)


class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Update all groups.',
        )

        parser.add_argument(
            '-d',
            '--days',
            type=int,
            dest='days',
            help='Number of days to update from.',
        )

    def handle(self, *args, **options):
        self.stdout.write("Updating groups...")
        if options['all']:
            ss = Structure.objects.all()
        else:
            now = timezone.now()
            cursor = now - datetime.timedelta(days=options['days'])
            ss = Structure.objects.filter(
                updated_ts__gt=cursor,
            )
        total = ss.count()
        i = 0
        for s in ss:
            i += 1
            update_or_create_group_from_structure(s)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} groups.".format(total))
