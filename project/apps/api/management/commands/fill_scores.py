from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    score_performance,
)

from apps.api.models import (
    Round,
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
                round = Round.objects.get(
                    slug=slug,
                )
            except Round.DoesNotExist:
                raise CommandError("Round does not exist.")
            performances = round.performances.filter(
                status=round.performances.model.STATUS.new,
            ).order_by('position')
            for performance in performances:
                performance.start()
                performance.save()
                score_performance(performance)
                performance.finish()
                performance.save()
            self.stdout.write("Filled Round")
