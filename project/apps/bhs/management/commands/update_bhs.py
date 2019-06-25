
# Standard Library
import datetime
import logging

# Django
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
# First-Party
from apps.bhs.models import Person
from apps.bhs.models import Group
from apps.bhs.models import Member
from apps.bhs.models import Officer
from apps.bhs.models import Human
from apps.bhs.models import Join
from apps.bhs.models import Role
from apps.bhs.models import Structure
from apps.bhs.models import Subscription
from apps.bhs.tasks import create_or_update_account_from_human
from apps.bhs.tasks import delete_account_from_human
from apps.bhs.tasks import get_account_orphans

User = get_user_model()


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
        self.stdout.write("Updating Persons and Accounts.")
        self.stdout.write("Fetching Humans...")
        humans = Human.objects.export_values(cursor=cursor)
        t = len(humans)
        i = 0
        for human in humans:
            i += 1
            if i != t:
                self.stdout.flush()
            self.stdout.write("Updating {0} of {1} Persons/Accounts/Users...".format(i, t), ending='\r')
            person, _ = Person.objects.update_or_create_from_human(human)
            try:
                account, created = create_or_update_account_from_human(human)
            except Exception as e:
                log.error((e, human))
                continue
            if created:
                User.objects.create_user(
                    username=account['user_id'],
                    person=person,
                )
        self.stdout.write("Updated {0} Accounts.".format(t))
        if not cursor:
            humans = list(Human.objects.values_list('id', flat=True))
            self.stdout.write("Deleting Person orphans...")
            t = Person.objects.delete_orphans(humans)
            self.stdout.write("Deleted {0} Person orphans.".format(t))
            self.stdout.write("Deleting Account orphans...")
            orphans = get_account_orphans()
            t = len(orphans)
            for orphan in orphans:
                delete_account_from_human(orphan)
            self.stdout.write("Deleted {0} Account orphans.".format(t))

        # Sync Groups
        self.stdout.write("Updating Groups.")
        self.stdout.write("Fetching Structures...")
        structures = Structure.objects.export_values(cursor=cursor)
        t = len(structures)
        i = 0
        for structure in structures:
            i += 1
            if i != t:
                self.stdout.flush()
            self.stdout.write("Updating {0} of {1} Groups...".format(i, t), ending='\r')
            Group.objects.update_or_create_from_structure(structure)
        self.stdout.write("Updated {0} Groups.".format(t))
        if not cursor:
            self.stdout.write("Deleting Orphans...")
            structures = list(Structure.objects.values_list('id', flat=True))
            t = Group.objects.delete_orphans(structures)
            self.stdout.write("Deleted {0} Group orphans.".format(t))

        # # Sync Officers
        # self.stdout.write("Updating Officers.")
        # self.stdout.write("Fetching Roles...")
        # roles = Role.objects.export_values(cursor=cursor)
        # t = len(roles)
        # i = 0
        # for role in roles:
        #     i += 1
        #     if i != t:
        #         self.stdout.flush()
        #     self.stdout.write("Updating {0} of {1} Officers...".format(i, t), ending='\r')
        #     Officer.objects.update_or_create_from_role(role)
        # self.stdout.write("Updated {0} Officers.".format(t))
        # if not cursor:
        #     self.stdout.write("Deleting orphans...")
        #     roles = list(Role.objects.values_list('id', flat=True))
        #     t = Officer.objects.delete_orphans(roles)
        #     self.stdout.write("Deleted {0} Officer orphans.".format(t))

        # # Sync Members
        # self.stdout.write("Updating Members.")
        # self.stdout.write("Fetching Joins...")
        # joins = Join.objects.export_values(cursor=cursor)
        # t = len(joins)
        # i = 0
        # for join in joins:
        #     i += 1
        #     if i != t:
        #         self.stdout.flush()
        #     self.stdout.write("Updating {0} of {1} Members...".format(i, t), ending='\r')
        #     Member.objects.update_or_create_from_join(join)
        # self.stdout.write("Updated {0} Members.".format(t))
        # if not cursor:
        #     self.stdout.write("Deleting orphans...")
        #     joins = list(Join.objects.values_list('id', flat=True))
        #     t = Member.objects.delete_orphans(joins)
        #     self.stdout.write("Deleted {0} Member orphans.".format(t))

        self.stdout.write("Complete.")
