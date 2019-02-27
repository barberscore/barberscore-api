
# Third-Party
import django_rq
from django_fsm_log.models import StateLog

# Django
from django.apps import apps
from django.db.models import Manager
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
        else:
            # Else clear logs
            ss = StateLog.objects.filter(
                content_type__model='person',
                groups__mc_pk__isnull=False,
            )
            ss.delete()
        t = humans.count()
        # Creating/Update Persons
        Person = apps.get_model('api.person')
        queue = django_rq.get_queue('low')
        for human in humans:
            queue.enqueue(
                Person.objects.update_or_create_from_human,
                human,
            )
        return t

    def delete_orphans(self):
        # Get base
        humans = list(self.values_list('id', flat=True))
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
        queue = django_rq.get_queue('low')
        for structure in structures:
            queue.enqueue(
                Group.objects.update_or_create_from_structure,
                structure,
            )
        return t

    def delete_orphans(self):
        # Get base
        structures = list(self.values_list('id', flat=True))
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
        roles = self.select_related(
            'structure',
            'human',
        )
        if cursor:
            roles = roles.filter(
                modified__gt=cursor,
            )
        t = roles.count()
        # Creates race condition on multi-worker
        Officer = apps.get_model('api.officer')
        queue = django_rq.get_queue('low')
        for role in roles:
            queue.enqueue(
                Officer.objects.update_or_create_from_role,
                role,
            )
        return t

    def delete_orphans(self):
        # Get base
        roles = list(self.values_list('id', flat=True))
        # Delete Orphans
        Officer = apps.get_model('api.officer')
        orphans = Officer.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=roles,
        )
        t = orphans.count()
        orphans.delete()
        return t


class JoinManager(Manager):
    def update_members(self, cursor=None):
        # Get all records as values
        joins = self.filter(
            paid=True,
        ).select_related(
            'structure',
            'subscription',
            'subscription__human',
        )
        if cursor:
            joins = joins.filter(
                modified__gt=cursor,
            )
        t = joins.count()
        # Creates race condition on multi-worker
        Member = apps.get_model('api.member')
        queue = django_rq.get_queue('low')
        for join in joins:
            queue.enqueue(
                Member.objects.update_or_create_from_join,
                join,
            )
        return t

    def delete_orphans(self):
        # Get base
        joins = list(self.values_list('id', flat=True))
        # Delete Orphans
        Member = apps.get_model('api.member')
        orphans = Member.objects.filter(
            mc_pk__isnull=False,
        ).exclude(
            mc_pk__in=joins,
        )
        t = orphans.count()
        orphans.delete()
        return t



# class SubscriptionManager(Manager):
#     def update_users(self, cursor=None):
#         # Get base
#         subscriptions = self.select_related(
#             'human',
#         ).filter(
#             items_editable=True,
#         ).order_by(
#             'modified',
#         )
#         if cursor:
#             subscriptions = subscriptions.filter(
#                 modified__gt=cursor,
#             )
#         else:
#             # Else clear logs
#             ss = StateLog.objects.filter(
#                 content_type__model='user',
#                 users__mc_pk__isnull=False,
#             )
#             ss.delete()
#         t = subscriptions.count()
#         # Creating/Update Persons
#         User = apps.get_model('api.user')
#         queue = django_rq.get_queue('low')
#         for subscription in subscriptions:
#             queue.enqueue(
#                 User.objects.update_or_create_from_subscription,
#                 subscription,
#             )
#         return t
