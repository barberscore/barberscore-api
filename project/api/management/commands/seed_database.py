# Django
from django.core.management.base import BaseCommand


from api.factories import (
    InternationalFactory,
)


class Command(BaseCommand):
    help = "Command to seed database."

    def handle(self, *args, **options):
        InternationalFactory()
