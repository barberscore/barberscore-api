
# Standard Library
import datetime
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from timezone_field import TimeZoneField

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import ArrayField

# First-Party
from api.fields import ImageUploadPath


log = logging.getLogger(__name__)


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    legacy_name = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    legacy_selection = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    legacy_complete = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    legacy_venue = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    STATUS = Choices(
        (-25, 'manual', 'Manual',),
        (-20, 'incomplete', 'Incomplete',),
        (-15, 'imported', 'Imported',),
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
        help_text="""
            The location in the form "City, State".""",
        max_length=255,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the convention.""",
    )

    image = models.ImageField(
        upload_to=ImageUploadPath(),
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A general description field; usually used for hotel and venue info.""",
        blank=True,
        max_length=1000,
    )

    DIVISION = Choices(
        ('EVG', [
            (10, 'evgd1', 'EVG Division I'),
            (20, 'evgd2', 'EVG Division II'),
            (30, 'evgd3', 'EVG Division III'),
            (40, 'evgd4', 'EVG Division IV'),
            (50, 'evgd5', 'EVG Division V'),
        ]),
        ('FWD', [
            (60, 'fwdaz', 'FWD Arizona'),
            (70, 'fwdne', 'FWD Northeast'),
            (80, 'fwdnw', 'FWD Northwest'),
            (90, 'fwdse', 'FWD Southeast'),
            (100, 'fwdsw', 'FWD Southwest'),
        ]),
        ('LOL', [
            (110, 'lol10l', 'LOL 10000 Lakes'),
            (120, 'lolone', 'LOL Division One'),
            (130, 'lolnp', 'LOL Northern Plains'),
            (140, 'lolpkr', 'LOL Packerland'),
            (150, 'lolsw', 'LOL Southwest'),
        ]),
        ('MAD', [
            # (160, 'madatl', 'MAD Atlantic'),
            (170, 'madcen', 'MAD Central'),
            (180, 'madnth', 'MAD Northern'),
            (190, 'madsth', 'MAD Southern'),
            # (200, 'madwst', 'MAD Western'),
        ]),
        ('NED', [
            (210, 'nedgp', 'NED Granite and Pine'),
            (220, 'nedmtn', 'NED Mountain'),
            (230, 'nedpat', 'NED Patriot'),
            (240, 'nedsun', 'NED Sunrise'),
            (250, 'nedyke', 'NED Yankee'),
        ]),
        ('SWD', [
            (260, 'swdne', 'SWD Northeast'),
            (270, 'swdnw', 'SWD Northwest'),
            (280, 'swdse', 'SWD Southeast'),
            (290, 'swdsw', 'SWD Southwest'),
        ]),
    )

    divisions = ArrayField(
        base_field=models.IntegerField(
            choices=DIVISION,
        ),
        default=list,
        blank=True,
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

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='conventions',
    )

    # Internals
    class Meta:
        unique_together = (
            (
                'year',
                'season',
                'name',
                'group',
            ),
        )

    class JSONAPIMeta:
        resource_name = "convention"

    def __str__(self):
        return self.name

    def clean(self):
        if self.group.kind > self.group.KIND.district:
            raise ValidationError(
                {'group': 'Owning group must be at least district'}
            )

    # Methods
    def get_assignment_emails(self):
        Assignment = apps.get_model('api.assignment')
        assignments = self.assignments.filter(
            status=Assignment.STATUS.active,
            category__lte=Assignment.CATEGORY.ca,
            person__email__isnull=False,
        )
        result = ["{0} <{1}>".format(
            assignment.person.common_name,
            assignment.person.email,
        ) for assignment in assignments]
        return result


    # Convention Permissions
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
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_convention_manager,
        ])

    # Convention Transition Conditions
    def can_activate(self):
        if self.status == self.STATUS.new:
            return all([
                self.open_date,
                self.close_date,
                self.start_date,
                self.end_date,
                self.open_date < self.close_date,
                self.close_date < self.start_date,
                self.start_date <= self.end_date,
                self.sessions.count() > 0,
            ])
        return False

    def can_deactivate(self):
        return all([
            not self.sessions.exclude(status=self.sessions.model.STATUS.finished)
        ])

    # Convention Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.active,
        conditions=[can_activate],
    )
    def activate(self, *args, **kwargs):
        """Publish convention and related sessions."""
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.inactive,
        conditions=[can_deactivate],
    )
    def deactivate(self, *args, **kwargs):
        """Archive convention and related sessions."""
        return
