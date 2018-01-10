# Django
from django.core.management.base import BaseCommand

from api.models import (
    Session,
)
from api.tasks import (
    create_actives_report,
)


class Command(BaseCommand):
    help = "Command to rebuild actives report."

    def handle(self, *args, **options):
        sessions = Session.objects.filter(
            is_archived=False,
            status__lt=Session.STATUS.closed,
        )
        for session in sessions:
            create_actives_report.delay(session)
        self.stdout.write("Rebuilt Session actives report")
        return
