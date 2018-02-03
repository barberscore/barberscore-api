
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Group
from api.tasks import update_chorus_from_chapter


class Command(BaseCommand):
    help = "Command to update all active chorus from chapter info."

    def handle(self, *args, **options):
        self.stdout.write("Updating...")

        # Build list of active, BHS choruses
        choruses = Group.objects.filter(
            status__gt=0,
            kind=Group.KIND.chorus,
            bhs_pk__isnull=False,
        )
        # Creating/Update Groups
        self.stdout.write("Queuing chorus updates...")
        for chorus in choruses:
            update_chorus_from_chapter.delay(chorus)
        self.stdout.write("Complete")
