# Standard Libary
import datetime
import logging

# Django
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import timezone

# First-Party
from api.models import Enrollment
from api.models import Group
from api.models import Member
from api.models import Organization
from api.models import Person
from bhs.models import Human
from bhs.models import SMJoin
from bhs.models import Structure

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync with BHS database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            dest='days',
            nargs='?',
            const=1,
            help='Number of days to update.',
        )

        parser.add_argument(
            '--hours',
            type=int,
            dest='hours',
            nargs='?',
            const=1,
            help='Number of hours to update.',
        )

        parser.add_argument(
            '--minutes',
            type=int,
            dest='minutes',
            nargs='?',
            const=1,
            help='Number of hours to update.',
        )

    def handle(self, *args, **options):
        # Set Cursor
        if options['days']:
            cursor = timezone.now() - datetime.timedelta(days=options['days'], hours=1)
        elif options['hours']:
            cursor = timezone.now() - datetime.timedelta(hours=options['hours'], minutes=5)
        elif options['minutes']:
            cursor = timezone.now() - datetime.timedelta(minutes=options['minutes'], seconds=5)
        else:
            raise CommandError('No argument specified.')

        # Sync Persons
        self.stdout.write("Updating persons...")
        hs = Human.objects.filter(
            updated_ts__gt=cursor,
        ).exclude(id__in=[
            '8e44efc7-ea7a-4075-9e35-529d4e458f89',  # Duplicate to strip
        ])
        i = 0
        t = hs.count()
        for h in hs:
            i += 1
            try:
                Person.objects.update_or_create_from_human(h)
            except Exception as e:
                log.error(e)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} persons.".format(t))

        # Sync BHS Status and Current Through
        self.stdout.write("Updating BHS status...")
        js = SMJoin.objects.filter(
            status=True,
            structure__kind='organization',
            subscription__items_editable=True,
            updated_ts__gt=cursor,
        ).order_by('updated_ts')
        i = 0
        t = js.count()
        for j in js:
            i += 1
            try:
                Person.objects.update_from_join(j)
            except Exception as e:
                log.error(e)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} statuses.".format(t))

        # Sync Organizations
        self.stdout.write("Updating organizations...")
        ss = Structure.objects.filter(
            kind__in=[
                'organization',
                'district',
                'chapter',
            ],
            updated_ts__gt=cursor,
        )
        i = 0
        t = ss.count()
        for s in ss:
            i += 1
            try:
                Organization.objects.update_or_create_from_structure(s)
            except Exception as e:
                log.error(e)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} organizations.".format(t))

        # Sync Groups
        self.stdout.write("Updating groups...")
        ss = Structure.objects.filter(
            kind__in=[
                'quartet',
                'chapter',
            ],
            updated_ts__gt=cursor,
        ).exclude(id__in=[
            '0207656d-64ff-443d-862f-bc4fec6ea2be'
        ])
        i = 0
        t = ss.count()
        for s in ss:
            i += 1
            try:
                Group.objects.update_or_create_from_structure(s)
            except Exception as e:
                log.error(e)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} groups.".format(t))

        # Sync Members
        self.stdout.write("Updating memberships...")
        js = SMJoin.objects.filter(
            status=True,
            structure__kind__in=[
                'quartet',
                'chapter',
            ],
            updated_ts__gt=cursor,
        ).order_by('updated_ts')
        i = 0
        t = js.count()
        for j in js:
            i += 1
            try:
                Member.objects.update_or_create_from_join(j)
            except Exception as e:
                log.error(e)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} memberships.".format(t))

        # Sync Enrollments - Very Slow!
        self.stdout.write("Updating enrollments...")
        js = SMJoin.objects.filter(
            status=True,
            subscription__items_editable=True,
            updated_ts__gt=cursor,
        ).order_by('updated_ts')
        i = 0
        t = js.count()
        for j in js:
            i += 1
            try:
                Enrollment.objects.update_or_create_from_join(j)
            except Exception as e:
                log.error(e)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} enrollments.".format(t))
        self.stdout.write("Complete.")

        log.info("Successful from {0}.".format(cursor))
