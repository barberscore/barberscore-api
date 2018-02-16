from django.core.management.base import BaseCommand

# First-Party
from api.models import Group


class Command(BaseCommand):
    help = "Sort the group tree hierarchy."

    def handle(self, *args, **options):
        self.stdout.write("Starting sort...")
        Group.objects.sort_tree()
        self.stdout.write("Complete.")
