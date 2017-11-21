# Standard Libary
import datetime

# Django
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.utils import timezone

from api.models import (
    Person,
    Group,
    Enrollment,
    Member,
    Organization,
)

from bhs.models import (
    Human,
    SMJoin,
    Structure,
)


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
            Person.objects.update_or_create_from_human(h)
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
            Person.objects.update_from_join(j)
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
            Organization.objects.update_or_create_organization_from_structure(s)
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
        )
        i = 0
        t = ss.count()
        for s in ss:
            i += 1
            Group.objects.update_or_create_group_from_structure(s)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} groups.".format(t))

        # Sync Members
        self.stdout.write("Updating memberships...")
        js = SMJoin.objects.filter(
            status=True,
            subscription__items_editable=True,
            updated_ts__gt=cursor,
        ).order_by('updated_ts')
        i = 0
        t = js.count()
        for j in js:
            i += 1
            Member.objects.update_or_create_from_join(j)
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
        for s in ss:
            i += 1
            Enrollment.objects.update_or_create_from_join(j)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} enrollments.".format(t))

        self.stdout.write("Complete.")
