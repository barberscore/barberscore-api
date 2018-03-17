# Standard Libary
import datetime
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
from django.core.exceptions import ValidationError
from django.db import models

# First-Party
config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
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

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (9, 'video', 'Video',),
    )

    season = models.IntegerField(
        choices=SEASON,
    )

    PANEL = Choices(
        (1, 'single', "Single"),
        (2, 'double', "Double"),
        (3, 'triple', "Triple"),
        (4, 'quadruple', "Quadruple"),
        (5, 'quintiple', "Quintiple"),
    )

    panel = models.IntegerField(
        choices=PANEL,
        null=True,
        blank=True,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
    )

    open_date = models.DateField(
        null=True,
        blank=True,
    )

    close_date = models.DateField(
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

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A general description field; usually used for hotel and venue info.""",
        blank=True,
        max_length=1000,
    )

    # FKs
    venue = models.ForeignKey(
        'Venue',
        related_name='conventions',
        help_text="""
            The venue for the convention.""",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    group = models.ForeignKey(
        'Group',
        related_name='conventions',
        on_delete=models.CASCADE,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "convention"

    def __str__(self):
        return self.name

    def clean(self):
        if self.group.kind > self.group.KIND.district:
            raise ValidationError(
                {'group': 'Owning group must be at least district'}
            )

    # Convention Permissions
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
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.group.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
        ])

    # Convention Transition Conditions
    def can_activate_convention(self):
        if any([
            not self.open_date,
            not self.close_date,
            not self.start_date,
            not self.close_date,
        ]):
            return False
        return all([
            self.open_date,
            self.close_date,
            self.start_date,
            self.end_date,
            self.open_date < self.close_date,
            self.close_date < self.start_date,
            self.start_date < self.end_date,
            self.grantors.count() > 0,
            self.sessions.count() > 0,
        ])

    # Convention Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.active,
        conditions=[can_activate_convention],
    )
    def activate(self, *args, **kwargs):
        """Publish convention and related sessions."""
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.inactive,
    )
    def deactivate(self, *args, **kwargs):
        """Archive convention and related sessions."""
        return
