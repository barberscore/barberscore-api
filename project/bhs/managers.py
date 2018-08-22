from django.db.models import Manager
from django.apps import apps
from django_fsm_log.models import StateLog
import django_rq
from django.db.models import Q
from django.utils.timezone import localdate

class HumanManager(Manager):
    def update_persons(self, cursor=None):
        # Get base
        humans = self.all()
        # Filter if cursored
        if cursor:
            humans = self.filter(
                modified__gt=cursor,
            )
        t = humans.count()
        # Creating/Update Persons
        Person = apps.get_model('api.person')
        for human in humans:
            django_rq.enqueue(
                Person.objects.update_or_create_from_human,
                human,
            )
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
    def update_groups(self, cursor=None):
        # Get base
        structures = self.select_related('parent').all()
        if cursor:
            # Filter if cursored
            structures = structures.filter(
                modified__gt=cursor,
            )
        else:
            # Else clear logs
            ss = StateLog.objects.filter(
                content_type__model='group',
                groups__mc_pk__isnull=False,
            )
            ss.delete()
        t = structures.count()
        # Creating/Update Groups
        Group = apps.get_model('api.group')
        for structure in structures:
            django_rq.enqueue(
                Group.objects.update_or_create_from_structure,
                structure,
            )
        return t

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
        # Get base
        roles = self.select_related(
            'structure',
            'human',
        ).order_by(
            'modified',
            'created',
        )
        # Will rebuild without a cursor
        if cursor:
            roles = roles.filter(
                modified__gt=cursor,
            )
        else:
            # Else clear logs
            ss = StateLog.objects.filter(
                content_type__model='officer',
                officers__mc_pk__isnull=False,
            )
            ss.delete()
        t = roles.count()
        # Creating/Update Officers
        Officer = apps.get_model('api.officer')
        for role in roles:
            django_rq.enqueue(
                Officer.objects.update_from_role,
                role,
            )
        return t


class JoinManager(Manager):
    def update_members(self, cursor=None):
        Member = apps.get_model('api.member')
        # Get base
        joins = self.select_related(
            'structure',
            'subscription',
            'subscription__human',
        ).order_by(
            'modified',
            '-inactive_date',
        )
        if cursor:
            joins = joins.filter(
                modified__gt=cursor,
            )
        else:
            # Else clear logs
            ss = StateLog.objects.filter(
                content_type__model='member',
                members__mc_pk__isnull=False,
            )
            ss.delete()

        t = joins.count()
        # Creating/Update Membership
        for join in joins:
            Member.objects.update_from_join(join)
            # django_rq.enqueue(
            #     Member.objects.update_from_join,
            #     join,
            # )
        return t

    # def update_members(self, cursor=None):
    #     Member = apps.get_model('api.member')
    #     # Get base
    #     joins = self.select_related(
    #         'structure',
    #         'subscription__human',
    #     ).exclude(paid=0)
    #     if cursor:
    #         joins = joins.filter(
    #             modified__gt=cursor,
    #         )
    #     # Return unique rows
    #     joins = joins.values_list(
    #         'structure__id',
    #         'subscription__human__id',
    #     ).distinct()

    #     # Normalize to list of lists
    #     joins = [list(x) for x in joins]

    #     # Creating/Update Member
    #     for join in joins:
    #         join.append(bool(self.filter(
    #             Q(inactive_date=None) |
    #             Q(
    #                 inactive_date__gt=localdate(),
    #                 subscription__status='active',
    #             ),
    #             structure__id=join[0],
    #             subscription__human__id=join[1],
    #         ).exclude(paid=0)))
    #         django_rq.enqueue(
    #             Member.objects.update_from_join2,
    #             join,
    #         )
    #     return len(joins)


class SubscriptionManager(Manager):
    def update_users(self, cursor=None):
        # Get base
        subscriptions = self.select_related(
            'human',
        ).filter(
            items_editable=True,
        ).order_by(
            'modified',
        )
        if cursor:
            subscriptions = subscriptions.filter(
                modified__gt=cursor,
            )
        else:
            # Else clear logs
            ss = StateLog.objects.filter(
                content_type__model='user',
                users__mc_pk__isnull=False,
            )
            ss.delete()
        t = subscriptions.count()
        # Creating/Update Persons
        User = apps.get_model('api.user')
        for subscription in subscriptions:
            django_rq.enqueue(
                User.objects.update_or_create_from_subscription,
                subscription,
            )
        return t
