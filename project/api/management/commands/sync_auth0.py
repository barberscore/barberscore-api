# Django
from django.core.management.base import BaseCommand

# First-Party
from bhs.updaters import crud_auth0


class Command(BaseCommand):
    help = "Command to sync database with Auth0."

    def handle(self, *args, **options):
        return crud_auth0()
