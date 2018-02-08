import logging
import django_rq
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Enrollment
from bhs.models import SMJoin

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync quartets and structures."

    def handle(self, *args, **options):
        # Get unique active joins for Chapters
        join_pks = SMJoin.objects.filter(
            inactive_date=None,
            structure__kind__in=[
                'Chapter',
                'Quartet',
            ],
        ).values_list(
            'id',
            'subscription__human',
            'structure',
        )
        # Creating/Update Groups
        i = 0
        t = len(join_pks)
        for join_pk in join_pks:
            i += 1
            django_rq.enqueue(
                Enrollment.objects.update_or_create_from_join_pks,
                join_pk,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} enrollments...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} enrollments.".format(t))
