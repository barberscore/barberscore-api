
# Standard Library
import datetime
import logging
import uuid
from math import ceil

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
from django.db.models import Q
from django.conf import settings
from django.utils.functional import cached_property

# Django
from django.contrib.postgres.fields import DecimalRangeField
from django.contrib.postgres.fields import IntegerRangeField

# First-Party
from .fields import ImageUploadPath
from .fields import DivisionsField

log = logging.getLogger(__name__)


class Assignment(TimeStampedModel):
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
        default=STATUS.active,
    )

    KIND = Choices(
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (30, 'observer', 'Observer'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    CATEGORY = Choices(
        (5, 'drcj', 'DRCJ'),
        (10, 'ca', 'CA'),
        (30, 'music', 'Music'),
        (40, 'performance', 'Performance'),
        (50, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
        null=True,
        blank=True,
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='assignments',
        on_delete=models.CASCADE,
    )

    person_id = models.UUIDField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assignments',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='assignments',
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "assignment"

    def __str__(self):
        return str(self.id)

    # Assignment Permissions
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
        roles = [
            'SCJC',
        ]
        return any(item in roles for item in request.user.roles)

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        roles = [
            'SCJC',
        ]
        return any(item in roles for item in request.user.roles)

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Assignment."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Withdraw the Assignment."""
        return


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (5, 'built', 'Built',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    name = models.CharField(
        max_length=255,
        default='Convention',
    )

    district = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    SEASON = Choices(
        # (1, 'summer', 'Summer',),
        # (2, 'midwinter', 'Midwinter',),
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

    venue_name = models.CharField(
        help_text="""
            The venue name (when available).""",
        max_length=255,
        default='(TBD)',
    )

    location = models.CharField(
        help_text="""
            The general location in the form "City, State".""",
        max_length=255,
        default='(TBD)',
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the convention.""",
        null=True,
        blank=True,
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

    divisions = DivisionsField(
        help_text="""Only select divisions if required.  If it is a district-wide convention do not select any.""",
        base_field=models.IntegerField(
            choices=DIVISION,
        ),
        default=list,
        blank=True,
    )

    KINDS = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )

    kinds = DivisionsField(
        help_text="""The session kind(s) created at build time.""",
        base_field=models.IntegerField(
            choices=KINDS,
        ),
        default=list,
        blank=True,
    )

    # FKs
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conventions',
    )

    group_id = models.UUIDField(
        null=True,
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='conventions',
    )

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    # Internals
    # class Meta:
    #     unique_together = (
    #         (
    #             'year',
    #             'season',
    #             'name',
    #             'group',
    #         ),
    #     )

    class JSONAPIMeta:
        resource_name = "convention"

    def __str__(self):
        if self.district == 'BHS':
            return " ".join([
                self.district,
                str(self.year),
                self.name,
            ])
        return " ".join([
            self.district,
            self.get_season_display(),
            str(self.year),
            self.name,
        ])

    def clean(self):
        return
        # if self.group.kind > self.group.KIND.district:
        #     raise ValidationError(
        #         {'group': 'Owning group must be at least district'}
        #     )

    # Methods
    def get_drcj_emails(self):
        assignments = self.assignments.filter(
            status=Assignment.STATUS.active,
            category=Assignment.CATEGORY.drcj,
        ).order_by(
            'kind',
            'category',
            'user__family_name',
            'user__given_name',
        )
        seen = set()
        result = [
            "{0} ({1} {2}) <{3}>".format(assignment.user.name, assignment.get_kind_display(), assignment.get_category_display(), assignment.user.email,)
            for assignment in assignments
            if not (
                "{0} ({1} {2}) <{3}>".format(assignment.user.name, assignment.get_kind_display(), assignment.get_category_display(), assignment.user.email,) in seen or seen.add(
                    "{0} ({1} {2}) <{3}>".format(assignment.user.name, assignment.get_kind_display(), assignment.get_category_display(), assignment.user.email,)
                )
            )
        ]
        return result


    def get_ca_emails(self):
        assignments = self.assignments.filter(
            status=Assignment.STATUS.active,
            category=Assignment.CATEGORY.ca,
        ).order_by(
            'kind',
            'category',
            'user__family_name',
            'user__given_name',
        )
        seen = set()
        result = [
            "{0} ({1} {2}) <{3}>".format(assignment.user.name, assignment.get_kind_display(), assignment.get_category_display(), assignment.user.email,)
            for assignment in assignments
            if not (
                "{0} ({1} {2}) <{3}>".format(assignment.user.name, assignment.get_kind_display(), assignment.get_category_display(), assignment.user.email,) in seen or seen.add(
                    "{0} ({1} {2}) <{3}>".format(assignment.user.name, assignment.get_kind_display(), assignment.get_category_display(), assignment.user.email,)
                )
            )
        ]
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
        roles = [
            'SCJC',
        ]
        return any(item in roles for item in request.user.roles)

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        roles = [
            'SCJC',
        ]
        return any(item in roles for item in request.user.roles)

    # Convention Transition Conditions
    def can_reset(self):
        if self.status <= self.STATUS.built:
            return True
        return False

    def can_build(self):
        if self.kinds and self.panel:
            return True
        return False

    def can_activate(self):
        try:
            return all([
                self.open_date,
                self.close_date,
                self.start_date,
                self.end_date,
                self.open_date < self.close_date,
                self.close_date < self.start_date,
                self.start_date <= self.end_date,
                self.location,
                self.timezone,
            ])
        except TypeError:
            return False
        return False

    def can_deactivate(self):
        return

    # Convention Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.new,
        conditions=[can_reset],
    )
    def reset(self, *args, **kwargs):
        assignments = self.assignments.all()
        assignments.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        """Build convention and related sessions."""

        # Reset for indempodence
        self.reset()

        # scjcs = Officer.objects.filter(
        #     Q(office=Officer.OFFICE.scjc_chair) | Q(office=Officer.OFFICE.scjc_admin),
        #     status__gt=0,
        # )
        # for scjc in scjcs:
        #     self.assignments.create(
        #         category=Assignment.CATEGORY.drcj,
        #         status=Assignment.STATUS.active,
        #         kind=Assignment.KIND.observer,
        #         person=scjc.person,
        #     )
        # drcjs = self.group.officers.filter(
        #     office=Officer.OFFICE.drcj,
        #     status__gt=0,
        # )
        # for drcj in drcjs:
        #     self.assignments.create(
        #         category=Assignment.CATEGORY.drcj,
        #         status=Assignment.STATUS.active,
        #         kind=Assignment.KIND.official,
        #         person=drcj.person,
        #     )
        # ca_specialists = Officer.objects.filter(
        #     office=Officer.OFFICE.scjc_ca,
        #     status__gt=0,
        # )
        # for ca_specialist in ca_specialists:
        #     self.assignments.create(
        #         category=Assignment.CATEGORY.ca,
        #         status=Assignment.STATUS.active,
        #         kind=Assignment.KIND.observer,
        #         person=ca_specialist.person,
        #     )
        # cas = ceil((self.panel + 1) / 2)
        # while cas > 0:
        #     self.assignments.create(
        #         category=Assignment.CATEGORY.ca,
        #         status=Assignment.STATUS.active,
        #         kind=Assignment.KIND.official,
        #     )
        #     cas -= 1
        judges = self.panel
        while judges > 0:
            self.assignments.create(
                category=Assignment.CATEGORY.music,
                status=Assignment.STATUS.active,
                kind=Assignment.KIND.official,
            )
            self.assignments.create(
                category=Assignment.CATEGORY.performance,
                status=Assignment.STATUS.active,
                kind=Assignment.KIND.official,
            )
            self.assignments.create(
                category=Assignment.CATEGORY.singing,
                status=Assignment.STATUS.active,
                kind=Assignment.KIND.official,
            )
            judges -= 1
        # for kind in list(self.kinds):
        #     self.sessions.create(
        #         kind=kind,
        #     )
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.built,
        target=STATUS.active,
        conditions=[can_activate],
    )
    def activate(self, *args, **kwargs):
        """Activate convention."""
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.active,
        target=STATUS.inactive,
        conditions=[can_deactivate],
    )
    def deactivate(self, *args, **kwargs):
        """Archive convention and related sessions."""
        return
