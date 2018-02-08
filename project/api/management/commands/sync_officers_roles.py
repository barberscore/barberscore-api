import logging
import django_rq
from datetime import date
# Django
from django.core.management.base import BaseCommand
from django.db.models import Q
# First-Party
from api.models import Officer
from bhs.models import Role

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating officers...")
        # Get unique active joins for Chapters
        today = date.today()
        roles = Role.objects.filter(
            Q(end_date=None) |
            Q(end_date__gt=today)
        ).exclude(
            name='Quartet Admin',
        ).values(
            'human',
            'structure',
        )
        # Creating/Update Groups
        self.stdout.write("Queuing enrollment updates...")
        for role in roles:
            django_rq.enqueue(
                Officer.objects.update_or_create_from_role,
                role,
            )
        self.stdout.write("Complete")
