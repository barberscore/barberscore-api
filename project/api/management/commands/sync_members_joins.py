import logging
import django_rq
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Member
from bhs.models import SMJoin

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating quartet enrollments...")

        # Get unique active joins for Chapters
        joins = SMJoin.objects.filter(
            inactive_date=None,
            structure__kind='Quartet',
        ).values(
            'id',
            'subscription__human',
            'structure',
        ).distinct()
        # Creating/Update Groups
        self.stdout.write("Queuing enrollment updates...")
        for join in joins:
            django_rq.enqueue(
                Member.objects.update_or_create_from_join,
                join,
            )
        self.stdout.write("Complete")
