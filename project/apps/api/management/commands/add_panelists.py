from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    add_judges,
)

from apps.api.models import (
    Contest,
)


class Command(BaseCommand):
    help = "Create sample contest."

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            nargs='+',
        )

    def handle(self, *args, **options):
        for slug in options['slug']:
            try:
                contest = Contest.objects.get(
                    slug=slug,
                )
            except Contest.DoesNotExist:
                raise CommandError("Award does not exist.")
            result = add_judges(contest)
            self.stdout.write("{0}".format(result))
