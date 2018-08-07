# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django_fsm_log.models import StateLog
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.timezone import localdate

# Django
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.apps import apps

# First-Party
from api.managers import MemberManager

log = logging.getLogger(__name__)


class Member(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    MEM_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'active_internal', 'Active Internal',),
        (30, 'active_licensed', 'Active Licensed',),
        (40, 'cancelled', 'Cancelled',),
        (50, 'closed', 'Closed',),
        (60, 'closed_merged', 'Closed Merged',),
        (70, 'closed_revoked', 'Closed Revoked',),
        (80, 'closed_voluntary', 'Closed Voluntary',),
        (90, 'expelled', 'Expelled',),
        (100, 'expired', 'Expired',),
        (105, 'expired_licensed', 'Expired Licensed',),
        (110, 'lapsed', 'Lapsed',),
        (120, 'not_approved', 'Not Approved',),
        (130, 'pending', 'Pending',),
        (140, 'pending_voluntary', 'Pending Voluntary',),
        (150, 'suspended', 'Suspended',),
        (160, 'suspended_membership', 'Suspended Membership',),
        (170, 'awaiting_payment', 'Awaiting Payment',),
    )

    mem_status = models.IntegerField(
        choices=MEM_STATUS,
        null=True,
        blank=True,
    )

    SUB_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'expired', 'Expired',),
        (30, 'pending', 'Pending',),
        (40, 'lapsedRenew', 'Lapsed',),
        (50, 'cancelled', 'Cancelled',),
        (60, 'swapped', 'Swapped',),
    )

    sub_status = models.IntegerField(
        choices=SUB_STATUS,
        null=True,
        blank=True,
    )

    MEM_CODE = Choices(
        (10, 'RG', 'RG Regular'),
        (20, 'R5', 'R5 Regular 50 Year'),
        (30, 'SN', 'SN Senior'),
        (40, 'S5', 'S5 Senior 50 Year'),
        (50, 'SL', 'SL Senior Legacy'),
        (60, 'Y1', 'Y1 Youth Initial'),
        (70, 'Y2', 'Y2 Youth Subsequent'),
        (80, 'LF', 'LF Lifetime Regular'),
        (90, 'L5', 'L5 Lifetime 50 Year'),
        (100, 'LY', 'LY Lifetime Youth'),
        (110, 'LS', 'LS Lifetime Senior'),
        (120, 'AS', 'AS Associate'),
    )

    mem_code = models.IntegerField(
        choices=MEM_CODE,
        null=True,
        blank=True,
    )

    inactive_date = models.DateField(
        null=True,
        blank=True,
    )

    INACTIVE_REASON = Choices(
        (1, 'Non_renewal', 'Non-Renewal'),
        (2, 'Renewed', 'Renewed'),
        (3, 'NotCancelled', 'Not Cancelled'),
        (4, 'Non_Payment', 'Non-Payment'),
        (5, 'Expired', 'Expired'),
        (6, 'Deceased', 'Deceased'),
        (7, 'changedOption', 'changedOption'),
        (8, 'Other', 'Other'),
        (9, 'cancelled', 'cancelled'),
        (10, 'Transferred', 'Transferred'),
        (11, 'swappedChapter', 'swappedChapter'),
        (12, 'swapped', 'swapped'),
    )

    inactive_reason = models.IntegerField(
        choices=INACTIVE_REASON,
        null=True,
        blank=True,
    )

    PART = Choices(
        # (-1, 'director', 'Director'),
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        null=True,
        blank=True,
    )

    established_date = models.DateField(
        null=True,
        blank=True,
    )

    current_through = models.DateField(
        null=True,
        blank=True,
    )

    mc_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    # Properties
    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='members',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='members',
        on_delete=models.CASCADE,
    )

    subscription = models.ForeignKey(
        'Subscription',
        related_name='members',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='members',
    )

    # Internals
    objects = MemberManager()

    class Meta:
        unique_together = (
            ('group', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "member"

    def __str__(self):
        return str(self.id)

    def clean(self):
        pass
        # if self.is_admin:
        #     try:
        #         is_active = self.person.user.is_active
        #     except ObjectDoesNotExist:
        #         raise ValidationError(
        #             {'is_admin': 'Admin must User account.'}
        #         )
        #     if not is_active:
        #         raise ValidationError(
        #             {'is_admin': 'Admin User account must be active.'}
        #         )

    # Methods
    def mc_check(self):
        Join = apps.get_model('bhs.join')
        if not self.mc_pk:
            return ValueError("Not a MC Record")
        status = bool(Join.objects.filter(
            Q(inactive_date=None) |
            Q(
                inactive_date__gt=localdate(),
                subscription__status='active',
            ),
            structure__id=self.group.mc_pk,
            subscription__human__id=self.person.mc_pk,
        ))
        if status and self.status != self.STATUS.active:
            self.activate()
            self.save()
            return "Activated"
        if not status and self.status != self.STATUS.inactive:
            self.deactivate()
            self.save()
            return "Deactivated"
        return "No change"

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.group.officers.filter(
                    person__user=request.user,
                    status__gt=0,
                ),
                self.mc_pk == None,
            ]),
        ])

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Member."""
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Member."""
        return
