
# Standard Library
import datetime
import logging

# Django
from django.core.management.base import BaseCommand
from django.utils import timezone

# First-Party
from api.models import Person
from api.models import Group
from api.models import Member
from api.models import Officer
from api.models import User
from bhs.models import Human
from bhs.models import Join
from bhs.models import Role
from bhs.models import Structure
from bhs.models import Subscription

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
        self.stdout.write("Updating Persons.")
        self.stdout.write("Fetching humans...")
        humans = Human.objects.export_values(cursor=cursor)
        t = len(humans)
        i = 0
        for human in humans:
            i += 1
            self.stdout.write("Updating {0} of {1} persons...".format(i, t), ending='\r')
            if i != t:
                self.stdout.flush()
            Person.objects.update_or_create_from_human(human)
        self.stdout.write("Updated {0} persons.".format(t))
        if not cursor:
            self.stdout.write("Deleting orphans...")
            humans = list(Human.objects.values_list('id', flat=True))
            t = Person.objects.delete_orphans(humans)
            self.stdout.write("Deleted {0} person orphans.".format(t))

        # Sync Groups
        self.stdout.write("Updating Groups.")
        self.stdout.write("Fetching structures...")
        structures = Structure.objects.export_values(cursor=cursor)
        t = len(structures)
        i = 0
        for structure in structures:
            i += 1
            self.stdout.write("Updating {0} of {1} groups...".format(i, t), ending='\r')
            if i != t:
                self.stdout.flush()
            Group.objects.update_or_create_from_structure(structure)
        self.stdout.write("Updated {0} groups.".format(t))
        if not cursor:
            self.stdout.write("Deleting orphans...")
            structures = list(Structure.objects.values_list('id', flat=True))
            t = Group.objects.delete_orphans(structures)
            self.stdout.write("Deleted {0} group orphans.".format(t))

        # Sync Officers
        self.stdout.write("Updating Officers.")
        self.stdout.write("Fetching roles...")
        roles = Role.objects.export_values(cursor=cursor)
        t = len(roles)
        i = 0
        for role in roles:
            i += 1
            self.stdout.write("Updating {0} of {1} officers...".format(i, t), ending='\r')
            if i != t:
                self.stdout.flush()
            Officer.objects.update_or_create_from_role(role)
        self.stdout.write("Updated {0} officers.".format(t))
        if not cursor:
            self.stdout.write("Deleting orphans...")
            roles = list(Role.objects.values_list('id', flat=True))
            t = Officer.objects.delete_orphans(roles)
            self.stdout.write("Deleted {0} officer orphans.".format(t))

        # Sync Members
        self.stdout.write("Updating Members.")
        self.stdout.write("Fetching joins...")
        joins = Join.objects.export_values(cursor=cursor)
        t = len(joins)
        i = 0
        for join in joins:
            i += 1
            self.stdout.write("Updating {0} of {1} members...".format(i, t), ending='\r')
            if i != t:
                self.stdout.flush()
            Member.objects.update_or_create_from_join(join)
        self.stdout.write("Updated {0} members.".format(t))
        if not cursor:
            self.stdout.write("Deleting orphans...")
            joins = list(Join.objects.values_list('id', flat=True))
            t = Member.objects.delete_orphans(joins)
            self.stdout.write("Deleted {0} member orphans.".format(t))

        self.stdout.write("Complete.")
