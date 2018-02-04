import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.tasks import update_or_create_chapter_enrollment_from_join
from bhs.models import Structure

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating chapter enrollments...")

        # Build list of structures
        structures = Structure.objects.filter(
            kind='Chapter',
        )
        # Delete Orphans
        # Creating/Update Groups
        self.stdout.write("Queuing enrollment updates...")
        for structure in structures:
            js = structure.smjoins.values(
                'subscription__human',
                'structure',
            ).distinct()

            for j in js:
                m = structure.smjoins.filter(
                    subscription__human__id=j['subscription__human'],
                    structure__id=j['structure'],
                ).latest('established_date', 'updated_ts')
                update_or_create_chapter_enrollment_from_join.delay(m)
        self.stdout.write("Complete")
