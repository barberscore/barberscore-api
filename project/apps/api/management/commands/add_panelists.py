from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    impanel_panelists,
)

from apps.api.models import (
    Contest,
)


class Command(BaseCommand):
    help = "Create sample panel."

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
                raise CommandError("Contest does not exist.")
            result = impanel_panelists(contest)
            self.stdout.write("{0}".format(result))
