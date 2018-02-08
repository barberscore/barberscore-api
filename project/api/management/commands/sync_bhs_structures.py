import django_rq
import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Organization
from bhs.models import Structure

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync chapters and structures."

    def handle(self, *args, **options):
        # Build list of structures
        structures = Structure.objects.filter(
            kind__in=[
                'Chapter',
                'Quartet',
            ],
        )
        structure_pks = list(structures.values_list('id', flat=True))

        # Delete Orphans
        orphans = Organization.objects.filter(
            bhs_pk__isnull=False,
            kind=Organization.KIND.chapter,
        ).exclude(
            bhs_pk__in=structure_pks,
        )
        t = orphans.count()
        self.stdout.write("Deleting {0} orphans...".format(t))
        for orphan in orphans:
            log.error("Delete orphan: {0}".format(orphan))
            return
        # Creating/Update Organizations
        i = 0
        t = structures.count()
        for structure in structures:
            i += 1
            django_rq.enqueue(
                Organization.objects.update_or_create_from_structure,
                structure,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} structures...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} structures.".format(t))
