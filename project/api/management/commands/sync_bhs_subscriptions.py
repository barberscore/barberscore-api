
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Person
from api.tasks import update_bhs_subscription_from_person


class Command(BaseCommand):
    help = "Command to sync persons and humans."

    def handle(self, *args, **options):
        self.stdout.write("Updating persons and subscriptions...")
        persons = Person.objects.filter(
            bhs_pk__isnull=False,
        )
        for person in persons:
            update_bhs_subscription_from_person.delay(person)
        self.stdout.write("Complete")
