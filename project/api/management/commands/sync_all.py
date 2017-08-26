# Django
from django.core.management.base import BaseCommand

# First-Party
from bhs.updaters import crud_auth0


class Command(BaseCommand):
    help = "Command to sync database with Auth0."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Update all groups.',
        )

    def handle(self, *args, **options):
        # sync persons
        self.stdout.write("Updating persons...")
        if options['all']:
            hs = Human.objects.all()
        else:
            now = timezone.now()
            cursor = now - datetime.timedelta(hours=25)
            hs = Human.objects.filter(
                updated_ts__gt=cursor,
            )
        total = hs.count()
        i = 0
        for h in hs:
            i += 1
            update_or_create_person_from_human(h)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} persons.".format(total))
        # Sync Groups
        self.stdout.write("Updating groups...")
        if options['all']:
            ss = Structure.objects.all()
        else:
            now = timezone.now()
            cursor = now - datetime.timedelta(hours=25)
            ss = Structure.objects.filter(
                updated_ts__gt=cursor,
            )
        total = ss.count()
        i = 0
        for s in ss:
            i += 1
            update_or_create_group_from_structure(s)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} groups.".format(total))

        # Sync Members
        self.stdout.write("Updating members...")
        if options['all']:
            duplicates = SMJoin.objects.filter(
                structure__kind__in=[
                    'quartet',
                    'chapter',
                ],
            ).values(
                'structure__id',
                'subscription__human_id',
            ).order_by(
            ).annotate(
                count_id=Count('id')
            ).filter(count_id__gt=0)
        else:
            now = timezone.now()
            cursor = now - datetime.timedelta(hours=25)
            duplicates = SMJoin.objects.filter(
                structure__kind__in=[
                    'quartet',
                    'chapter',
                ],
                updated_ts__gt=cursor,
            ).values(
                'structure__id',
                'subscription__human_id',
            ).order_by(
            ).annotate(
                count_id=Count('id')
            ).filter(count_id__gt=0)

        i = 0
        total = duplicates.count()
        for d in duplicates:
            i += 1
            j = SMJoin.objects.filter(
                structure=d['structure__id'],
                subscription__human=d['subscription__human_id'],
            ).order_by(
                'status',
                'established_date',
            ).last()
            update_or_create_member_from_smjoin(j)
            self.stdout.write("{0}/{1}".format(i, total), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} members.".format(total))
        self.stdout.write("Complete")
