
# Standard Library
import uuid
import datetime

# Third-Party
from django_fsm import FSMIntegerField
from django.core.files.base import ContentFile
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from timezone_field import TimeZoneField

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Func
from django.db.models import F
from django.conf import settings
from django.contrib.postgres.fields import DecimalRangeField
from django.contrib.postgres.fields import IntegerRangeField
from django.utils.functional import cached_property
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

from .fields import UploadPath
from .fields import DivisionsField
from .tasks import build_email
from .tasks import send_invite_email_from_entry
from .tasks import send_submit_email_from_entry
from .tasks import send_withdraw_email_from_entry
from .tasks import send_approve_email_from_entry
from .tasks import send_open_email_from_session
from .tasks import send_close_email_from_session
from .tasks import send_verify_email_from_session
from .tasks import send_verify_report_email_from_session
from .tasks import send_package_email_from_session
from .tasks import send_package_report_email_from_session

from django.apps import apps


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
        upload_to=UploadPath('image'),
        max_length=255,
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


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # Denormalized from BHS Award
    award_id = models.UUIDField(
        null=True,
        blank=True,
    )

    award_name = models.CharField(
        help_text="""Award Name.""",
        max_length=255,
        null=True,
        blank=True,
    )

    AWARD_KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    award_kind = models.IntegerField(
        choices=AWARD_KIND,
        null=True,
        blank=True,
    )

    AWARD_GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    award_gender = models.IntegerField(
        help_text="""
            The gender to which the award is restricted.  If unselected, this award is open to all combinations.
        """,
        choices=AWARD_GENDER,
        null=True,
        blank=True,
    )

    AWARD_LEVEL = Choices(
        (10, 'championship', "Championship"),
        (30, 'qualifier', "Qualifier"),
        (45, 'representative', "Representative"),
        (50, 'deferred', "Deferred"),
        (60, 'manual', "Manual"),
        (70, 'raw', "Improved - Raw"),
        (80, 'standard', "Improved - Standard"),
    )

    award_level = models.IntegerField(
        choices=AWARD_LEVEL,
        null=True,
        blank=True,
    )

    AWARD_SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    award_season = models.IntegerField(
        choices=AWARD_SEASON,
        null=True,
        blank=True,
    )

    award_description = models.TextField(
        help_text="""
            The Public description of the award.""",
        max_length=1000,
        null=True,
        blank=True,
    )

    award_district = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    AWARD_DIVISION = Choices(
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

    award_division = models.IntegerField(
        choices=AWARD_DIVISION,
        null=True,
        blank=True,
    )

    AWARD_AGE = Choices(
        (10, 'seniors', 'Seniors',),
        (20, 'novice', 'Novice',),
        (30, 'youth', 'Youth',),
    )

    award_age = models.IntegerField(
        choices=AWARD_AGE,
        null=True,
        blank=True,
    )

    award_is_novice = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    AWARD_SIZE = Choices(
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

    award_size = models.IntegerField(
        choices=AWARD_SIZE,
        null=True,
        blank=True,
    )

    award_size_range = IntegerRangeField(
        null=True,
        blank=True,
    )

    AWARD_SCOPE = Choices(
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

    award_scope = models.IntegerField(
        choices=AWARD_SCOPE,
        null=True,
        blank=True,
    )

    award_scope_range = DecimalRangeField(
        null=True,
        blank=True,
    )

    award_tree_sort = models.IntegerField(
        # unique=True,
        editable=False,
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='contests',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='contests',
    )

    # Internals
    # class Meta:
    #     unique_together = (
    #         ('session', 'award',)
    #     )

    class JSONAPIMeta:
        resource_name = "contest"

    def __str__(self):
        return str(self.id)

    def clean(self):
        pass
        # if self.award.level == self.award.LEVEL.qualifier and self.group:
        #     raise ValidationError(
        #         {'level': 'Qualifiers can not select winners'}
        #     )


    # Contest Permissions
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
            'DRCJ',
        ]
        return any([item in roles for item in request.user.roles])


    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        if self.session.status >= self.session.STATUS.opened:
            return False
        return any([
            'SCJC' in request.user.roles,
            self.session.owners.filter(id__contains=request.user.id),
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.excluded], target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.included], target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return


class Contestant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    entry = models.ForeignKey(
        'Entry',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='contestants',
    )

    # Internals
    # class Meta:
    #     ordering = (
    #         'contest__award__tree_sort',
    #     )
    #     unique_together = (
    #         ('entry', 'contest',),
    #     )

    class JSONAPIMeta:
        resource_name = "contestant"

    def __str__(self):
        return str(self.id)

    # Methods

    # Contestant Permissions
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
            'DRCJ',
            'Manager',
        ]
        return any([item in roles for item in request.user.roles])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                'SCJC' in request.user.roles,
            ]),
            all([
                self.contest.session.owners.filter(id__contains=request.user.id),
                self.contest.session.status < self.contest.session.STATUS.packaged,
            ]),
            all([
                self.entry.owners.filter(id__contains=request.user.id),
                self.entry.status < self.entry.STATUS.approved,
            ]),
        ])

    # Contestant Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return


