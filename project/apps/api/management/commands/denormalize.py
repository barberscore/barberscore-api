from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Convention,
    Contest,
    Contestant,
    Performance,
    Group,
    Person,
    Singer,
    Director,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        vs = Convention.objects.all()
        for v in vs:
            v.save()
        ts = Contest.objects.all()
        for t in ts:
            t.save()
        cs = Contestant.objects.all()
        for c in cs:
            c.save()
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        gs = Group.objects.all()
        for g in gs:
            g.save()
        rs = Person.objects.all()
        for r in rs:
            r.save()
        ss = Singer.objects.all()
        for s in ss:
            s.save()
        ds = Director.objects.all()
        for d in ds:
            d.save()
        return "Done"
