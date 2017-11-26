# Django
from django.core.management.base import (
    BaseCommand,
)

from api.models import (
    Group,
    Organization,
)


class Command(BaseCommand):
    help = "Command to denormalize group organizations."

    def handle(self, *args, **options):
        gs = Group.objects.filter(
            status=Group.STATUS.active,
        )
        i = 0
        t = gs.count()
        self.stdout.write("Updating groups...")
        for g in gs:
            i += 1
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
            try:
                organization = g.organization
            except Organization.DoesNotExist:
                organization = None
            if not organization:
                international = ""
                district = ""
                division = ""
                chapter = ""
            else:
                try:
                    international = Organization.objects.get(
                        children=organization,
                        kind=Organization.KIND.international,
                    ).code
                except Organization.DoesNotExist:
                    international = ""
                try:
                    district = Organization.objects.get(
                        children=organization,
                        kind=Organization.KIND.district,
                    ).code
                except Organization.DoesNotExist:
                    district = ""
                try:
                    division = Organization.objects.get(
                        children=organization,
                        kind=Organization.KIND.division,
                    ).name
                except Organization.DoesNotExist:
                    division = ""
                try:
                    chapter = Organization.objects.get(
                        children=organization,
                        kind=Organization.KIND.chapter,
                    ).name
                except Organization.DoesNotExist:
                    chapter = ""
            g.international = international
            g.district = district
            g.division = division
            g.chapter = chapter
            g.save()
        self.stdout.write("Updated {0} groups.".format(t))
