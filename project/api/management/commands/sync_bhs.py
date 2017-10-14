# Standard Libary
import datetime

# Django
from django.core.management.base import BaseCommand
from django.utils import timezone

from bhs.models import (
    Human,
    SMJoin,
    Structure,
)
from bhs.updaters import (
    update_or_create_group_from_structure,
    update_or_create_member_from_smjoin,
    update_or_create_person_from_human,
)


class Command(BaseCommand):
    help = "Command to sync with BHS database."

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
            nargs='?',
            const=2,
            help='Number of days to update.',
        )

    def handle(self, *args, **options):
        # sync persons
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
            h.full_clean()
            i += 1
            update_or_create_person_from_human(h)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} persons.".format(total))
        # Sync Groups
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
            s.full_clean()
            i += 1
            update_or_create_group_from_structure(s)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} groups.".format(total))

        # Sync Members
        self.stdout.write("Updating members...")
        if options['all']:
            js = SMJoin.objects.exclude(
                updated_ts=None,
            ).filter(
                structure__kind__in=[
                    'organization',
                    'quartet',
                    'chapter',
                ],
            ).order_by('updated_ts')
        else:
            now = timezone.now()
            cursor = now - datetime.timedelta(days=options['days'])
            js = SMJoin.objects.filter(
                structure__kind__in=[
                    'organization',
                    'quartet',
                    'chapter',
                ],
                updated_ts__gt=cursor,
            ).order_by('updated_ts')
        i = 0
        total = js.count()
        for j in js:
            j.full_clean()
            i += 1
            update_or_create_member_from_smjoin(j)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} members.".format(total))
        self.stdout.write("Complete")
