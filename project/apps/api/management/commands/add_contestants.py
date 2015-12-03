from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    add_contestants,
)

from apps.api.models import (
    Panel,
)


class Command(BaseCommand):
    help = "Create sample panel."

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            type=str,
        )
        parser.add_argument(
            '--kind',
            type=int,
        )

        parser.add_argument(
            '--number',
            type=int,
        )

    def handle(self, *args, **options):
        try:
            panel = Panel.objects.get(
                slug=options['slug'],
            )
        except Panel.DoesNotExist:
            raise CommandError("Panel does not exist.")
        result = add_contestants(panel, options['number'])
        self.stdout.write("{0}".format(result))
