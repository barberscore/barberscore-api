import django_rq
import logging

# Django
from django.core.management.base import BaseCommand
from django.db import IntegrityError
# First-Party
from api.models import Person
from api.models import User

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to update all active chorus from chapter info."

    def handle(self, *args, **options):
        self.stdout.write("Updating...")

        # Active Persons MUST have Users
        # UNLESS they don't have email
        persons = Person.objects.filter(
            status=Person.STATUS.active,
            user__isnull=True,
        ).exclude(
            email='',
        )
        for person in persons:
            try:
                user = User.objects.create(
                    status=User.STATUS.active,
                    name=person.nomen,
                    email=person.email,
                )
            except IntegrityError as e:
                person.status = Person.STATUS.new
                person.save()
                log.error("{0} {1}".format(e, person))
                continue
            person.user = user
            person.save()

        # Activate Users where needed
        persons = Person.objects.filter(
            status=Person.STATUS.active,
            user__isnull=False,
        ).exclude(
            user__status=User.STATUS.active,
        )
        for person in persons:
            person.user.status = person.user.STATUS.active
            person.user.save()

        # Deactivate Users where needed
        persons = Person.objects.filter(
            status=Person.STATUS.inactive,
            user__isnull=False,
        ).exclude(
            user__status=User.STATUS.inactive,
        )
        for person in persons:
            person.user.status = person.user.STATUS.inactive
            person.user.save()
        self.stdout.write("Complete")
