from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Performance,
    Contestant,
)


class Command(BaseCommand):
    help = "Command to denormailze data."

    def handle(self, *args, **options):
        ps = Performance.objects.all()
        for p in ps:
            p.save()
        cs = Contestant.objects.all()
        for c in cs:
            c.save()
        return "Done"
