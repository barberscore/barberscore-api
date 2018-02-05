import django_rq
import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Enrollment, Organization, Member

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating memberships to enrollments...")

        # Build list of active chapters with BHS Source
        enrollments = Enrollment.objects.filter(
            organization__kind=Organization.KIND.chapter,
            bhs_pk__isnull=False,
        )

        # Delete Orphans
        # Creating/Update Groups
        self.stdout.write("Queuing chorus member updates...")
        for enrollment in enrollments:
            django_rq.enqueue(
                Member.objects.update_or_create_from_enrollment,
                enrollment,
            )
        self.stdout.write("Complete")
