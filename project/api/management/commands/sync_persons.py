# Standard Libary
import datetime

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Person
from bhs.models import Human
from bhs.updaters import update_or_create_person_from_human

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
            help='Update all persons.',
        )

        parser.add_argument(
            '-d',
            '--days',
            type=int,
            dest='days',
            const=2,
            help='Number of days to update.',
        )

    def handle(self, *args, **options):
        self.stdout.write("Updating persons...")
        if options['all']:
            hs = Human.objects.all()
        else:
            now = timezone.now()
            cursor = now - datetime.timedelta(days=options['days'])
            hs = Human.objects.filter(
                updated_ts__gt=cursor,
            )
        total = hs.count()
        i = 0
        for h in hs:
            i += 1
            update_or_create_person_from_human(h)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} persons.".format(total))
