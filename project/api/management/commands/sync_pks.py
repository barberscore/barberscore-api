# Django
from django.core.management.base import (
    BaseCommand,
)

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from api.models import (
    Person,
)

from bhs.models import (
    Human,
)


class Command(BaseCommand):
    help = "Command to sync BHS PKs."

    def handle(self, *args, **options):
        # Sync Persons
        self.stdout.write("Updating from email...")
        # Instantiate list
        es = []
        hs = Human.objects.all()
        for h in hs:
            try:
                # Validate the email
                validate_email(h.email)
                es.append(h.email)
            except ValidationError:
                # Create barberscore email otherwise
                es.append("{0}@barberscore.com".format(h.bhs_id))
        # find persons who lack PK but match email
        ps = Person.objects.filter(
            bhs_pk=None,
            email__in=es,
        )
        i = 0
        t = ps.count()
        # Update these.
        for p in ps:
            i += 1
            h = Human.objects.get(
                email=p.email,
            )
            p.bhs_pk = str(h.id)
            p.save()
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} persons from email.".format(t))

        # Repeat process for BHS IDs.
        self.stdout.write("Updating from BHS ID...")
        bs = []
        hs = Human.objects.all()
        for h in hs:
            bs.append(h.bhs_id)
        ps = Person.objects.filter(
            bhs_pk=None,
            bhs_id__in=bs,
        )
        i = 0
        t = ps.count()
        for p in ps:
            i += 1
            h = Human.objects.get(
                bhs_id=p.bhs_id,
            )
            p.bhs_pk = str(h.id)
            p.save()
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} persons from BHS ID.".format(t))

        self.stdout.write("Complete.")
