# Django
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to seed database."

    from api.factories import (
        InternationalFactory,
    )

    def handle(self, *args, **options):
        self.InternationalFactory()
