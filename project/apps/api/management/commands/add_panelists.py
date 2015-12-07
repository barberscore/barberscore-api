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
    help = "Create sample session."

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
                raise CommandError("Contest does not exist.")
            result = add_judges(session)
            self.stdout.write("{0}".format(result))
