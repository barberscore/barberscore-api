import django_rq

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Organization
from api.models import Enrollment
from api.models import Officer
from api.models import Office


class Command(BaseCommand):
    help = "Command to update all active chorus from chapter info."

    def handle(self, *args, **options):
        self.stdout.write("Updating...")

        # Build list of active, BHS choruses
        enrollments = Enrollment.objects.filter(
            organization__kind__in=[
                Organization.KIND.quartet,
            ]
        )

        # Creating/Update Groups
        i = 0
        t = enrollments.count()
        office = Office.objects.get(
            name='Quartet Manager',
        )
        for enrollment in enrollments:
            defaults = {
                'status': enrollment.status,
            }
            django_rq.enqueue(
                Officer.objects.update_or_create,
                person=enrollment.person,
                organization=enrollment.organization,
                office=office,
                defaults=defaults,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} officers...".format(i, t), ending='\r')
        self.stdout.write("Complete")
