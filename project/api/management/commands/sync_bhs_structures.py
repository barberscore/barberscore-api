import django_rq
import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Group
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
        ).values_list(
            'id',
            'name',
            'preferred_name',
            'chorus_name',
            'status__name',
            'kind',
            'established_date',
            'email',
            'phone',
            'website',
            'facebook',
            'twitter',
            'bhs_id',
            'parent',
        )
        # # Delete Orphans
        # orphans = Group.objects.filter(
        #     bhs_pk__isnull=False,
        #     kind=Group.KIND.chapter,
        # ).exclude(
        #     bhs_pk__in=structure_pks,
        # )
        # t = orphans.count()
        # self.stdout.write("Deleting {0} orphans...".format(t))
        # for orphan in orphans:
        #     log.error("Delete orphan: {0}".format(orphan))
        #     return
        # Creating/Update Groups
        i = 0
        t = structures.count()
        for structure in structures:
            i += 1
            django_rq.enqueue(
                Group.objects.update_or_create_from_structure_object,
                structure,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} structures...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} structures.".format(t))
