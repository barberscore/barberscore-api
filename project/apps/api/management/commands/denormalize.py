from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Convention,
    Contest,
    Contestant,
    Performance,
    Song,
    # Singer,
    # Director,
    # Panelist,
    Ranking,
    Session,
    Panel,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        ps = Song.objects.all()
        for p in ps:
            p.save()
        as_ = Performance.objects.all()
        for a in as_:
            a.save()
        cs = Contestant.objects.all()
        for c in cs:
            c.save()
        rs = Ranking.objects.all()
        for r in rs:
            r.save()
        ss = Session.objects.all()
        for s in ss:
            s.save()
        ts = Contest.objects.all()
        for t in ts:
            t.save()
        ps = Panel.objects.all()
        for p in ps:
            p.save()
        vs = Convention.objects.all()
        for v in vs:
            v.save()
        # ss = Singer.objects.all()
        # for s in ss:
        #     s.save()
        # js = Panelist.objects.all()
        # for j in js:
        #     j.save()
        # ds = Director.objects.all()
        # for d in ds:
        #     d.save()
        return "Done"
