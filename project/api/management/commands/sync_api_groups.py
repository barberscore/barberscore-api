import django_rq

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Organization
from api.models import Group


class Command(BaseCommand):
    help = "Command to update all active chorus from chapter info."

    def handle(self, *args, **options):
        self.stdout.write("Updating...")

        # Build list of active, BHS choruses
        organizations = Organization.objects.filter(
            kind__in=[
                Organization.KIND.chorus,
                Organization.KIND.quartet,
            ]
        )

        # Creating/Update Groups
        i = 0
        t = organizations.count()
        for organization in organizations:
            defaults = {
                'name': organization.name,
                'status': organization.status,
                'kind': organization.kind,
                'code': organization.code,
                'start_date': organization.start_date,
                'end_date': organization.end_date,
                'location': organization.location,
                'website': organization.website,
                'facebook': organization.facebook,
                'twitter': organization.twitter,
                'email': organization.email,
                'phone': organization.phone,
                'description': organization.description,
                'notes': organization.notes,
                'mem_status': organization.mem_status,
                'bhs_id': organization.bhs_id,
                'bhs_pk': organization.bhs_pk,
            }
            django_rq.enqueue(
                Group.objects.update_or_create,
                organization=organization,
                defaults=defaults,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} groups...".format(i, t), ending='\r')
        self.stdout.write("Complete")
