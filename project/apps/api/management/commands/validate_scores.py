from django.core.management.base import (
    BaseCommand,
    CommandError,
)

# from apps.api.factories import (
#     score_performance,
# )

from apps.api.models import (
    Session,
    Score,
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
                session = Session.objects.get(
                    slug=slug,
                )
            except Session.DoesNotExist:
                raise CommandError("Session does not exist.")
            scores = Score.objects.filter(
                song__performance__session=session,
                status=Score.STATUS.flagged,
            )
            for score in scores:
                score.validate()
                score.save()
            self.stdout.write("Validated Scores")
