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
                g.international = ""
                g.district = ""
                g.division = ""
                g.chapter = ""
            else:
                international = organization
                if international.kind >= Organization.KIND.international:
                    try:
                        while international.kind != Organization.KIND.international:
                            international = international.parent
                        g.international = international.code
                    except AttributeError:
                        g.international = ""
                else:
                    g.international = ""
                district = organization
                if district.kind >= Organization.KIND.district:
                    try:
                        while district.kind != Organization.KIND.district:
                            district = district.parent
                        g.district = district.code
                    except AttributeError:
                        g.district = ""
                else:
                    g.district = ""
                division = organization
                if division.kind >= Organization.KIND.division:
                    try:
                        while division.kind != Organization.KIND.division:
                            division = division.parent
                        g.division = division.name
                    except AttributeError:
                        g.division = ""
                else:
                    g.division = ""
                chapter = organization
                if chapter.kind >= Organization.KIND.chapter:
                    try:
                        while chapter.kind != Organization.KIND.chapter:
                            chapter = chapter.parent
                        g.chapter = chapter.name
                    except AttributeError:
                        g.chapter = ""
                else:
                    g.chapter = ""
            g.save()
        self.stdout.write("Updated {0} groups.".format(t))
