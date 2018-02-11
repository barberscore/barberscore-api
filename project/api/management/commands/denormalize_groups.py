# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Group


class Command(BaseCommand):
    help = "Command to denormalize group ."

    def handle(self, *args, **options):
        gs = Group.objects.filter(
            status__in=[
                Group.STATUS.active,
                Group.STATUS.exempt,
            ],
        )
        i = 0
        t = gs.count()
        self.stdout.write("Updating groups...")
        for g in gs:
            i += 1
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
            try:
                parent = g.parent
            except Group.DoesNotExist:
                parent = None
            if not parent:
                g.international = ""
                g.district = ""
                g.division = ""
                g.chapter = ""
            else:
                international = parent
                if international.kind >= Group.KIND.international:
                    try:
                        while international.kind != Group.KIND.international:
                            international = international.parent
                        g.international = international.code
                    except AttributeError:
                        g.international = ""
                else:
                    g.international = ""
                district = parent
                if district.kind >= Group.KIND.district:
                    try:
                        while district.kind not in [
                            Group.KIND.district,
                            Group.KIND.noncomp,
                            Group.KIND.affiliate,
                        ]:
                            district = district.parent
                        g.district = district.code
                    except AttributeError:
                        g.district = ""
                else:
                    g.district = ""
                division = parent
                if division.kind >= Group.KIND.division:
                    try:
                        while division.kind != Group.KIND.division:
                            division = division.parent
                        g.division = division.name
                    except AttributeError:
                        g.division = ""
                else:
                    g.division = ""
                chapter = parent
                if chapter.kind >= Group.KIND.chapter:
                    try:
                        while chapter.kind != Group.KIND.chapter:
                            chapter = chapter.parent
                        g.chapter = chapter.name
                    except AttributeError:
                        g.chapter = ""
                else:
                    g.chapter = ""
            g.save()
        self.stdout.write("Updated {0} groups.".format(t))
