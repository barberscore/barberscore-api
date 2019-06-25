
# Standard Library
import datetime
import logging

# Django
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
# First-Party


from apps.bhs.models import Person
User = get_user_model()

class Command(BaseCommand):
    help = "Command to sync with BHS database."

    def handle(self, *args, **options):
        # L Persons
        users = User.objects.filter(
            is_staff=False,
            person__isnull=True,
        )
        self.stdout.write("Linking {0} Accounts.")
        for user in users:
            person = Person.objects.get(
                email=user.email,
            )
            person.user = user
            person.save()
        self.stdout.write("Complete.")
