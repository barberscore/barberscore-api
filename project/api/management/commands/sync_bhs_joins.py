import logging
import django_rq
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Member
from bhs.models import SMJoin

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync bhs joins with members."

    def handle(self, *args, **options):
        # Get unique active joins
        js = SMJoin.objects.filter(
            structure__status__name='active',
            structure__kind__in=[
                'quartet',
                'chapter',
            ],
        ).order_by(
            'established_date',
            '-inactive_date',
        ).values_list(
            'id',
            'structure__id',
            'subscription__human__id',
            'status',
            'inactive_date',
            'inactive_reason',
            'membership__status__name',
            'membership__code',
            'vocal_part',
        )
        # Creating/Update Groups
        i = 0
        t = js.count()
        for j in js:
            i += 1
            django_rq.enqueue(
                Member.objects.update_or_create_from_join_objects,
                j,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} members...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} members.".format(t))
