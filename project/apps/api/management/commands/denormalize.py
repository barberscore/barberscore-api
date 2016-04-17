from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Award,
    Convention,
    Performer,
    Performance,
    Song,
    Group,
    # Judge,
    Contestant,
    Contest,
    Round,
    Session,
    Score,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        ws = Award.objects.all()
        for w in ws:
            w.save()
        cs = Convention.objects.all()
        for c in cs:
            c.save()
        ps = Session.objects.all()
        for p in ps:
            p.save()
        ss = Round.objects.all()
        for s in ss:
            s.save()
        gs = Group.objects.all()
        for g in gs:
            g.save()
        cs = Performer.objects.all()
        for c in cs:
            c.save()
        rs = Contest.objects.all()
        for r in rs:
            r.save()
        rs = Contestant.objects.all()
        for r in rs:
            r.save()
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        ss = Song.objects.all()
        for s in ss:
            s.save()
        zs = Score.objects.all()
        for s in zs:
            s.save()
        # ss = Singer.objects.all()
        # for s in ss:
        #     s.save()
        # js = Judge.objects.all()
        # for j in js:
        #     j.save()
        # ds = Director.objects.all()
        # for d in ds:
        #     d.save()
        return "Done"
