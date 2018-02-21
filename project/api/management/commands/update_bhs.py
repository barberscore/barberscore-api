# Standard Libary
import datetime
import logging

# Django
from django.core.management.base import BaseCommand
from django.utils import timezone

# First-Party
from api.models import Person
from api.models import User
from bhs.models import Human
from bhs.models import Structure
from bhs.models import Role
from bhs.models import Join

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
            cursor = None

        # Sync Persons
        t = Human.objects.update_persons(cursor=cursor)
        self.stdout.write("Queued {0} persons.".format(t))
        t = Human.objects.delete_orphans()
        self.stdout.write("Deleted {0} person orphans.".format(t))

        # Sync Groups
        t = Structure.objects.update_groups(cursor=cursor)
        self.stdout.write("Queued {0} groups.".format(t))
        t = Structure.objects.delete_orphans()
        self.stdout.write("Deleted {0} group orphans.".format(t))

        # Sync Members
        t = Join.objects.update_members()
        self.stdout.write("Queued {0} members.".format(t))

        # Sync Roles
        t = Role.objects.update_officers()
        # self.stdout.write("Queued {0} officers.".format(t))
        self.stdout.write("BYPASSED chapter officers.")

        # Sync Users
        t = Person.objects.update_users(cursor=cursor)
        self.stdout.write("Queued {0} users.".format(t))

        # Sync Accounts
        # t = User.objects.update_accounts(cursor=cursor)
        # self.stdout.write("Queued {0} accounts.".format(t))

        self.stdout.write("Complete.")
