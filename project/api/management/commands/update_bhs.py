# Standard Libary
import datetime
import logging
import django_rq

# Django
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils import timezone

# First-Party
from api.models import Member
from api.models import Officer
from api.models import User
from api.models import Group
from api.models import Person
from bhs.models import Human
from bhs.models import SMJoin
# from bhs.models import Role
from bhs.models import Structure
from bhs.models import Subscription

from api.tasks import update_or_create_account_from_user

log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Command to sync with BHS database."

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
            raise CommandError('No argument specified.')

        # Sync Persons
        humans = Human.objects.filter(
            updated_ts__gt=cursor,
        )
        i = 0
        t = humans.count()
        for human in humans:
            i += 1
            django_rq.enqueue(
                Person.objects.update_or_create_from_human,
                human,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} persons...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} persons.".format(t))

        # Sync Subsciptions
        subscriptions = Subscription.objects.filter(
            items_editable=True,
            updated_ts__gt=cursor,
        ).order_by('created_ts')
        i = 0
        t = subscriptions.count()
        for subscription in subscriptions:
            i += 1
            django_rq.enqueue(
                Person.objects.update_status_from_subscription,
                subscription,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} subscriptions...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} subscriptions.".format(t))

        # Sync Groups
        structures = Structure.objects.filter(
            updated_ts__gt=cursor,
        )
        i = 0
        t = structures.count()
        for structure in structures:
            i += 1
            django_rq.enqueue(
                Group.objects.update_or_create_from_structure,
                structure,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} groups...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} groups.".format(t))

        # Sync Members
        joins = SMJoin.objects.filter(
            structure__kind__in=[
                'chapter',
                'quartet',
            ],
            updated_ts__gt=cursor,
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
        i = 0
        t = joins.count()
        for join in joins:
            i += 1
            django_rq.enqueue(
                Member.objects.update_or_create_from_join_object,
                join,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} members...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} members.".format(t))
        self.stdout.write("Complete.")

        # Sync Users
        persons = Person.objects.filter(
            modified__lt=cursor,
        ).exclude(
            email='',
        )
        i = 0
        t = persons.count()
        for person in persons:
            i += 1
            django_rq.enqueue(
                User.objects.update_or_create_from_person,
                person,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} persons...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} persons.".format(t))

        # Sync Accounts
        users = User.objects.filter(
            modified__lt=cursor,
        )
        i = 0
        t = users.count()
        for user in users:
            i += 1
            update_or_create_account_from_user.delay(user)
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} users...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} users.".format(t))

        # Sync Roles
        # TODO this is waiting for an updated TS
        # roles = Role.objects.filter(
        #     updated_ts__gt=cursor,
        # ).exclude(
        #     name='Quartet Admin',
        # )
        # # Creating/Update Groups
        # self.stdout.write("Queuing officer updates...")
        # for role in roles:
        #     django_rq.enqueue(
        #         Officer.objects.update_or_create_from_role,
        #         role,
        #     )

        # Quartet Admins Update
        members = Member.objects.filter(
            group__kind=Group.KIND.quartet,
            modified__gt=cursor,
        )
        i = 0
        t = members.count()
        for member in members:
            django_rq.enqueue(
                Officer.objects.update_or_create_from_member,
                member,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} quartet officers...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} officers.".format(t))

        self.stdout.write("Complete.")
