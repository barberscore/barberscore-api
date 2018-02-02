# Standard Libary
import datetime
import logging
import random
import uuid

# Third-Party
from cloudinary.models import CloudinaryField
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ranking import Ranking
from timezone_field import TimeZoneField

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField  # CIEmailField,
from django.contrib.postgres.fields import FloatRangeField
from django.contrib.postgres.fields import IntegerRangeField
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.timezone import now

# First-Party
from api.fields import CloudinaryRenameField
from api.managers import ChartManager
from api.managers import ConventionManager
from api.managers import EnrollmentManager
from api.managers import GroupManager
from api.managers import MemberManager
from api.managers import OrganizationManager
from api.managers import PersonManager
from api.managers import UserManager
from api.tasks import create_admins_report
from api.tasks import create_bbscores_report
from api.tasks import create_csa_report
from api.tasks import create_drcj_report
from api.tasks import create_ors_report
from api.tasks import create_oss_report
from api.tasks import create_sa_report
from api.tasks import create_variance_report
from api.tasks import send_entry
from api.tasks import send_session
from api.tasks import send_session_reports

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Repertory(TimeStampedModel):
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
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='repertories',
        on_delete=models.CASCADE,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='repertories',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        verbose_name_plural = 'repertories'
        unique_together = (
            ('group', 'chart',),
        )

    class JSONAPIMeta:
        resource_name = "repertory"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.group,
                    self.chart,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_group_manager,
            request.user.is_session_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.group.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_session_manager,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_group_manager,
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
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Repertory."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Repertory."""
        return
