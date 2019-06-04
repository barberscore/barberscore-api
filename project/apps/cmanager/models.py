
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

# Django
from django.contrib.postgres.fields import FloatRangeField
from django.contrib.postgres.fields import IntegerRangeField

# First-Party
from .managers import AwardManager
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

    person = models.ForeignKey(
        'bhs.person',
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
            request.user.is_assignment_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_assignment_manager,
        ])

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


class Award(TimeStampedModel):
    """
    Award Model.

    The specific award conferred by a Group.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""Award Name.""",
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

    KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    gender = models.IntegerField(
        help_text="""
            The gender to which the award is restricted.  If unselected, this award is open to all combinations.
        """,
        choices=GENDER,
        null=True,
        blank=True,
    )

    LEVEL = Choices(
        (10, 'championship', "Championship"),
        (30, 'qualifier', "Qualifier"),
        (45, 'representative', "Representative"),
        (50, 'deferred', "Deferred"),
        (60, 'manual', "Manual"),
        (70, 'raw', "Improved - Raw"),
        (80, 'standard', "Improved - Standard"),
    )

    level = models.IntegerField(
        choices=LEVEL,
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

    is_single = models.BooleanField(
        help_text="""Single-round award""",
        default=False,
    )

    threshold = models.FloatField(
        help_text="""
            The score threshold for automatic qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    minimum = models.FloatField(
        help_text="""
            The minimum score required for qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    advance = models.FloatField(
        help_text="""
            The score threshold to advance to next round (if any) in
            multi-round qualification.
        """,
        null=True,
        blank=True,
    )

    spots = models.IntegerField(
        help_text="""Number of top spots which qualify""",
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            The Public description of the award.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
    )

    DIVISION = Choices(
        (10, 'evgd1', 'EVG Division I'),
        (20, 'evgd2', 'EVG Division II'),
        (30, 'evgd3', 'EVG Division III'),
        (40, 'evgd4', 'EVG Division IV'),
        (50, 'evgd5', 'EVG Division V'),
        (60, 'fwdaz', 'FWD Arizona'),
        (70, 'fwdne', 'FWD Northeast'),
        (80, 'fwdnw', 'FWD Northwest'),
        (90, 'fwdse', 'FWD Southeast'),
        (100, 'fwdsw', 'FWD Southwest'),
        (110, 'lol10l', 'LOL 10000 Lakes'),
        (120, 'lolone', 'LOL Division One'),
        (130, 'lolnp', 'LOL Northern Plains'),
        (140, 'lolpkr', 'LOL Packerland'),
        (150, 'lolsw', 'LOL Southwest'),
        # (160, 'madatl', 'MAD Atlantic'),
        (170, 'madcen', 'MAD Central'),
        (180, 'madnth', 'MAD Northern'),
        (190, 'madsth', 'MAD Southern'),
        # (200, 'madwst', 'MAD Western'),
        (210, 'nedgp', 'NED Granite and Pine'),
        (220, 'nedmtn', 'NED Mountain'),
        (230, 'nedpat', 'NED Patriot'),
        (240, 'nedsun', 'NED Sunrise'),
        (250, 'nedyke', 'NED Yankee'),
        (260, 'swdne', 'SWD Northeast'),
        (270, 'swdnw', 'SWD Northwest'),
        (280, 'swdse', 'SWD Southeast'),
        (290, 'swdsw', 'SWD Southwest'),
    )

    division = models.IntegerField(
        choices=DIVISION,
        null=True,
        blank=True,
    )

    AGE = Choices(
        (10, 'seniors', 'Seniors',),
        (20, 'novice', 'Novice',),
        (30, 'youth', 'Youth',),
    )

    age = models.IntegerField(
        choices=AGE,
        null=True,
        blank=True,
    )

    SIZE = Choices(
        (100, 'p1', 'Plateau 1',),
        (110, 'p2', 'Plateau 2',),
        (120, 'p3', 'Plateau 3',),
        (130, 'p4', 'Plateau 4',),
        (140, 'pa', 'Plateau A',),
        (150, 'paa', 'Plateau AA',),
        (160, 'paaa', 'Plateau AAA',),
        (170, 'paaaa', 'Plateau AAAA',),
        (180, 'pb', 'Plateau B',),
        (190, 'pi', 'Plateau I',),
        (200, 'pii', 'Plateau II',),
        (210, 'piii', 'Plateau III',),
        (220, 'piv', 'Plateau IV',),
        (230, 'small', 'Small',),
    )

    size = models.IntegerField(
        choices=SIZE,
        null=True,
        blank=True,
    )

    size_range = IntegerRangeField(
        null=True,
        blank=True,
    )

    SCOPE = Choices(
        (100, 'p1', 'Plateau 1',),
        (110, 'p2', 'Plateau 2',),
        (120, 'p3', 'Plateau 3',),
        (130, 'p4', 'Plateau 4',),
        (140, 'pa', 'Plateau A',),
        (150, 'paa', 'Plateau AA',),
        (160, 'paaa', 'Plateau AAA',),
        (170, 'paaaa', 'Plateau AAAA',),
        (175, 'paaaaa', 'Plateau AAAAA',),
    )

    scope = models.IntegerField(
        choices=SCOPE,
        null=True,
        blank=True,
    )

    scope_range = FloatRangeField(
        null=True,
        blank=True,
    )

    # Denormalizations
    tree_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    # FKs
    group = models.ForeignKey(
        'bhs.group',
        related_name='awards',
        on_delete=models.CASCADE,
    )

    parent = models.ForeignKey(
        'self',
        help_text="""If a qualifier, this is the award qualifying for.""",
        related_name='children',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    objects = AwardManager()

    class Meta:
        ordering = [
            'tree_sort',
        ]

    class JSONAPIMeta:
        resource_name = "award"

    def __str__(self):
        return self.name

    def clean(self):
        if self.level == self.LEVEL.qualifier and not self.threshold:
            raise ValidationError(
                {'level': 'Qualifiers must have thresholds'}
            )
        # if self.level != self.LEVEL.qualifier and self.threshold:
        #     raise ValidationError(
        #         {'level': 'Non-Qualifiers must not have thresholds'}
        #     )

    # Award Permissions
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
            request.user.is_award_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_award_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Award."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Award."""
        return


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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
        (5, 'built', 'Built',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
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

    location = models.CharField(
        help_text="""
            The general location in the form "City, State".""",
        max_length=255,
        default='',
        blank=True,
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
    venue = models.ForeignKey(
        'stage.venue',
        related_name='conventions',
        help_text="""
            The specific venue for the convention (if available.)""",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    group = models.ForeignKey(
        'bhs.group',
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
        if self.group.kind > self.group.KIND.district:
            raise ValidationError(
                {'group': 'Owning group must be at least district'}
            )

    # Methods
    def get_drcj_emails(self):
        Assignment = apps.get_model('cmanager.assignment')
        assignments = self.assignments.filter(
            status=Assignment.STATUS.active,
            category=Assignment.CATEGORY.drcj,
            person__email__isnull=False,
        ).order_by(
            'kind',
            'category',
            'person__last_name',
            'person__first_name',
        )
        seen = set()
        result = [
            "{0} ({1} {2}) <{3}>".format(assignment.person.common_name, assignment.get_kind_display(), assignment.get_category_display(), assignment.person.email,)
            for assignment in assignments
            if not (
                "{0} ({1} {2}) <{3}>".format(assignment.person.common_name, assignment.get_kind_display(), assignment.get_category_display(), assignment.person.email,) in seen or seen.add(
                    "{0} ({1} {2}) <{3}>".format(assignment.person.common_name, assignment.get_kind_display(), assignment.get_category_display(), assignment.person.email,)
                )
            )
        ]
        return result


    def get_ca_emails(self):
        Assignment = apps.get_model('cmanager.assignment')
        assignments = self.assignments.filter(
            status=Assignment.STATUS.active,
            category=Assignment.CATEGORY.ca,
            person__email__isnull=False,
        ).order_by(
            'kind',
            'category',
            'person__last_name',
            'person__first_name',
        )
        seen = set()
        result = [
            "{0} ({1} {2}) <{3}>".format(assignment.person.common_name, assignment.get_kind_display(), assignment.get_category_display(), assignment.person.email,)
            for assignment in assignments
            if not (
                "{0} ({1} {2}) <{3}>".format(assignment.person.common_name, assignment.get_kind_display(), assignment.get_category_display(), assignment.person.email,) in seen or seen.add(
                    "{0} ({1} {2}) <{3}>".format(assignment.person.common_name, assignment.get_kind_display(), assignment.get_category_display(), assignment.person.email,)
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
                self.sessions.count() > 0,
            ])
        except TypeError:
            return False
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
        target=STATUS.new,
        conditions=[can_reset],
    )
    def reset(self, *args, **kwargs):
        assignments = self.assignments.all()
        sessions = self.sessions.all()
        assignments.delete()
        sessions.delete()
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

        # Assignment = apps.get_model('cmanager.assignment')
        Officer = apps.get_model('bhs.officer')
        scjcs = Officer.objects.filter(
            Q(office=Officer.OFFICE.scjc_chair) | Q(office=Officer.OFFICE.scjc_admin),
            status__gt=0,
        )
        for scjc in scjcs:
            self.assignments.create(
                category=Assignment.CATEGORY.drcj,
                status=Assignment.STATUS.active,
                kind=Assignment.KIND.observer,
                person=scjc.person,
            )
        drcjs = self.group.officers.filter(
            office=Officer.OFFICE.drcj,
            status__gt=0,
        )
        for drcj in drcjs:
            self.assignments.create(
                category=Assignment.CATEGORY.drcj,
                status=Assignment.STATUS.active,
                kind=Assignment.KIND.official,
                person=drcj.person,
            )
        ca_specialists = Officer.objects.filter(
            office=Officer.OFFICE.scjc_ca,
            status__gt=0,
        )
        for ca_specialist in ca_specialists:
            self.assignments.create(
                category=Assignment.CATEGORY.ca,
                status=Assignment.STATUS.active,
                kind=Assignment.KIND.observer,
                person=ca_specialist.person,
            )
        cas = ceil((self.panel + 1) / 2)
        while cas > 0:
            self.assignments.create(
                category=Assignment.CATEGORY.ca,
                status=Assignment.STATUS.active,
                kind=Assignment.KIND.official,
            )
            cas -= 1
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
        for kind in list(self.kinds):
            self.sessions.create(
                kind=kind,
            )
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
