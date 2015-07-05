from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Convention,
    Contest,
    Contestant,
    Group,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        cs = Contestant.objects.all()
        for c in cs:
            c.save()
        ts = Contest.objects.all()
        for t in ts:
            t.save()
        vs = Convention.objects.all()
        for v in vs:
            v.save()
        gs = Group.objects.all()
        for g in gs:
            g.save()
        return "Done"
