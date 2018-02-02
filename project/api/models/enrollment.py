# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps as api_apps
from django.db import models
from django.utils.encoding import smart_text

# First-Party
from api.managers import EnrollmentManager

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Enrollment(TimeStampedModel):
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

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    # FKs
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
    )

    # Internals
    objects = EnrollmentManager()

    class Meta:
        default_related_name = 'enrollments'
        unique_together = (
            ('organization', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "enrollment"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.organization,
                    self.person,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Enrollment Permissions
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
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Enrollment Transitions
