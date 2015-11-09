from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Convention,
    Contest,
    Contestant,
    Performance,
    Song,
    Group,
    Singer,
    Director,
    Panelist,
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
        as_ = Performance.objects.all()
        for a in as_:
            a.save()
        ps = Song.objects.all()
        for p in ps:
            p.save()
        ss = Singer.objects.all()
        for s in ss:
            s.save()
        js = Panelist.objects.all()
        for j in js:
            j.save()
        ds = Director.objects.all()
        for d in ds:
            d.save()
        return "Done"
