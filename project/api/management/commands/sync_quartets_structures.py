import django_rq
import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Group
from bhs.models import Structure

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating quartets and structures...")

        # Build list of structures
        structures = Structure.objects.filter(
            kind='Quartet',
        )
        structure_pks = list(structures.values_list('id', flat=True))

        # Delete Orphans
        self.stdout.write("Deleting orphans...")
        orphans = Group.objects.filter(
            bhs_pk__isnull=False,
            kind=Group.KIND.quartet,
        ).exclude(
            bhs_pk__in=structure_pks,
        )
        for orphan in orphans:
            log.error("Delete orphan: {0}".format(orphan))
            return
        # Creating/Update Groups
        self.stdout.write("Queuing group updates...")
        for structure in structures:
            django_rq.enqueue(
                Group.objects.update_or_create_from_structure,
                structure,
            )
        self.stdout.write("Complete")
