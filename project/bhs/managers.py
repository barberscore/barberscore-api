from django.db.models import Manager
from django.apps import apps
import django_rq


class HumanManager(Manager):
    def update_persons(self, cursor=None, active_only=True, *args, **kwargs):
        # Get base
        humans = self.all()
        # Filter if cursored
        if active_only:
            humans = humans.filter(
                is_deceased=False,
            )
        if cursor:
            humans = humans.filter(
                updated_ts__gt=cursor,
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
                Person.objects.update_or_create_from_human_object,
                human,
            )
        return

    def delete_orphans(self, *args, **kwargs):
        # Get base
        humans = self.all()
        humans = list(humans.values_list('id', flat=True))
        # Delete Orphans
        Person = apps.get_model('api.person')
        orphans = Person.objects.filter(
            bhs_pk__isnull=False,
        ).exclude(
            bhs_pk__in=humans,
        )
        for orphan in orphans:
            print(orphan)
            return


class StructureManager(Manager):
    def update_groups(self, cursor=None, active_only=True, *args, **kwargs):
        # Get base
        structures = self.all()
        # Filter if cursored
        if active_only:
            structures = structures.filter(
                status__name='active',
            )
        if cursor:
            structures = structures.filter(
                updated_ts__gt=cursor,
            )
        # Return as objects
        structures = structures.values_list(
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
            'parent',
        )
        # Creating/Update Groups
        Group = apps.get_model('api.group')
        for structure in structures:
            django_rq.enqueue(
                Group.objects.update_or_create_from_structure_object,
                structure,
            )
        return

    def delete_orphans(self, *args, **kwargs):
        # Get base
        structures = self.all()
        structures = list(structures.values_list('id', flat=True))
        # Delete Orphans
        Group = apps.get_model('api.group')
        orphans = Group.objects.filter(
            bhs_pk__isnull=False,
        ).exclude(
            bhs_pk__in=structures,
        )
        for orphan in orphans:
            print(orphan)
            return


class SubscriptionManager(Manager):
    def update_persons(self, cursor=None, *args, **kwargs):
        # Get base
        subscriptions = self.filter(
            items_editable=True,
        )
        # Filter if cursored
        if cursor:
            subscriptions = subscriptions.filter(
                updated_ts__gt=cursor,
            )
        # Order and Return as objects
        subscriptions = subscriptions.order_by(
            'created_ts',
        ).values_list(
            'human__id',
            'items_editable',
            'status',
            'current_through',
        )

        # Creating/Update Persons
        Person = apps.get_model('api.person')
        for subscription in subscriptions:
            django_rq.enqueue(
                Person.objects.update_status_from_subscription_object,
                subscription,
            )
        return


class RoleManager(Manager):
    def update_chapter_officers(self, cursor=None, active_only=True, *args, **kwargs):
        # Get base
        roles = self.exclude(
            name='Quartet Admin',
        )
        if active_only:
            roles = roles.filter(
                structure__status__name='active',
            )
        # Filter if cursored
        if cursor:
            raise RuntimeError("Not currently supported")
            roles = roles.filter(
                updated_ts__gt=cursor,
            )
        # Order and Return as objects
        roles = roles.order_by(
            'start_date'
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
                Officer.objects.update_or_create_from_role_object,
                role,
            )
        return


class SMJoinManager(Manager):
    def update_members(self, cursor=None, *args, **kwargs):
        # Get base
        joins = self.filter(
            structure__kind__in=[
                'quartet',
                'chapter',
            ],
        )
        # Filter if cursored
        if cursor:
            joins = joins.filter(
                updated_ts__gt=cursor,
            )
        # Order and Return as objects
        joins = joins.order_by(
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

        # Creating/Update Persons
        Member = apps.get_model('api.member')
        for join in joins:
            django_rq.enqueue(
                Member.objects.update_or_create_from_join_object,
                join,
            )
        return

    def update_quartet_officers(self, cursor=None, active_only=True, *args, **kwargs):
        # Get base
        joins = self.filter(
            structure__kind='quartet',
        )
        # Filter if cursored
        if active_only:
            joins = joins.filter(
                structure__status__name='active',
            )
        # Filter if cursored
        if cursor:
            joins = joins.filter(
                updated_ts__gt=cursor,
            )
        # Order and Return as objects
        joins = joins.order_by(
            'established_date',
            '-inactive_date',
        ).values_list(
            'id',
            'status',
            'structure',
            'human',
        )

        # Creating/Update Officers
        Officer = apps.get_model('api.officer')
        for join in joins:
            django_rq.enqueue(
                Officer.objects.update_or_create_from_join_object,
                join,
            )
        return
