import logging
import django_rq
# Django
from django.core.management.base import BaseCommand
# First-Party
from api.models import Officer
from bhs.models import Role

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync bhs roles with officers."

    def handle(self, *args, **options):
        self.stdout.write("Updating officers...")
        # Get unique active joins for Chapters
        roles = Role.objects.exclude(
            name='Quartet Admin',
        ).order_by(
            'start_date'
        ).values_list(
            'id',
            'name',
            'structure',
            'human',
            'start_date',
            'end_date',
        )
        # Creating/Update Groups
        self.stdout.write("Queuing officer updates...")
        for role in roles:
            django_rq.enqueue(
                Officer.objects.update_or_create_from_role_object,
                role,
            )
        self.stdout.write("Complete")
