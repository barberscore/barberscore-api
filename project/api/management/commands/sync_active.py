# Standard Libary
import datetime

# Django
from django.core.management.base import BaseCommand

from api.models import (
    Person,
)


class Command(BaseCommand):
    help = "Command to sync active status."

    def handle(self, *args, **options):
        # sync persons
        self.stdout.write("Updating active status...")
        today = datetime.date.today()
        ps = Person.objects.filter(
            status=10,
            valid_through__lt=today,
        )
        for p in ps:
            p.deactivate()
            p.save()
        self.stdout.write("Complete")
