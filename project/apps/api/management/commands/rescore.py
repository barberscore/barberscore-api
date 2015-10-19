from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Contestant,
    Appearance,
    Performance,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        as_ = Appearance.objects.all()
        for a in as_:
            a.save()
        cs = Contestant.objects.all()
        for c in cs:
            c.save()
        return "Done"
