# Standard Libary
import maya
import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Person
from api.models import Member
from api.models import Officer
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
            cursor = maya.now().subtract(days=options['days'], hours=1).datetime()
        elif options['hours']:
            cursor = maya.now().subtract(hours=options['hours'], minutes=5).datetime()
        elif options['minutes']:
            cursor = maya.now().subtract(minutes=options['minutes'], seconds=5).datetime()
        else:
            cursor = None

        if cursor:
            active_only = True
        else:
            active_only = False

        # Sync Persons
        t = Human.objects.update_persons(cursor=cursor, active_only=active_only)
        self.stdout.write("Queued {0} persons.".format(t))
        t = Human.objects.delete_orphans()
        self.stdout.write("Deleted {0} person orphans.".format(t))

        # Sync Groups
        t = Structure.objects.update_groups(cursor=cursor, active_only=active_only)
        self.stdout.write("Queued {0} groups.".format(t))
        t = Structure.objects.delete_orphans()
        self.stdout.write("Deleted {0} group orphans.".format(t))

        # Sync Members
        latest = Member.objects.latest('created').created
        t = Join.objects.update_members(cursor=latest)
        self.stdout.write("Queued {0} members.".format(t))

        # Sync Roles
        latest = Officer.objects.latest('created').created
        t = Role.objects.update_officers(cursor=latest)
        self.stdout.write("Queued {0} officers.".format(t))

        # Sync Users
        t = Person.objects.update_users(cursor=cursor, active_only=active_only)
        self.stdout.write("Queued {0} users.".format(t))

        self.stdout.write("Complete.")
