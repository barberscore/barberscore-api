# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps as api_apps
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import models

# First-Party
from api.managers import MemberManager

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Member(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
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

    PART = Choices(
        (-1, 'director', 'Director'),
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

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    is_admin = models.BooleanField(
        default=False,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

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

    # Internals
    objects = MemberManager()

    class Meta:
        unique_together = (
            ('group', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "member"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        if self.is_admin:
            try:
                is_active = self.person.user.is_active
            except ObjectDoesNotExist:
                raise ValidationError(
                    {'is_admin': 'Admin must User account.'}
                )
            if not is_active:
                raise ValidationError(
                    {'is_admin': 'Admin User account must be active.'}
                )

    def save(self, *args, **kwargs):
        # self.nomen = " ".join(
        #     map(
        #         lambda x: smart_text(x), [
        #             self.person,
        #             self.group,
        #         ]
        #     )
        # )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_group_manager,
            request.user.is_session_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.group.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
            request.user.is_session_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Member."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Member."""
        return
