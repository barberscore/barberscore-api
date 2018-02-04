import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Enrollment, Organization
from api.tasks import update_or_create_members_from_enrollments

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating quartets and structures...")

        # Build list of active chapters with BHS Source
        enrollments = Enrollment.objects.filter(
            organization__kind=Organization.KIND.chapter,
            bhs_pk__isnull=False,
        )

        # Delete Orphans
        # Creating/Update Groups
        self.stdout.write("Queuing chorus member updates...")
        for enrollment in enrollments:
            update_or_create_members_from_enrollments.delay(enrollment)
        self.stdout.write("Complete")
