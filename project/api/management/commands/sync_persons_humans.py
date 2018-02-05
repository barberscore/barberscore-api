import django_rq

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Person
from bhs.models import Human


class Command(BaseCommand):
    help = "Command to sync persons and humans."

    def handle(self, *args, **options):
        self.stdout.write("Updating persons and humans...")
        # Build list of humans
        humans = Human.objects.all()
        human_pks = list(humans.values_list('id', flat=True))
        # Delete Orphans
        self.stdout.write("Deleting orphans...")
        orphans = Person.objects.filter(
            bhs_pk__isnull=False,
        ).exclude(
            bhs_pk__in=human_pks,
        )
        for orphan in orphans:
            orphan.delete()
        # Creating/Update Persons
        self.stdout.write("Queuing person updates...")
        for human in humans:
            django_rq.enqueue(
                Person.objects.update_or_create_from_human,
                human,
            )
        self.stdout.write("Complete")
