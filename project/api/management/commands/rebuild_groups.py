# Django
from django.core.management.base import BaseCommand

from api.models import (
    Group,
)


class Command(BaseCommand):
    help = "Command to rebuild group parents."

    def handle(self, *args, **options):
        self.stdout.write("Updating groups...")
        gs = Group.objects.all()
        i = 0
        t = gs.count()
        for g in gs:
            i += 1
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
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
        self.stdout.write("Updated {0} groups.".format(t))
        return
