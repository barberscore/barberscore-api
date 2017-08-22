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
        if options['all']:
            js = SMJoin.objects.all()
        else:
            now = datetime.date.today()
            cursor = now - datetime.timedelta(days=1)
            js = SMJoin.objects.filter(
                created_ts__gt=cursor,
            )
        total = js.count()
        i = 0
        for j in js:
            update_or_create_member_from_smjoin(j)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
            i += 1
