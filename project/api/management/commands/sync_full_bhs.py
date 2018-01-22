
# Django
from django.core.management.base import (
    BaseCommand,
)

from api.models import (
    Person,
    Group,
    # Enrollment,
    Member,
    Organization,
)

from bhs.models import (
    Human,
    SMJoin,
    Structure,
)


class Command(BaseCommand):
    help = "Command to sync with BHS database."

    def handle(self, *args, **options):

        # Sync Persons
        self.stdout.write("Updating persons...")
        hs = Human.objects.all()
        i = 0
        t = hs.count()
        for h in hs:
            i += 1
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
            Person.objects.update_or_create_from_human(h)
        self.stdout.write("Updated {0} persons.".format(t))

        # Sync BHS Status and Current Through
        self.stdout.write("Updating BHS status...")
        js = SMJoin.objects.filter(
            status=True,
            structure__kind='organization',
            subscription__items_editable=True,
        ).order_by('updated_ts')
        i = 0
        t = js.count()
        for j in js:
            i += 1
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
            Person.objects.update_from_join(j)
        self.stdout.write("Updated {0} statuses.".format(t))

        # Sync Organizations
        self.stdout.write("Updating organizations...")
        ss = Structure.objects.filter(
            kind__in=[
                'organization',
                'district',
                'chapter',
            ],
        )
        i = 0
        t = ss.count()
        for s in ss:
            i += 1
            Organization.objects.update_or_create_from_structure(s)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} organizations.".format(t))

        # Sync Groups
        self.stdout.write("Updating groups...")
        ss = Structure.objects.filter(
            kind__in=[
                'quartet',
                'chapter',
            ],
        )
        i = 0
        t = ss.count()
        for s in ss:
            i += 1
            Group.objects.update_or_create_from_structure(s)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} groups.".format(t))

        # Sync Members
        self.stdout.write("Updating memberships...")
        js = SMJoin.objects.filter(
            status=True,
            structure__kind__in=[
                'quartet',
                'chapter',
            ],
        ).order_by('updated_ts')
        i = 0
        t = js.count()
        for j in js:
            i += 1
            Member.objects.update_or_create_from_join(j)
            self.stdout.write("{0}/{1}".format(i, t), ending='\r')
            self.stdout.flush()
        self.stdout.write("Updated {0} memberships.".format(t))

        # Sync Enrollments - Very Slow!
        self.stdout.write("Skipping enrollments...")
        # self.stdout.write("Updating enrollments...")
        # js = SMJoin.objects.filter(
        #     status=True,
        #     subscription__items_editable=True,
        # ).order_by('updated_ts')
        # i = 0
        # t = js.count()
        # for j in js:
        #     i += 1
        #     Enrollment.objects.update_or_create_from_join(j)
        #     self.stdout.write("{0}/{1}".format(i, t), ending='\r')
        #     self.stdout.flush()
        # self.stdout.write("Updated {0} enrollments.".format(t))

        self.stdout.write("Complete.")
