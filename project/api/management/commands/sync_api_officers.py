import logging
import django_rq
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Member
from api.models import Group
from api.models import Office
from api.models import Officer
from bhs.models import Role

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to update all officers."

    def handle(self, *args, **options):
        self.stdout.write("Updating...")

        roles = Role.objects.exclude(
            name='Quartet Admin',
        )
        i = 0
        t = roles.count()
        for role in roles:
            i += 1
            django_rq.enqueue(
                Officer.objects.update_or_create_from_role,
                role,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} chapter officers...".format(i, t), ending='\r')
        # Active Persons MUST have Users
        # UNLESS they don't have email
        # Quartet Admins Update
        members = Member.objects.filter(
            group__kind=Group.KIND.quartet,
        )
        i = 0
        t = members.count()
        for member in members:
            i += 1
            django_rq.enqueue(
                Officer.objects.update_or_create_from_member,
                member,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} quartet officers...".format(i, t), ending='\r')
        self.stdout.write("Complete")
