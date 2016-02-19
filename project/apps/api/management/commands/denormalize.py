from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Convention,
    Performer,
    Performance,
    Song,
    # Singer,
    # Director,
    # Judge,
    Contestant,
    Round,
    Session,
    Score,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        zs = Score.objects.all()
        for s in zs:
            s.save()
        ss = Song.objects.all()
        for s in ss:
            s.save()
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        cs = Performer.objects.all()
        for c in cs:
            c.save()
        rs = Contestant.objects.all()
        for r in rs:
            r.save()
        ss = Round.objects.all()
        for s in ss:
            s.save()
        ps = Session.objects.all()
        for p in ps:
            p.save()
        cs = Convention.objects.all()
        for c in cs:
            c.save()
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
