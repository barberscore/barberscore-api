# Django
from django.core.management.base import BaseCommand


from api.models import (
    User,
)


class Command(BaseCommand):
    help = "Command to seed database."

    def handle(self, *args, **options):
        User.objects.create_superuser(
            'test@barberscore.com',
            'password',
        )
