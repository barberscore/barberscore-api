from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    add_competitors,
)

from apps.api.models import (
    Award,
)


class Command(BaseCommand):
    help = "Create sample contest."

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            type=str,
        )
        parser.add_argument(
            'number',
            type=int,
        )

    def handle(self, *args, **options):
        try:
            award = Award.objects.get(
                slug=options['slug'],
            )
        except Award.DoesNotExist:
            raise CommandError("Award does not exist.")
        result = add_competitors(award, options['number'])
        self.stdout.write("{0}".format(result))
