import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Organization
from api.tasks import update_or_create_chapter_from_structure
from bhs.models import Structure

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync chapters and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating organizations and structures...")

        # Build list of structures
        structures = Structure.objects.filter(
            kind='Chapter',
        )
        structure_pks = list(structures.values_list('id', flat=True))

        # Delete Orphans
        self.stdout.write("Deleting orphans...")
        orphans = Organization.objects.filter(
            bhs_pk__isnull=False,
            kind=Organization.KIND.chapter,
        ).exclude(
            bhs_pk__in=structure_pks,
        )
        for orphan in orphans:
            log.error("Delete orphan: {0}".format(orphan))
            return
        # Creating/Update Organizations
        self.stdout.write("Queuing organization updates...")
        for structure in structures:
            update_or_create_chapter_from_structure.delay(structure)
        self.stdout.write("Complete")
