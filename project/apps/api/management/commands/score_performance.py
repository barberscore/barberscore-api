from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    score_performance,
)

from apps.api.models import (
    Performance,
)


class Command(BaseCommand):
    help = "Score performance."

    def add_arguments(self, parser):
        parser.add_argument(
            'id',
            nargs='+',
        )

    def handle(self, *args, **options):
        for id in options['id']:
            try:
                performance = Performance.objects.get(
                    pk=id,
                )
            except Performance.DoesNotExist:
                raise CommandError("Performance does not exist.")
            result = score_performance(performance)
            self.stdout.write("{0}".format(result))
