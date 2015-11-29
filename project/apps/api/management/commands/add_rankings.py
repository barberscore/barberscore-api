from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    add_rankings,
)

from apps.api.models import (
    Award,
)


class Command(BaseCommand):
    help = "Create sample panel."

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
            raise CommandError("Contest does not exist.")
        result = add_rankings(award, options['number'])
        self.stdout.write("{0}".format(result))
