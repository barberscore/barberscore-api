from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Convention,
    Award,
    Contestant,
    Performance,
    Song,
    # Singer,
    # Director,
    # Judge,
    Competitor,
    Round,
    Contest,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        ss = Song.objects.all()
        for s in ss:
            s.save()
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        cs = Contestant.objects.all()
        for c in cs:
            c.save()
        rs = Competitor.objects.all()
        for r in rs:
            r.save()
        ss = Round.objects.all()
        for s in ss:
            s.save()
        cs = Award.objects.all()
        for c in cs:
            c.save()
        ps = Contest.objects.all()
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
