from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    add_panelists,
)

from apps.api.models import (
    Panel,
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
                panel = Panel.objects.get(
                    slug=slug,
                )
            except Panel.DoesNotExist:
                raise CommandError("Contest does not exist.")
            result = add_panelists(panel)
            self.stdout.write("{0}".format(result))