class Entry(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'built', 'Built',),
        (5, 'invited', 'Invited',),
        (7, 'withdrawn', 'Withdrawn',),
        (10, 'submitted', 'Submitted',),
        (20, 'approved', 'Approved',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    is_evaluation = models.BooleanField(
        help_text="""
            Entry requests evaluation.""",
        default=True,
    )

    is_private = models.BooleanField(
        help_text="""
            Keep scores private.""",
        default=False,
    )

    is_mt = models.BooleanField(
        help_text="""
            Keep scores private.""",
        default=False,
    )

    draw = models.IntegerField(
        help_text="""
            The draw for the initial round only.""",
        null=True,
        blank=True,
    )

    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    base = models.FloatField(
        help_text="""
            The incoming base score used to determine most-improved winners.""",
        null=True,
        blank=True,
    )

    participants = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    pos = models.IntegerField(
        help_text='Estimated Participants-on-Stage',
        null=True,
        blank=True,
    )

    representing = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    description = models.TextField(
        help_text="""
            Public Notes (usually from group).""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
    )

    image = models.ImageField(
        upload_to=UploadPath('image'),
        max_length=255,
        null=True,
        blank=True,
    )

    # Denorm
    group_id = models.UUIDField(
        null=True,
        blank=True,
    )

    GROUP_STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (-5, 'aic', 'AIC',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    group_status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=GROUP_STATUS,
        null=True,
        blank=True,
    )

    group_name = models.CharField(
        help_text="""
            The name of the resource.
        """,
        max_length=255,
        default='',
        blank=True,
    )

    group_nomen = models.CharField(
        help_text="""
            The combined name of the resource.
        """,
        max_length=255,
        default='',
        blank=True,
    )

    GROUP_KIND = Choices(
        ('International', [
            (1, 'international', "International"),
        ]),
        ('District', [
            (11, 'district', "District"),
            (12, 'noncomp', "Noncompetitive"),
            (13, 'affiliate', "Affiliate"),
        ]),
        ('Chapter', [
            (30, 'chapter', "Chapter"),
        ]),
        ('Group', [
            (32, 'chorus', "Chorus"),
            (41, 'quartet', "Quartet"),
            (46, 'vlq', "VLQ"),
        ]),
    )

    group_kind = models.IntegerField(
        help_text="""
            The kind of group.
        """,
        choices=GROUP_KIND,
        null=True,
        blank=True,
    )

    GROUP_GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    group_gender = models.IntegerField(
        help_text="""
            The gender of group.
        """,
        choices=GROUP_GENDER,
        null=True,
        blank=True,
    )

    GROUP_DIVISION = Choices(
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

    group_division = models.IntegerField(
        choices=GROUP_DIVISION,
        null=True,
        blank=True,
    )

    group_bhs_id = models.IntegerField(
        blank=True,
        null=True,
        unique=True,
    )

    group_code = models.CharField(
        help_text="""
            Short-form code.""",
        max_length=255,
        blank=True,
        default='',
    )

    group_description = models.TextField(
        help_text="""
            A description of the group.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
        default='',
    )

    group_participants = models.CharField(
        help_text='Director(s) or Members (listed TLBB)',
        max_length=255,
        blank=True,
        default='',
    )

    group_tree_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    group_international = models.TextField(
        help_text="""
            The denormalized international group.""",
        blank=True,
        max_length=255,
        default='',
    )

    group_district = models.TextField(
        help_text="""
            The denormalized district group.""",
        blank=True,
        max_length=255,
        default='',
    )

    group_chapter = models.TextField(
        help_text="""
            The denormalized chapter group.""",
        blank=True,
        max_length=255,
        default='',
    )

    group_is_senior = models.BooleanField(
        help_text="""Qualifies as a Senior Group.  This can be set manually, but is denormlized nightly for quartets.""",
        default=False,
    )

    group_is_youth = models.BooleanField(
        help_text="""Qualifies as a Youth Group.  Must be set manually.""",
        default=False,
    )

    group_is_divided = models.BooleanField(
        help_text="""This district has divisions.""",
        default=False,
    )

    group_is_divided = models.BooleanField(
        help_text="""This district has divisions.""",
        default=False,
    )

    group_charts = ArrayField(
        base_field=JSONField(
            default=dict,
            blank=True,
            null=True,
        ),
        null=True,
        blank=True,
        default=list,
    )

    # FKs
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='entries',
    )

    session = models.ForeignKey(
        'Session',
        related_name='entries',
        on_delete=models.CASCADE,
    )

    statelogs = GenericRelation(
        StateLog,
        related_query_name='entries',
    )

    # Properties
    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    # Internals
    class Meta:
        verbose_name_plural = 'entries'
        # unique_together = (
        #     ('group', 'session',),
        # )

    class JSONAPIMeta:
        resource_name = "entry"

    def __str__(self):
        return str(self.id)

    def clean(self):
        if self.is_private and self.contestants.filter(status__gt=0):
            raise ValidationError(
                {'is_private': 'You may not compete for an award and remain private.'}
            )
        if self.session.status >= self.session.STATUS.packaged:
            raise ValidationError(
                {'session': 'You may not add entries after the Session has been packaged.'}
            )


    # Entry Permissions
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
            'DRCJ',
            'Manager',
        ]
        return any([item in roles for item in request.user.roles])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            # For SCJC
            'SCJC' in request.user.roles,
            # For DRCJs
            all([
                self.session.owners.filter(id__contains=request.user.id),
                self.session.status < self.session.STATUS.packaged,
            ]),
            # For Groups
            all([
                self.owners.filter(id__contains=request.user.id),
                self.status <= self.STATUS.approved,
            ]),
        ])

    # Methods
    def update_from_group(self):
        if self.group_id:
            Group = apps.get_model('bhs.group')
            group = Group.objects.get(id=self.group_id)
            repertories = group.repertories.filter(
                status__gt=0,
            )
            charts = [{
                'id': str(repertory.chart.id),
                'title': repertory.chart.title,
                'arrangers': repertory.chart.arrangers,
                'nomen': repertory.chart.nomen,
            } for repertory in repertories]
            self.group_name = group.name
            self.group_status = group.status
            self.group_nomen = group.nomen
            self.group_kind = group.kind
            self.group_gender = group.gender
            self.group_division = group.division
            self.group_bhs_id = group.bhs_id
            self.group_code = group.code
            self.group_description = group.description
            self.group_participants = group.participants
            self.group_tree_sort = group.tree_sort
            self.group_international = group.international
            self.group_district = group.district
            self.group_chapter = group.chapter
            self.group_is_senior = group.is_senior
            self.group_is_youth = group.is_youth
            self.group_is_divided = group.is_divided
            self.group_charts = charts
            self.owners.set(group.owners.all())
            if group.image:
                try:
                    self.image.save('image', group.image.file, save=True)
                except:
                    pass
        return

    def get_owner_emails(self):
        owners = self.owners.order_by(
            'last_name',
            'first_name',
        )
        seen = set()
        result = [
            "{0} ({1}) <{2}>".format(owner.name, self.group_name, owner.email)
            for owner in owners
            if not (
                "{0} ({1}) <{2}>".format(owner.name, self.group_name, owner.email) in seen or seen.add(
                    "{0} ({1}) <{2}>".format(owner.name, self.group_name, owner.email)
                )
            )
        ]
        return result

    def get_invite_email(self):
        template = 'emails/entry_invite.txt'
        context = {'entry': self}
        subject = "[Barberscore] Contest Invitation for {0}".format(
            self.group_name,
        )
        to = self.get_owner_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_invite_email(self):
        email = self.get_invite_email()
        return email.send()


    def get_withdraw_email(self):
        # Send confirmation email
        template = 'emails/entry_withdraw.txt'
        context = {'entry': self}
        subject = "[Barberscore] Withdrawl Notification for {0}".format(
            self.group_name,
        )
        to = self.get_owner_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_withdraw_email(self):
        email = self.get_withdraw_email()
        return email.send()


    def get_submit_email(self):
        template = 'emails/entry_submit.txt'
        contestants = self.contestants.filter(
            status__gt=0,
        ).order_by(
            'contest__award_name',
        )
        context = {
            'entry': self,
            'contestants': contestants,
        }
        subject = "[Barberscore] Submission Notification for {0}".format(
            self.group_name,
        )
        to = self.get_owner_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_submit_email(self):
        email = self.get_submit_email()
        return email.send()


    def get_approve_email(self):
        template = 'emails/entry_approve.txt'
        repertories = sorted(self.group_charts)
        contestants = self.contestants.filter(
            status__gt=0,
        ).order_by(
            'contest__award_name',
        )
        context = {
            'entry': self,
            'repertories': repertories,
            'contestants': contestants,
        }
        subject = "[Barberscore] Approval Notification for {0}".format(
            self.group_name,
        )
        to = self.group.get_officer_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_approve_email(self):
        email = self.get_approve_email()
        return email.send()


    # Entry Transition Conditions
    def can_build_entry(self):
        return True

    def can_invite_entry(self):
        return all([
            self.owners,
            self.group_status == self.GROUP_STATUS.active,
        ])

    def can_submit_entry(self):
        return all([
            # Only active groups can submit.
            self.group_status == self.GROUP_STATUS.active,
            # Check POS for choruses only
            self.pos if self.group_kind == self.GROUP_KIND.chorus else True,
            # ensure they can't submit a private while competiting.
            not all([
                self.is_private,
                self.contestants.filter(status__gt=0).count() > 0,
            ]),
            # Check participants
            self.participants,
        ])

    def can_approve(self):
        if self.is_private and self.contestants.filter(status__gt=0):
            return False
        return True

    # Entry Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new],
        target=STATUS.built,
        conditions=[can_build_entry],
    )
    def build(self, *args, **kwargs):
        """Build Entry"""
        self.update_from_group()
        contests = self.session.contests.filter(
            status=self.session.contests.model.STATUS.included,
        )
        for contest in contests:
            # Could also do some default logic here.
            self.contestants.create(
                status=self.contestants.model.STATUS.excluded,
                contest=contest,
            )
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
        ],
        target=STATUS.invited,
        conditions=[can_invite_entry],
    )
    def invite(self, *args, **kwargs):
        """Invites the group to enter"""
        send_invite_email_from_entry.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
            STATUS.invited,
            STATUS.submitted,
            STATUS.approved,
        ],
        target=STATUS.withdrawn,
        conditions=[],
    )
    def withdraw(self, *args, **kwargs):
        """Withdraws the Entry from the Session"""
        # If the session has been drawn, re-index.
        if self.draw:
            remains = self.session.entries.filter(draw__gt=self.draw)
            self.draw = None
            self.save()
            for entry in remains:
                entry.draw = entry.draw - 1
                entry.save()
        # Remove from all contestants
        contestants = self.contestants.filter(status__gte=0)
        for contestant in contestants:
            contestant.exclude()
            contestant.save()
        # Queue email
        send_withdraw_email_from_entry.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
            STATUS.invited,
            STATUS.submitted,
            STATUS.withdrawn,
        ],
        target=STATUS.submitted,
        conditions=[can_submit_entry],
    )
    def submit(self, *args, **kwargs):
        send_submit_email_from_entry.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
            STATUS.submitted,
            STATUS.withdrawn,
            STATUS.approved,
        ],
        target=STATUS.approved,
        conditions=[
            can_approve,
        ],
    )
    def approve(self, *args, **kwargs):
        send_approve_email_from_entry.delay(self)
        return


