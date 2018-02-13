import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Member
from api.models import Group
from api.models import Office
from api.models import Officer

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to update all officers from quartets."

    def handle(self, *args, **options):
        self.stdout.write("Updating...")

        # Active Persons MUST have Users
        # UNLESS they don't have email
        members = Member.objects.filter(
            group__status__gt=0,
            group__kind=Group.KIND.quartet,
        )
        office = Office.objects.get(
            name='Quartet Manager',
        )
        for member in members:
            defaults = {
                'status': member.status,
            }

            officer, created = Officer.objects.update_or_create(
                person=member.person,
                group=member.group,
                office=office,
                defaults=defaults,
            )
        self.stdout.write("Complete")
