import django_rq

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Person
from bhs.models import Human


class Command(BaseCommand):
    help = "Command to sync persons and humans."

    def handle(self, *args, **options):
        self.stdout.write("Getting list of humans...")
        # Build list of humans
        humans = Human.objects.all(
        ).values_list(
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'email',
            'birth_date',
            'phone',
            'cell_phone',
            'work_phone',
            'bhs_id',
            'sex',
            'primary_voice_part',
        )
        # # Delete Orphans
        # self.stdout.write("Deleting orphans...")
        # orphans = Person.objects.filter(
        #     bhs_pk__isnull=False,
        # ).exclude(
        #     bhs_pk__in=human_pks,
        # )
        # i = 0
        # t = orphans.count()
        # for orphan in orphans:
        #     i += 1
        #     self.stdout.flush()
        #     self.stdout.write("Deleting {0}/{1} orphans...".format(i, t), ending='\r')
        #     orphan.delete()
        # Creating/Update Persons
        self.stdout.write("Queuing person updates...")
        i = 0
        t = humans.count()
        for human in humans:
            django_rq.enqueue(
                Person.objects.update_or_create_from_human_object,
                human,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} persons...".format(i, t), ending='\r')
        self.stdout.write("Complete")
