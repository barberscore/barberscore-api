
# Standard Library
import datetime
import logging
import requests
# Django
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.apps import apps
from django.conf import settings
from apps.bhs.tasks import update_person_from_membercenter
from apps.bhs.tasks import update_group_from_membercenter
# First-Party
User = get_user_model()
Person = apps.get_model('bhs.person')
Group = apps.get_model('bhs.group')

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync with Member Center database."

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
        self.stdout.write("Fetching Persons from Member Center...")
        endpoint, _, token = settings.MEMBERCENTER_URL.partition('@')
        url = "{0}/bhs/person".format(endpoint)
        headers = {
            'Authorization': 'Token {0}'.format(token)
        }
        params = {
            'modified__gt': cursor,
        }
        response = requests.get(
            url,
            headers=headers,
            params=params,
        ).json()
        t = response['meta']['pagination']['count']
        i = 0
        if t > 0:
            for item in response['data']:
                i += 1
                self.stdout.flush()
                self.stdout.write("Updating {0} of {1} Persons...".format(i, t), ending='\r')

                update_person_from_membercenter.delay(item)
                # Only link user if there are officers and an email
                # if person.email and person.officers.filter(status__gt=0):
                #     user, _ = User.objects.get_or_create(email=person.email)
                #     # person.user = user
                #     person.save()
        self.stdout.write("")
        self.stdout.write("Updated {0} Persons.".format(t))
        # if not cursor:
        #     humans = list(Human.objects.values_list('id', flat=True))
        #     self.stdout.write("Deleting Person orphans...")
        #     t = Person.objects.delete_orphans(humans)
        #     self.stdout.write("Deleted {0} Person orphans.".format(t))

        # # Sync Groups
        self.stdout.write("Fetching Groups from Member Center...")
        endpoint, _, token = settings.MEMBERCENTER_URL.partition('@')
        url = "{0}/bhs/group".format(endpoint)
        headers = {
            'Authorization': 'Token {0}'.format(token)
        }
        params = {
            'modified__gt': cursor,
            'kind__gt': 30,
        }
        response = requests.get(
            url,
            headers=headers,
            params=params,
        ).json()
        t = response['meta']['pagination']['count']
        i = 0
        if t > 0:
            for item in response['data']:
                i += 1
                self.stdout.flush()
                self.stdout.write("Updating {0} of {1} Groups...".format(i, t), ending='\r')

                update_group_from_membercenter.delay(item)
                # Only link user if there are officers and an email
                # if person.email and person.officers.filter(status__gt=0):
                #     user, _ = User.objects.get_or_create(email=person.email)
                #     # person.user = user
                #     person.save()
        self.stdout.write("")
        self.stdout.write("Updated {0} Groups.".format(t))        # self.stdout.write("Fetching Structures from Member Center...")
        # structures = Structure.objects.export_values(cursor=cursor)
        # t = len(structures)
        # i = 0
        # for structure in structures:
        #     i += 1
        #     self.stdout.flush()
        #     self.stdout.write("Updating {0} of {1} Groups...".format(i, t), ending='\r')
        #     Group.objects.update_or_create_from_structure(structure)
        # self.stdout.write("")
        # self.stdout.write("Updated {0} Groups.".format(t))
        # if not cursor:
        #     self.stdout.write("Deleting Orphans...")
        #     structures = list(Structure.objects.values_list('id', flat=True))
        #     t = Group.objects.delete_orphans(structures)
        #     self.stdout.write("Deleted {0} Group orphans.".format(t))

        # # Sync Officers
        # self.stdout.write("Fetching Roles from Member Center...")
        # roles = Role.objects.export_values(cursor=cursor)
        # t = len(roles)
        # i = 0
        # for role in roles:
        #     i += 1
        #     self.stdout.flush()
        #     self.stdout.write("Updating {0} of {1} Officers...".format(i, t), ending='\r')
        #     officer, _ = Officer.objects.update_or_create_from_role(role)
        #     if officer.person.email:
        #         user, _ = User.objects.get_or_create(email=person.email)
        #         officer.group.owners.add(user)

        # self.stdout.write("")
        # self.stdout.write("Updated {0} Officers.".format(t))
        # if not cursor:
        #     self.stdout.write("Deleting orphans...")
        #     roles = list(Role.objects.values_list('id', flat=True))
        #     t = Officer.objects.delete_orphans(roles)
        #     self.stdout.write("Deleted {0} Officer orphans.".format(t))


        # # # Sync Members
        # # self.stdout.write("Updating Members.")
        # # self.stdout.write("Fetching Joins...")
        # # joins = Join.objects.export_values(cursor=cursor)
        # # t = len(joins)
        # # i = 0
        # # for join in joins:
        # #     i += 1
        # #     if i != t:
        # #         self.stdout.flush()
        # #     self.stdout.write("Updating {0} of {1} Members...".format(i, t), ending='\r')
        # #     Member.objects.update_or_create_from_join(join)
        # # self.stdout.write("Updated {0} Members.".format(t))
        # # if not cursor:
        # #     self.stdout.write("Deleting orphans...")
        # #     joins = list(Join.objects.values_list('id', flat=True))
        # #     t = Member.objects.delete_orphans(joins)
        # #     self.stdout.write("Deleted {0} Member orphans.".format(t))

        self.stdout.write("Complete.")
