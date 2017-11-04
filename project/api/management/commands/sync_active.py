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
            current_through__lt=today,
        )
        total = ps.count()
        i = 0
        for p in ps:
            i += 1
            p.deactivate()
            p.save()
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} persons.".format(total))
        self.stdout.write("Complete")
