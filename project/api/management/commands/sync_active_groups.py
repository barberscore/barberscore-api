
# Django
from django.core.management.base import (
    BaseCommand,
)

from api.models import (
    Group,
)

from api.tasks import (
    update_group_from_bhs,
)


class Command(BaseCommand):
    help = "Command to sync active groups with BHS database."

    def handle(self, *args, **options):

        # Sync Persons
        self.stdout.write("Updating active groups...")
        gs = Group.objects.filter(
            status=Group.STATUS.active,
        )
        for g in gs:
            update_group_from_bhs.delay(g)
        self.stdout.write("Complete")
