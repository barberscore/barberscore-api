from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    schedule_performances,
)

from apps.api.models import (
    Round,
)


class Command(BaseCommand):
    help = "Schedule performances for round."

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            nargs='+',
        )

    def handle(self, *args, **options):
        for slug in options['slug']:
            try:
                round = Round.objects.get(
                    slug=slug,
                )
            except Round.DoesNotExist:
                raise CommandError("Round does not exist.")
            result = schedule_performances(round)
            self.stdout.write("{0}".format(result))
