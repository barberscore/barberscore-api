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
        ss = Song.objects.all()
        for s in ss:
            s.save()
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        cs = Contestant.objects.all()
        for c in cs:
            c.save()
        rs = Ranking.objects.all()
        for r in rs:
            r.save()
        ss = Session.objects.all()
        for s in ss:
            s.save()
        cs = Contest.objects.all()
        for c in cs:
            c.save()
        ps = Panel.objects.all()
        for p in ps:
            p.save()
        cs = Convention.objects.all()
        for c in cs:
            c.save()
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
