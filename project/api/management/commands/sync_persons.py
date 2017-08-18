# Standard Libary
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from api.models import Person
from bhs.models import Human
from api.updaters import update_or_create_person_from_human

from email_validator import (
    validate_email,
    EmailNotValidError,
)

from django.db import (
    IntegrityError,
)
from django.utils import (
    encoding,
)

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def handle(self, *args, **options):
        self.stdout.write("Updating users...")
        hs = Human.objects.exclude(bhs_id=536190)
        total = hs.count()
        i = 0
        for h in hs:
            update_or_create_person_from_human(h)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
            i += 1
