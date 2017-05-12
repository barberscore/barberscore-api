# Django
from django.core.management.base import BaseCommand

from api.factories import (
    AdminFactory,
)


class Command(BaseCommand):
    help = "Command to seed database."

    def handle(self, *args, **options):
        AdminFactory()
