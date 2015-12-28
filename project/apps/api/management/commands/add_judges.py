from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    add_judges,
)

from apps.api.models import (
    Session,
)


class Command(BaseCommand):
    help = "Create judges."

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
        )

        parser.add_argument(
            'size',
            type=int,
        )

    def handle(self, *args, **options):
        try:
            session = Session.objects.get(
                slug=options['slug'],
            )
        except Session.DoesNotExist:
            raise CommandError("Session does not exist.")
        result = add_judges(session, options['size'])
        self.stdout.write("{0}".format(result))
