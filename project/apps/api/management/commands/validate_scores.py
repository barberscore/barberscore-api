from django.core.management.base import (
    BaseCommand,
    CommandError,
)

# from apps.api.factories import (
#     score_performance,
# )

from apps.api.models import (
    Round,
    Score,
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
                round = Round.objects.get(
                    slug=slug,
                )
            except Round.DoesNotExist:
                raise CommandError("Round does not exist.")
            scores = Score.objects.filter(
                song__performance__round=round,
                status=Score.STATUS.flagged,
            )
            for score in scores:
                score.validate()
                score.save()
            self.stdout.write("Validated Scores")