class Session(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'built', 'Built',),
        (4, 'opened', 'Opened',),
        (8, 'closed', 'Closed',),
        (10, 'verified', 'Verified',),
        (20, 'packaged', 'Packaged',),
        (30, 'finished', 'Finished',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of session.  Generally this will be either quartet or chorus.
        """,
        choices=KIND,
    )

    num_rounds = models.IntegerField(
        default=0,
    )

    is_invitational = models.BooleanField(
        help_text="""Invite-only (v. Open).""",
        default=False,
    )

    description = models.TextField(
        help_text="""
            The Public Description.  Will be sent in all email communications.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).  Will not be sent.""",
        blank=True,
    )

    footnotes = models.TextField(
        help_text="""
            Freeform text field; will print on OSS.""",
        blank=True,
    )

    legacy_report = models.FileField(
        upload_to=UploadPath('legacy_report'),
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
    )

    drcj_report = models.FileField(
        upload_to=UploadPath('drcj_report'),
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
    )

    # FKs
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='sessions',
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    target = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='feeders',
        on_delete=models.SET_NULL,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='sessions',
    )

    # Properties
    # Internals
    # class Meta:
        # unique_together = (
        #     ('convention', 'kind')
        # )

    class JSONAPIMeta:
        resource_name = "session"

    def __str__(self):
        return str(self.id)

    def clean(self):
        pass

    # Methods
    def get_invitees(self):
        Entry = apps.get_model('smanager.entry')
        Panelist = apps.get_model('rmanager.panelist')
        target = self.contests.filter(
            status__gt=0,
            # award__children__isnull=False,
        ).distinct().first().award
        feeders = self.feeders.all()
        entries = Entry.objects.filter(
            session__in=feeders,
            # contestants__contest__award__parent=target,
            # contestants__contest__status__gt=0,
        ).annotate(
            raw_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
            tot_score=Func(
                F('raw_score'),
                function='ROUND',
                template='%(function)s(%(expressions)s, 1)'
            ),
        ).exclude(
            tot_score=None,
        ).order_by(
            '-tot_score',
        )
        return entries


    def get_legacy(self):
        Entry = apps.get_model('smanager.entry')
        Group = apps.get_model('bhs.group')
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'oa',
            'contestant_id',
            'group_name',
            'group_type',
            'song_number',
            'song_title',
        ]
        ws.append(fieldnames)
        entries = self.entries.filter(
            status__in=[
                Entry.STATUS.approved,
            ]
        ).order_by('draw')
        for entry in entries:
            group = Group.objects.get(id=entry.group_id)
            oa = entry.draw
            group_name = group.name.encode('utf-8').strip()
            group_type = group.get_kind_display()
            if group_type == 'Quartet':
                contestant_id = group.bhs_id
            elif group_type == 'Chorus':
                contestant_id = group.code
            elif group_type == 'VLQ':
                contestant_id = group.code
            else:
                raise RuntimeError("Improper Entity Type: {0}".format(group.get_kind_display()))
            i = 1
            for repertory in group.repertories.order_by('chart__title'):
                song_number = i
                song_title = repertory.chart.title.encode('utf-8').strip()
                i += 1
                row = [
                    oa,
                    contestant_id,
                    group_name,
                    group_type,
                    song_number,
                    song_title,
                ]
                ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    def save_legacy(self):
        content = self.get_legacy()
        self.legacy_report.save("legacy_report", content)


    def get_drcj(self):
        Entry = apps.get_model('smanager.entry')
        Award = apps.get_model('bhs.award')
        Group = apps.get_model('bhs.group')
        Member = apps.get_model('bhs.member')
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'OA',
            'Group Name',
            'Representing',
            'Evaluation?',
            'Score/Eval-Only?',
            'BHS ID',
            'Group Status',
            'Repertory Count',
            'Estimated MOS',
            'Members Expiring',
            'Tenor',
            'Lead',
            'Baritone',
            'Bass',
            'Director/Participant(s)',
            'Award(s)',
            'Chapter(s)',
            'Contacts(s)',
        ]
        ws.append(fieldnames)
        entries = self.entries.filter(
            status__in=[
                Entry.STATUS.approved,
            ]
        ).order_by('draw')
        for entry in entries:
            group = Group.objects.get(id=entry.group_id)
            oa = entry.draw
            group_name = group.name
            representing = entry.representing
            evaluation = entry.is_evaluation
            is_private = entry.is_private
            bhs_id = group.bhs_id
            repertory_count = group.repertories.filter(
                status__gt=0,
            ).count()
            group_status = group.get_status_display()
            repertory_count = group.repertories.filter(
                status__gt=0,
            ).count()
            participant_count = entry.pos
            members = group.members.filter(
                status__gt=0,
            )
            # expiring_count = 0
            # for member in members:
            #     try:
            #         if member.person.current_through <= self.convention.close_date:
            #             expiring_count += 1
            #     except TypeError:
            #         continue
            expiring_count = "N/A"
            participants = entry.participants
            awards_list = []
            contestants = entry.contestants.filter(
                status__gt=0,
            ).order_by(
                # 'contest__award__name',
            )
            for contestant in contestants:
                award = Award.objects.get(id=contestant.contest.award_id)
                awards_list.append(award.name)
            awards = "\n".join(filter(None, awards_list))
            parts = {}
            part = 1
            while part <= 4:
                try:
                    member = members.get(
                        part=part,
                    )
                except Member.DoesNotExist:
                    parts[part] = None
                    part += 1
                    continue
                except Member.MultipleObjectsReturned:
                    parts[part] = None
                    part += 1
                    continue
                member_list = []
                member_list.append(
                    member.person.nomen,
                )
                member_list.append(
                    member.person.email,
                )
                phone = member.person.cell_phone.as_national if member.person.cell_phone else None
                member_list.append(
                    phone,
                )
                member_detail = "\n".join(filter(None, member_list))
                parts[part] = member_detail
                part += 1
            if group.kind == group.KIND.quartet:
                persons = members.values_list('person', flat=True)
                cs = Group.objects.filter(
                    members__person__in=persons,
                    members__status__gt=0,
                    kind=Group.KIND.chapter,
                ).distinct(
                ).order_by(
                    'name',
                ).values_list(
                    'name',
                    flat=True
                )
                chapters = "\n".join(cs)
            elif group.kind == group.KIND.chorus:
                try:
                    chapters = group.parent.name
                except AttributeError:
                    chapters = None
            admins = group.officers.filter(
                status__gt=0,
            )
            admins_list = []
            for admin in admins:
                phone = admin.person.cell_phone.as_national if admin.person.cell_phone else None
                contact = "; ".join(filter(None, [
                    admin.person.common_name,
                    admin.person.email,
                    phone,
                ]))
                admins_list.append(contact)
            contacts = "\n".join(filter(None, admins_list))
            row = [
                oa,
                group_name,
                representing,
                evaluation,
                is_private,
                bhs_id,
                group_status,
                repertory_count,
                participant_count,
                expiring_count,
                parts[1],
                parts[2],
                parts[3],
                parts[4],
                participants,
                awards,
                chapters,
                contacts,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    def save_drcj(self):
        content = self.get_drcj()
        self.drcj_report.save("drcj_report", content)


    def get_district_emails(self):
        Officer = apps.get_model('bhs.officer')
        Group = apps.get_model('bhs.group')
        officers = Officer.objects.filter(
            status=Officer.STATUS.active,
            group__status=Group.STATUS.active,
            person__email__isnull=False,
        )
        if self.kind == self.KIND.quartet:
            officers = officers.filter(
                group__parent=self.convention.group,
                group__kind=self.KIND.quartet,
            )
        else:
            officers = officers.filter(
                group__parent__parent=self.convention.group,
            ).exclude(
                group__kind=self.KIND.quartet,
            )
        if self.convention.divisions:
            officers = officers.filter(
                group__division__in=self.convention.divisions,
            )
        officers = officers.order_by(
            'group__name',
            'person__last_name',
            'person__first_name',
        )
        # Remove duplicates whilst preserving order.
        # http://www.martinbroadhurst.com/removing-duplicates-from-a-list-while-preserving-order-in-python.html
        seen = set()
        result = [
            "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
            for officer in officers
            if not (
                "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,) in seen or seen.add(
                    "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
                )
            )
        ]
        return result


    def get_participant_emails(self):
        Officer = apps.get_model('bhs.officer')
        Entry = apps.get_model('smanager.entry')
        officers = Officer.objects.filter(
            group__entries__in=self.entries.filter(status=Entry.STATUS.approved),
        ).order_by(
            'group__name',
            'person__last_name',
            'person__first_name',
        )
        seen = set()
        result = [
            "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
            for officer in officers
            if not (
                "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,) in seen or seen.add(
                    "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
                )
            )
        ]
        return result

    def get_open_email(self):
        template = 'emails/session_open.txt'
        context = {'session': self}
        subject = "[Barberscore] {0} Session is OPEN".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_district_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email

    def send_open_email(self):
        email = self.get_open_email()
        return email.send()


    def get_close_email(self):
        template = 'emails/session_close.txt'
        context = {'session': self}
        subject = "[Barberscore] {0} Session is CLOSED".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_district_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email


    def send_close_email(self):
        email = self.get_close_email()
        return email.send()


    def get_verify_email(self):
        template = 'emails/session_verify.txt'
        approved_entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        ).order_by('draw')
        context = {
            'session': self,
            'approved_entries': approved_entries,
        }
        subject = "[Barberscore] {0} Session Draw".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_participant_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email

    def send_verify_email(self):
        email = self.get_verify_email()
        return email.send()


    def get_verify_report_email(self):
        template = 'emails/session_verify_report.txt'
        context = {
            'session': self,
        }
        subject = "[Barberscore] {0} Session Draft Reports".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        attachments = []
        if self.drcj_report:
            xlsx = self.drcj_report.file
        else:
            xlsx = self.get_drcj()
        file_name = '{0} Session DRCJ Report DRAFT.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        if self.legacy_report:
            xlsx = self.legacy_report.file
        else:
            xlsx = self.get_legacy()
        file_name = '{0} Session Legacy Report DRAFT.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            attachments=attachments,
        )
        return email

    def send_verify_report_email(self):
        email = self.get_verify_report_email()
        return email.send()


    def get_package_email(self):
        template = 'emails/session_package.txt'
        approved_entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        ).order_by('draw')
        context = {
            'session': self,
            'approved_entries': approved_entries,
        }
        subject = "[Barberscore] {0} Session Starting".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_participant_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email

    def send_package_email(self):
        email = self.get_package_email()
        return email.send()


    def get_package_report_email(self):
        template = 'emails/session_package_report.txt'
        context = {
            'session': self,
        }
        subject = "[Barberscore] {0} Session FINAL Reports".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()

        attachments = []
        if self.drcj_report:
            xlsx = self.drcj_report.file
        else:
            xlsx = self.get_drcj()
        file_name = '{0} Session DRCJ Report FINAL.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        if self.legacy_report:
            xlsx = self.legacy_report.file
        else:
            xlsx = self.get_legacy()
        file_name = '{0} Session Legacy Report FINAL.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            attachments=attachments,
        )
        return email


    def send_package_report_email(self):
        email = self.get_package_report_email()
        return email.send()


    # Session Permissions
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
            'DRCJ',
        ]
        return any([item in roles for item in request.user.roles])


    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        if self.status >= self.STATUS.finished:
            return False
        return any([
            'SCJC' in request.user.roles,
            self.owners.filter(id__contains=request.user.id),
        ])

    # Session Conditions
    def can_reset(self):
        if self.status <= self.STATUS.built:
            return True
        return False

    def can_build(self):
        return all([
            self.num_rounds,
        ])

    def can_open(self):
        try:
            return all([
                # self.convention.open_date <= datetime.date.today(),
                self.contests.filter(status=self.contests.model.STATUS.included),
            ])
        except TypeError:
            return False

    def can_close(self):
        return True
        Entry = apps.get_model('smanager.entry')
        return all([
            self.convention.close_date < datetime.date.today(),
            self.entries.all(),
            self.entries.exclude(
                status__in=[
                    Entry.STATUS.approved,
                    Entry.STATUS.withdrawn,
                ],
            ).count() == 0,
        ])

    def can_verify(self):
        Entry = apps.get_model('smanager.entry')
        return all([
            self.entries.filter(status=Entry.STATUS.approved).count() > 0,
            not self.entries.filter(
                status=Entry.STATUS.approved,
                draw__isnull=True,
            ),
        ])

    def can_finish(self):
        return all([
            not self.rounds.exclude(status=self.rounds.model.STATUS.published)
        ])

    # Session Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.new,
        conditions=[can_reset]
    )
    def reset(self, *args, **kwargs):
        self.drcj_report.delete()
        contests = self.contests.all()
        rounds = self.rounds.all()
        entries = self.entries.all()
        contests.delete()
        rounds.delete()
        entries.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        """Build session contests."""
        Award.objects.get_model('bhs.award')

        # Reset for indempotence
        self.reset()

        i = 0
        # Get all the active awards for the convention group
        awards = Award.filter(
            status=Award.STATUS.active,
            kind=self.kind,
            season=self.convention.season,
            # division__in=self.convention.divisions,
        ).order_by('tree_sort')
        if self.convention.divisions:
            awards = awards.filter(
                division__in=self.convention.divisions,
            ).order_by('tree_sort')
        for award in awards:
            # Create contests for each active award.
            # Could also do some logic here for more precision
            self.contests.create(
                status=self.contests.model.STATUS.included,
                award=award,
            )
        # Create the rounds for the session, along with default # spots
        # for next round.
        for i in range(self.num_rounds):
            num = i + 1
            kind = self.num_rounds - i
            if kind == 3: # Unique to International
                spots = 20
            elif num == 2 and kind != 1: # All Semis
                spots = 10
            else:
                spots = 0
            self.rounds.create(
                num=num,
                kind=kind,
                spots=spots,
            )
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.built,
        target=STATUS.opened,
        conditions=[can_open],
    )
    def open(self, *args, **kwargs):
        """Make session available for entry."""
        # Send notification for all public contests
        if not self.is_invitational:
            send_open_email_from_session.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.opened,
        target=STATUS.closed,
        conditions=[can_close]
    )
    def close(self, *args, **kwargs):
        """Make session unavailable and set initial draw."""
        # Remove orphaned entries
        entries = self.entries.filter(
            status=self.entries.model.STATUS.new,
        )
        for entry in entries:
            entry.delete()
        # Withdraw dangling invitations
        entries = self.entries.filter(
            status=self.entries.model.STATUS.invited,
        )
        for entry in entries:
            entry.withdraw()
            entry.save()
        # Set initial draw for all Approved entries.
        entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        ).order_by('?')
        i = 1
        for entry in entries:
            entry.draw = i
            entry.save()
            i += 1
        # Send notification for all public contests only
        if not self.is_invitational:
            send_close_email_from_session.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.closed],
        target=STATUS.verified,
        conditions=[
            can_verify,
        ],
    )
    def verify(self, *args, **kwargs):
        """Make draw public."""
        send_verify_email_from_session.delay(self)
        send_verify_report_email_from_session.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.verified,
        target=STATUS.packaged,
        conditions=[],
    )
    def package(self, *args, **kwargs):
        """Button up session and transfer to CA."""

        # Save final reports
        self.save_drcj()
        self.save_legacy()

        #  Create and send the reports
        send_package_email_from_session.delay(self)
        send_package_report_email_from_session.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.packaged, STATUS.finished],
        target=STATUS.finished,
        conditions=[can_finish],
    )
    def finish(self, *args, **kwargs):
        return
