import logging

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Group
from api.tasks import update_or_create_quartet_membership_from_join
from bhs.models import Structure

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        self.stdout.write("Updating quartet memberships...")

        # Build list of structures
        quartets = Group.objects.filter(
            kind='Quartet',
            bhs_pk__isnull=False,
        )
        # Delete Orphans
        # Creating/Update Groups
        self.stdout.write("Queuing membership updates...")
        for quartet in quartets:

            structure = Structure.objects.get(id=quartet.bhs_pk)

            js = structure.smjoins.values(
                'subscription__human',
                'structure',
            ).distinct()

            for j in js:
                m = structure.smjoins.filter(
                    subscription__human__id=j['subscription__human'],
                    structure__id=j['structure'],
                ).latest('established_date', 'updated_ts')
                update_or_create_quartet_membership_from_join.delay(m)
        self.stdout.write("Complete")
