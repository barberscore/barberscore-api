# Django
from django.apps import apps as api_apps
from django.core.management.base import BaseCommand


from app.models import (
    User,
)


class Command(BaseCommand):
    help = "Command to seed database."

    def handle(self, *args, **options):
        User.objects.create_superuser(
            'admin@barberscore.com',
            'password',
        )
