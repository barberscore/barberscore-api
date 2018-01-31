
# Django
from django.core.management.base import (
    BaseCommand,
)

from api.models import (
    Person,
)

from api.tasks import (
    update_user_from_person,
)


class Command(BaseCommand):
    help = "Command to sync active persons with users."

    def handle(self, *args, **options):

        # Sync Persons
        self.stdout.write("Updating persons with users...")
        ps = Person.objects.filter(
            status__gt=0,
        ).exclude(
            email='',
        )
        for p in ps:
            update_user_from_person.delay(p)
        self.stdout.write("Complete")

