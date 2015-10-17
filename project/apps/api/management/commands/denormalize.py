from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Convention,
    Contest,
    Contestant,
    Appearance,
    Performance,
    Group,
    Singer,
    Director,
    Judge,
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
        as_ = Appearance.objects.all()
        for a in as_:
            a.save()
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        ss = Singer.objects.all()
        for s in ss:
            s.save()
        js = Judge.objects.all()
        for j in js:
            j.save()
        ds = Director.objects.all()
        for d in ds:
            d.save()
        return "Done"
