# Django
from django.core.management.base import BaseCommand

from api.models import (
    Group,
)


class Command(BaseCommand):
    help = "Command to rebuild group parents."

    def handle(self, *args, **options):
        gs = Group.objects.all()
        for g in gs:
            organization = g.organization
            while organization:
                if organization.kind == organization.KIND.international:
                    g.international = organization
                if organization.kind == organization.KIND.district:
                    g.district = organization
                if organization.kind == organization.KIND.division:
                    g.division = organization
                organization = organization.parent
            g.save()
