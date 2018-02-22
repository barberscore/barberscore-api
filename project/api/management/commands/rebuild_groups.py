# Django
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to rebuild denorms."

    def handle(self, *args, **options):
        Group = apps.get_model('api.group')
        Group.objects.denormalize()
        return
