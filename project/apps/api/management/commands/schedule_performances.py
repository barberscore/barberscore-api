from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    schedule_performances,
)

from apps.api.models import (
    Session,
)


class Command(BaseCommand):
    help = "Schedule performances for session."

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            nargs='+',
        )

    def handle(self, *args, **options):
        for slug in options['slug']:
            try:
                session = Session.objects.get(
                    slug=slug,
                )
            except Session.DoesNotExist:
                raise CommandError("Session does not exist.")
            result = schedule_performances(session)
            self.stdout.write("{0}".format(result))
