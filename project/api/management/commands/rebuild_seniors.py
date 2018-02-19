# Django
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command to rebuild seniors eligibility."

    def handle(self, *args, **options):
        Group = apps.get_model('api.group')

        quartets = Group.objects.filter(
            kind=Group.KIND.quartet,
            status__gt=0,
            bhs_pk__isnull=False,
        )

        for quartet in quartets:
            is_senior = quartet.get_is_senior()
            quartet.is_senior = is_senior
            quartet.save()

        return
