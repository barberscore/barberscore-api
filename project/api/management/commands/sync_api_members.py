import django_rq

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Organization
from api.models import Enrollment
from api.models import Member


class Command(BaseCommand):
    help = "Command to update all active chorus from chapter info."

    def handle(self, *args, **options):
        self.stdout.write("Updating...")

        # Build list of active, BHS choruses
        enrollments = Enrollment.objects.filter(
            organization__kind__in=[
                Organization.KIND.chorus,
                Organization.KIND.quartet,
            ]
        )

        # Creating/Update Groups
        i = 0
        t = enrollments.count()
        for enrollment in enrollments:
            defaults = {
                'status': enrollment.status,
                'bhs_pk': enrollment.bhs_pk,
            }
            group = enrollment.organization.groups.get(
                status__gt=0,
            )
            django_rq.enqueue(
                Member.objects.update_or_create,
                person=enrollment.person,
                group=group,
                defaults=defaults,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} enrollments...".format(i, t), ending='\r')
        self.stdout.write("Complete")
