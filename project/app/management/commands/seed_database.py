# Django
from django.apps import apps as api_apps
from django.core.management.base import BaseCommand


from app.factories import (
    InternationalFactory,
)


class Command(BaseCommand):
    help = "Command to seed database."

    def handle(self, *args, **options):
        InternationalFactory()
