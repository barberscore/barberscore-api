
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Group
from api.tasks import update_or_create_group_from_structure
from bhs.models import Structure


class Command(BaseCommand):
    help = "Command to sync groups and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating groups and structures...")

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
            orphan.delete()
        # Creating/Update Groups
        self.stdout.write("Queuing group updates...")
        for structure in structures:
            update_or_create_group_from_structure.delay(structure)
        self.stdout.write("Complete")
