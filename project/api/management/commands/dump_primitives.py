# Django
# Standard Libary
import json
from itertools import chain

from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

# First-Party
from api.models import (
    Award,
    Entity,
    Office,
)


class Command(BaseCommand):
    help = "Command to dump BHS primitives."

    def handle(self, *args, **options):
        eqs = Entity.objects.filter(
            kind__lt=30,
            status=Entity.STATUS.active,
        ).order_by(
            'kind',
            'name',
        )
        aqs = Award.objects.filter(
            status=Award.STATUS.active,
        )
        oqs = Office.objects.filter(
            status=Office.STATUS.active,
        )
        data = list(chain(eqs, aqs, oqs))
        json = serialize(
            'json',
            data,
            cls=DjangoJSONEncoder,
        )
        self.stdout.write(json)
