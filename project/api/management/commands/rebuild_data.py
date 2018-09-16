

# Standard Library
import datetime

# Django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Command to rebuild denorms."

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            dest='days',
            nargs='?',
            const=1,
            help='Number of days to update.',
        )

        parser.add_argument(
            '--hours',
            type=int,
            dest='hours',
            nargs='?',
            const=1,
            help='Number of hours to update.',
        )

        parser.add_argument(
            '--minutes',
            type=int,
            dest='minutes',
            nargs='?',
            const=1,
            help='Number of hours to update.',
        )

    def handle(self, *args, **options):
        # Set Cursor
        if options['days']:
            cursor = timezone.now() - datetime.timedelta(days=options['days'], hours=1)
        elif options['hours']:
            cursor = timezone.now() - datetime.timedelta(hours=options['hours'], minutes=5)
        elif options['minutes']:
            cursor = timezone.now() - datetime.timedelta(minutes=options['minutes'], seconds=5)
        else:
            cursor = None
        Group = apps.get_model('api.group')
        Group.objects.denormalize(cursor=cursor)
        Group.objects.sort_tree()
        Group.objects.update_seniors()
        Award = apps.get_model('api.award')
        Award.objects.sort_tree()
        return
