from django.db.models import Manager
from django.db.models import F
from django.apps import apps
import django_rq


class HumanManager(Manager):
    def update_persons(self, cursor=None, active_only=True):
        # Get base
        humans = self.all()
        # Filter if cursored
        if active_only:
            humans = humans.filter(
                is_deceased=False,
            )
        if cursor:
            humans = humans.filter(
                modified__gt=cursor,
            )
        # Return as objects
        humans = humans.values_list(
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

        # Creating/Update Persons
        Person = apps.get_model('api.person')
        for human in humans:
            django_rq.enqueue(
                Person.objects.update_or_create_from_human,
                human,
                is_object=True,
            )
        t = humans.count()
        return t

    def delete_orphans(self):
        # Get base
        humans = self.all()
        humans = list(humans.values_list('id', flat=True))
        # Delete Orphans
        Person = apps.get_model('api.person')
        orphans = Person.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=humans,
        )
        t = orphans.count()
        orphans.delete()
        return t


class StructureManager(Manager):
    def update_groups(self, cursor=None, active_only=True):
        # Get base
        structures = self.all()
        # Filter if cursored
        if active_only:
            structures = structures.filter(
                status__name='active',
            )
        if cursor:
            structures = structures.filter(
                modified__gt=cursor,
            )
        # Return as objects
        structures = structures.select_related(
            'status',
        ).values_list(
            'id',
            'name',
            'preferred_name',
            'chorus_name',
            'status__name',
            'kind',
            'established_date',
            'email',
            'phone',
            'website',
            'facebook',
            'twitter',
            'bhs_id',
            'parent__id',
            'chapter_code',
        )
        # Creating/Update Groups
        Group = apps.get_model('api.group')
        for structure in structures:
            django_rq.enqueue(
                Group.objects.update_or_create_from_structure,
                structure,
                is_object=True,
            )
        return structures.count()

    def delete_orphans(self):
        # Get base
        structures = self.all()
        structures = list(structures.values_list('id', flat=True))
        # Delete Orphans
        Group = apps.get_model('api.group')
        orphans = Group.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=structures,
        )
        t = orphans.count()
        orphans.delete()
        return t


class RoleManager(Manager):
    def update_officers(self, cursor=None):
        # Get the cursor
        Officer = apps.get_model('api.officer')

        # Get base, excluding Quartets
        roles = self.exclude(
            name='Quartet Admin',
        )
        # Will rebuild without a cursor
        if cursor:
            roles = roles.filter(
                created__gt=cursor,
            )
        # Order and Return as objects
        roles = roles.order_by(
            'created'
        ).values_list(
            'id',
            'name',
            'structure',
            'human',
            'start_date',
            'end_date',
        )

        # Creating/Update Officers
        Officer = apps.get_model('api.officer')
        for role in roles:
            django_rq.enqueue(
                Officer.objects.update_or_create_from_role,
                role,
                is_object=True,
            )
        return roles.count()


class JoinManager(Manager):
    def update_members(self, cursor=None):
        Member = apps.get_model('api.member')
        # Get base
        joins = self.select_related(
            'structure',
            'subscription',
            'subscription__human',
            'membership',
            'membership__status',
        )
        # Rebuild will do the whole thing.
        if cursor:
            joins = joins.filter(
                created__gt=cursor,
            )
        # Order and Return as objects
        joins = joins.order_by(
            F('inactive_date').asc(nulls_last=True),
            'created',
        ).values_list(
            'id',
            'structure__id',
            'subscription__human__id',
            'inactive_date',
            'inactive_reason',
            'vocal_part',
            'subscription__status',
            'subscription__current_through',
            'established_date',
            'membership__code',
            'membership__status__name',
        )

        # Creating/Update Persons
        Member = apps.get_model('api.member')
        for join in joins:
            django_rq.enqueue(
                Member.objects.create_from_join,
                join,
                is_object=True,
            )
        return joins.count()
