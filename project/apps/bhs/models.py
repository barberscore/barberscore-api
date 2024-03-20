import uuid
import datetime
import operator
from io import BytesIO

# Third-Party
from model_utils import Choices
from django_fsm import FSMIntegerField
from model_utils.models import TimeStampedModel
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from phonenumber_field.modelfields import PhoneNumberField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from timezone_field import TimeZoneField
from docx import Document

# Django
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property
from django.conf import settings
from django.contrib.postgres.fields import DecimalRangeField
from django.contrib.postgres.fields import IntegerRangeField
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models import Case, When, Q, Count
from django.template.defaultfilters import pluralize

# First-Party
from .managers import ConventionManager
from .managers import AwardManager
from .managers import PersonManager
from .managers import GroupManager
from .managers import ChartManager

from .fields import LowerEmailField
from .fields import ImageUploadPath
from .fields import UploadPath
from .fields import DivisionsField

from apps.organizations.models import Organization

from .validators import validate_punctuation

from apps.salesforce.decorators import notification_user

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

    organization = models.ForeignKey(
        'organizations.Organization',
        related_name='+',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    DISTRICT = Choices(
        (110, 'bhs', 'BHS'),
        (200, 'car', 'CAR'),
        (205, 'csd', 'CSD'),
        (210, 'dix', 'DIX'),
        (215, 'evg', 'EVG'),
        (220, 'fwd', 'FWD'),
        (225, 'ill', 'ILL'),
        (230, 'jad', 'JAD'),
        (235, 'lol', 'LOL'),
        (240, 'mad', 'MAD'),
        (345, 'ned', 'NED'),
        (350, 'nsc', 'NSC'),
        (355, 'ont', 'ONT'),
        (360, 'pio', 'PIO'),
        (365, 'rmd', 'RMD'),
        (370, 'sld', 'SLD'),
        (375, 'sun', 'SUN'),
        (380, 'swd', 'SWD'),
        (430, 'hi', 'HI'),
    )

    district = models.IntegerField(
        choices=DISTRICT,
        null=True,
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

    is_novice = models.BooleanField(
        default=False,
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

    scope_range = DecimalRangeField(
        null=True,
        blank=True,
    )

    # Denormalizations
    tree_sort = models.IntegerField(
        # unique=True,
        blank=True,
        null=True,
        # editable=False,
    )

    # Internals
    objects = AwardManager()

    class Meta:
        pass

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

    def is_searchable(self):
        return bool(self.status == self.STATUS.active)

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
        return bool(request.user.roles.filter(
            name__in=[
                'SCJC',
                'CA',
                'ADM',
            ]
        ))

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return bool(request.user.roles.filter(
            name__in=[
                'SCJC',
                'CA',
                'ADM',
            ]
        ))

    # Transitions
    @notification_user
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Award."""
        return

    @notification_user
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Award."""
        return


class Chart(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-20, 'protected', 'Protected',),
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    title = models.CharField(
        max_length=255,
    )

    arrangers = models.CharField(
        max_length=255,
    )

    composers = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    lyricists = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    holders = models.TextField(
        blank=True,
        default='',
    )

    description = models.TextField(
        help_text="""
            Fun or interesting facts to share about the chart (ie, 'from Disney's Lion King, first sung by Elton John'.)""",
        blank=True,
        max_length=1000,
        default='',
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
        default='',
    )

    image = models.ImageField(
        upload_to=ImageUploadPath('image'),
        null=True,
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='charts',
    )

    @cached_property
    def nomen(self):
        return "{0} [{1}]".format(
            self.title,
            self.arrangers,
        )

    def is_searchable(self):
        return self.status == self.STATUS.active

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    @cached_property
    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return 'https://res.cloudinary.com/barberscore/image/upload/v1554830585/missing_image.jpg'


    # Internals
    objects = ChartManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_chart',
                fields=[
                    'title',
                    'arrangers',
                ]
            )
        ]

    class JSONAPIMeta:
        resource_name = "chart"

    def __str__(self):
        return self.nomen

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
            request.user.roles.filter(
                name__in=[
                    'SCJC',
                    'Librarian',
                    'CA',
                    'ADM',
                ],
            )
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.roles.filter(
                name__in=[
                    'SCJC',
                    'Librarian',
                    'CA',
                    'ADM',
                ],
            )
        ])

    # Transitions
    @notification_user
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Chart."""
        return

    @notification_user
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Chart."""
        return

    @notification_user
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.protected)
    def protect(self, *args, **kwargs):
        """Protect the Chart."""
        return


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (-5, 'cancelled', 'Cancelled',),
        (0, 'new', 'New',),
        (5, 'built', 'Built',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        related_name='org',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    name = models.CharField(
        max_length=255,
        default='Convention',
    )

    DISTRICT_FULL_NAMES = {
        110: "Barbershop Harmony Society",
        200: "Cardinal",
        205: "Central States",
        210: "Dixie",
        215: "Evergreen",
        220: "Far Western",
        225: "Illinois",
        230: "Johnny Appleseed",
        235: "Land 'O Lakes",
        240: "Mid-Atlantic",
        345: "Northeastern",
        350: "Carolinas",
        355: "Ontario",
        360: "Pioneer",
        365: "Rocky Mountain",
        370: "Seneca Land",
        375: "Sunshine",
        380: "Southwestern",
        430: "Harmony, Inc.",
    }

    DISTRICT = Choices(
        (110, 'bhs', 'BHS'),
        (200, 'car', 'CAR'),
        (205, 'csd', 'CSD'),
        (210, 'dix', 'DIX'),
        (215, 'evg', 'EVG'),
        (220, 'fwd', 'FWD'),
        (225, 'ill', 'ILL'),
        (230, 'jad', 'JAD'),
        (235, 'lol', 'LOL'),
        (240, 'mad', 'MAD'),
        (345, 'ned', 'NED'),
        (350, 'nsc', 'NSC'),
        (355, 'ont', 'ONT'),
        (360, 'pio', 'PIO'),
        (365, 'rmd', 'RMD'),
        (370, 'sld', 'SLD'),
        (375, 'sun', 'SUN'),
        (380, 'swd', 'SWD'),
        (430, 'hi', 'HI'),
    )

    district = models.IntegerField(
        choices=DISTRICT,
        null=True,
    )

    SEASON = Choices(
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
    for r in reversed(range(1939, (datetime.datetime.now().year + 11))):
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

    district_display_name = models.CharField(
        verbose_name='District Display Name',
        help_text="""
            Used to override the display of the district name/abbr in case of multi-district conventions.""",
        max_length=255,
        default='',
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

    image = models.ImageField(
        upload_to=UploadPath('image'),
        max_length=255,
        null=True,
        blank=True,
    )

    bbstix_report = models.FileField(
        upload_to=UploadPath('bbstix_report'),
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
        verbose_name="BBSTIX Report",
    )

    bbstix_practice_report = models.FileField(
        upload_to=UploadPath('bbstix_practice_report'),
        help_text="""This BBSTIX report include practice judge data.""",
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
        verbose_name="BBSTIX Report (with Practice Judges)",
    )

    # FKs
    persons = models.ManyToManyField(
        'Person',
        related_name='conventions',
        blank=True,
    )

    def get_default_owners():
        return False

    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conventions',
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='conventions',
    )

    # Internals
    objects = ConventionManager()

    @cached_property
    def nomen(self):
        district_display = ''
        if self.district_display_name:
            district_display = self.district_display_name
        elif self.district is not None:
            district_display = self.get_district_display()

        if self.organization is not None:
            return " ".join([
                self.organization.abbreviation,
                str(self.year),
                self.name,
            ])
        elif self.district == self.DISTRICT.bhs:
            return " ".join([
                district_display,
                str(self.year),
                self.name,
            ])
        return " ".join([
            district_display,
            self.get_season_display(),
            str(self.year),
            self.name,
        ])

    def is_searchable(self):
        return self.district

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    @cached_property
    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return 'https://res.cloudinary.com/barberscore/image/upload/v1554830585/missing_image.jpg'


    # Internals
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_convention',
                fields=[
                    'year',
                    'season',
                    'name',
                    'district',
                ]
            )
        ]

    class JSONAPIMeta:
        resource_name = "convention"

    def __str__(self):
        return self.nomen

    def clean(self):
        return

    def get_owners_emails(self):
        owners = self.owners.order_by(
            'last_name',
            'first_name',
        )
        return ["{0} <{1}>".format(x.name, x.email) for x in owners]

    def get_bbstix_report(self, include_practice=False):

        # if include_practice:
        #     print("include_practice is true")
        # else:
        #     print("include_practice is false")

        Round = apps.get_model('adjudication.round')
        Session = apps.get_model('registration.session')
        Appearance = apps.get_model('adjudication.appearance')
        Entry = apps.get_model('registration.entry')
        Contest = apps.get_model('registration.contest')
        Panelist = apps.get_model('adjudication.panelist')

        ## Build doc here!
        rows = []

        # Header
        rows.append(
            "BBSTIX, BHS, {0}".format(
                self.name,
            )
        )

        # Location
        rows.append(
            "{0} District, {1}, {2}".format(
                self.DISTRICT_FULL_NAMES[self.district],
                self.location,
                self.end_date.strftime("%B %d, %Y"),
            )
        )

        # Alphabetical sort order for Sessions by kind nomen
        subsession_order = []
        i = 1
        for kind_id, kind_name in sorted(Session.KIND, key=operator.itemgetter(1)):
            subsession_order.append(
                When(kind=kind_id, then=i)
            )
            i += 1

        sessions = Session.objects.filter(
            convention_id=self.id,
        ).annotate(
            subsession_order=Case(*subsession_order, output_field=models.IntegerField())
        ).order_by(
            'subsession_order'
        )

        # Alphabetical sort order for Rounds by kind nomen
        round_order = []
        i = 1
        for kind_id, kind_name in sorted(Round.KIND, key=operator.itemgetter(1)):
            round_order.append(
                When(kind=kind_id, then=i)
            )
            i += 1

        panel_records = []
        song_records = []
        penalty_records = []
        panel_count = 0

        # Subsession
        for id, session in enumerate(sessions):

            rounds = Round.objects.filter(
                session_id=session.id
            ).annotate(
                round_order=Case(*round_order, output_field=models.IntegerField())
            ).order_by(
                'round_order'
            )

            contests = Contest.objects.filter(
                session_id=session.id
            ).order_by(
                'name'
            )

            subsession_ids = {}
            session_contests = []

            i = 1
            for contest in contests:
                subsession_ids[str(contest.id)] = i
                session_contests.append(
                    '{0}={1} ({2})'.format(
                        i,
                        contest.name,
                        '{0} Round{1}'.format(
                            rounds.count(), 
                            pluralize(rounds.count()),
                        )
                    )
                )
                i += 1

            for r in rounds:
                appearances = Appearance.objects.filter(
                    round_id=r.id,
                    num__gt=0,
                    status__in=[
                        Appearance.STATUS.completed,
                        Appearance.STATUS.finished,
                        Appearance.STATUS.advanced
                    ],
                ).prefetch_related(
                    'songs__scores',
                    'songs__scores__panelist',
                ).order_by(
                    'num',
                )

                # Sessions & Rounds

                subsession = 'Subsessions: {0} {1} ({2})'.format(
                    Session.KIND[session.kind],
                    Round.KIND[r.kind],
                    appearances.count(),
                )

                rows.append(
                    '{0}, {1}'.format(
                        subsession,
                        ', '.join(session_contests),
                    )
                )

                # Panel
                panelists = Panelist.objects.filter(
                    round_id=r.id,
                    kind=Panelist.KIND.official,
                    category__gt=Panelist.CATEGORY.adm,
                ).order_by(
                    'num',
                )

                round_panel = []
                for panelist in panelists:
                    shortname = panelist.name.replace(panelist.last_name, "").strip()
                    round_panel.append(
                        '"{0} ({1})={2}, {3}"'.format(
                            panelist.num,
                            Panelist.CATEGORY_SHORT_NAMES[panelist.category],
                            panelist.last_name,
                            shortname,
                        )
                    )

                # Practice Judges
                if include_practice:
                    panelists = Panelist.objects.filter(
                        round_id=r.id,
                        kind=Panelist.KIND.practice,
                        category__gt=Panelist.CATEGORY.adm,
                    ).order_by(
                        'num',
                    )

                    for panelist in panelists:
                        round_panel.append(
                            '"{0} ({1})={2}, {3}"'.format(
                                panelist.num,
                                Panelist.CATEGORY_SHORT_NAMES[panelist.category],
                                panelist.last_name,
                                panelist.first_name,
                            )
                        )

                # Set judge panel count based on the first session...might need to alter for variable size panels.
                if id == 0:
                    panel_count = len(round_panel)

                panel_records.append(
                    'Panel - {0} {1}:, {2}'.format(
                        Session.KIND[session.kind],
                        Round.KIND[r.kind],
                        ', '.join(round_panel),
                    )
                )

                # Songs
                for appearance in appearances:

                    # Competing in which contests?
                    entry = Entry.objects.filter(
                        group_id=appearance.group_id,
                        session_id=session.id
                    ).first()

                    contest_entered = []
                    for entry_contest in entry.contests.all():
                        contest_entered.append(
                            str(subsession_ids[str(entry_contest.id)])
                        )
                    contest_entered.sort()

                    songs = appearance.songs.prefetch_related(
                        'scores',
                        'scores__panelist',
                    ).order_by(
                        'num',
                    )

                    song_num = 1
                    for song in songs:

                        # Include practice judge scores?
                        if include_practice:
                            scores = song.scores.order_by('panelist__num')
                        else:
                            scores = song.scores.filter(
                                panelist__kind=Panelist.KIND.official,
                            ).order_by('panelist__num')

                        # collect scores for this song
                        song_scores = []
                        for score in scores:
                            song_scores.append(
                                str(score.points)
                            )

                        # Song Record
                        song_records.append(
                            'Session: {0} {1}, "Contestant Name: {2}", "Subsessions: {3}", OA: {4}, Song Nbr: {5}, "Song Title: {6}", {7}'.format(
                                Session.KIND[session.kind],
                                Round.KIND[r.kind],
                                appearance.name,
                                ','.join(contest_entered),
                                appearance.num,
                                song_num,
                                song.title,
                                ", ".join(song_scores),
                            )
                        )

                        # Penalty Record
                        penalty_article_map = {
                            30: "V.A.2",
                            32: "IX.A.2.a",
                            34: "IX.A.2.b",
                            36: "IX.A.2.c",
                            38: "IX.A.2.d",
                            39: "IX.A.2.e",
                            40: "IX.A.3",
                            44: "IX.A.3.b",
                            48: "XI.A.1",
                            50: "X.B",
                        }

                        penalty_desc_map = {
                            30: "Repeating Substantial Portions of a Song",
                            32: "Instrumental Accompaniment",
                            34: "Chorus Exceeding 4-Part Texture",
                            36: "Excessive Melody Not in Inner Part",
                            38: "Lack of Characteristic Chord Progression",
                            39: "Excessive Lyrics < 4 parts",
                            40: "Primarily Patriotic/Religious Intent",
                            44: "Not in Good Taste",
                            48: "Non-members Performing on Stage",
                            50: "Sound Equipment or Electronic Enhancement",
                        }

                        if len(song.penalties):
                            for penalty_id in sorted(song.penalties):
                                penalty_records.append(
                                    '"Penalty", "Session: {0} {1}", "Contestant: {2}", OA: {3}, "Judge: ???", Song Nbr: {4}, "Rule: Article {5}", "Description: {6}", 5+'.format(
                                        Session.KIND[session.kind],
                                        Round.KIND[r.kind],
                                        appearance.name,
                                        appearance.num,
                                        song_num,
                                        penalty_article_map[penalty_id],
                                        penalty_desc_map[penalty_id],
                                    )
                                )

                        song_num += 1

        # Judge Count Record
        rows.append(
            "Judge Count: {0}".format(
                panel_count,
            )
        )

        # Panel Record
        for panel in panel_records:
            rows.append(
                panel
            )

        # Song Record
            # Session: Chorus Finals, "Contestant Name: Maple Leaf Chord Company", "Subsessions: 6", OA: 1, Song Nbr: 1, "Song Title: A Little Street Where Old Friends Meet", 65, 65, 67, 70, 64, 67
        for song in song_records:
            rows.append(
                song
            )

        # Penalty Record
            # "Penalty", "Session: Quartet Finals", "Contestant: Ripple Effect", OA: 4, "Judge: M01", Song Nbr: 2, "Rule: Article IX.A.2.e", "Description: Excessive Passages without Lyrics in 4 parts", 3
        for penalty in penalty_records:
            rows.append(
                penalty
            )

        # Combine the rows
        buff = '\r\n'.join(rows)

        content = ContentFile(buff)
        return content

    def save_bbstix_report(self):
        bbstix = self.get_bbstix_report()
        return self.bbstix_report.save('bbstix_report', bbstix)

    def save_bbstix_practice_report(self):
        bbstix = self.get_bbstix_report(include_practice=True)
        return self.bbstix_practice_report.save('bbstix_report', bbstix)

    def rounds_finalized(self, finalized=True):
        Session = apps.get_model('registration.session')
        Round = apps.get_model('adjudication.round')

        # Gather Convention Sessions
        sessions = Session.objects.filter(
            convention_id=self.id,
        )

        # Loop Sessions to access Rounds
        for id, session in enumerate(sessions):
            rounds = Round.objects.filter(
                session_id=session.id
            )

            # Loop Rounds to check status
            for r in rounds:
                if r.status < Round.STATUS.finalized:
                    finalized = False

        return finalized

    def base_filename(self):
        return '{0}{1}'.format(
            self.get_district_display(),
            self.start_date.strftime("%Y%m%d")
        )

    # Methods
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
            request.user.roles.filter(name__in=[
                'SCJC',
                'CA',
                'ADM',
                ]
            )
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.roles.filter(name__in=[
                'SCJC',
                'CA',
                'ADM',
            ])
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
            ])
        except TypeError:
            return False
        return False

    def can_deactivate(self):
        return

    # Convention Transitions
    @notification_user
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.new,
        conditions=[can_reset],
    )
    def reset(self, *args, **kwargs):
        return

    @notification_user
    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        """Build convention and related sessions."""
        Sessions = apps.get_model('registration.session')

        current_user = kwargs['by']

        # Reset for indempodence
        self.reset()

        # Build Sessions
        # print('---BUILD SESSIONS---')
        for kind in self.kinds:
            session = Sessions.objects.create(
                convention=self,
                name=self.name,
                district=self.district,
                divisions=self.divisions,
                year=self.year,
                season=self.season,
                panel=self.panel,
                kind=kind,
                open_date=self.open_date,
                close_date=self.close_date,
                start_date=self.start_date,
                end_date=self.end_date,
                venue_name=self.venue_name,
                location=self.location,
                timezone=self.timezone,
                image=self.image,
            )
            session.owners.add(*self.owners.all())
            session.save();
    
            # print('---BUILD CONTESTS FOR SESSION---')
            session.build(by=current_user)
            session.save();
        return

    @notification_user
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

    @notification_user
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


class Group(TimeStampedModel):
    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""The name of the quartet/chorus.""",
        max_length=255,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (-5, 'aic', 'AIC',),
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
        (46, 'vlq', "VLQ"),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group.
        """,
        choices=KIND,
    )

    GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    gender = models.IntegerField(
        help_text="""
            The gender of group.
        """,
        choices=GENDER,
        null=True,
        blank=True
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        related_name='+',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    DISTRICT = Choices(
        ('BHS', [
            (200, 'car', 'CAR'),
            (205, 'csd', 'CSD'),
            (210, 'dix', 'DIX'),
            (215, 'evg', 'EVG'),
            (220, 'fwd', 'FWD'),
            (225, 'ill', 'ILL'),
            (230, 'jad', 'JAD'),
            (235, 'lol', 'LOL'),
            (240, 'mad', 'MAD'),
            (345, 'ned', 'NED'),
            (350, 'nsc', 'NSC'),
            (355, 'ont', 'ONT'),
            (360, 'pio', 'PIO'),
            (365, 'rmd', 'RMD'),
            (370, 'sld', 'SLD'),
            (375, 'sun', 'SUN'),
            (380, 'swd', 'SWD'),
        ]),
        ('Associated', [
            (410, 'nxtgn', 'NxtGn'),
            (420, 'mbha', 'MBHA'),
            (430, 'hi', 'HI'),
            (440, 'sai', 'SAI'),
        ]),
        ('Affiliated', [
            (510, 'babs', 'BABS'),
            (515, 'bha', 'BHA'),
            (520, 'bhnz', 'BHNZ'),
            (525, 'bing', 'BinG'),
            (530, 'fabs', 'FABS'),
            (540, 'hhar', 'HHar'),
            (550, 'iabs', 'IABS'),
            (560, 'labbs', 'LABBS'),
            (565, 'sabs', 'SABS'),
            (570, 'snobs', 'SNOBS'),
            (575, 'spats', 'SPATS'),
        ]),
    )

    district = models.IntegerField(
        choices=DISTRICT,
        null=True,
        blank=True
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

    division = models.IntegerField(
        choices=DIVISION,
        null=True,
        blank=True,
    )

    bhs_id = models.IntegerField(
        verbose_name='BHS ID',
        blank=True,
        null=True,
        unique=True,
    )

    code = models.CharField(
        help_text="""
            Legacy Short-form code (chapters only).""",
        max_length=255,
        blank=True,
    )

    is_senior = models.BooleanField(
        verbose_name='Is Senior',
        help_text="""Qualifies as a Senior Group.  Must be set manually.""",
        default=False,
    )

    is_youth = models.BooleanField(
        verbose_name='Is Youth',
        help_text="""Qualifies as a Youth Group.  Must be set manually.""",
        default=False,
    )

    description = models.TextField(
        help_text="""
            A description of the group.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    source_id = models.CharField(
        verbose_name='Source ID',
        null=True,
        blank=True,
        max_length=100,
        unique=True,
        db_index=True,
    )

    image = models.ImageField(
        upload_to=ImageUploadPath('image'),
        null=True,
        blank=True,
    )


    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
        default='',
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
        blank=True,
    )

    # FKs
    charts = models.ManyToManyField(
        'Chart',
        related_name='groups',
        blank=True,
    )

    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='groups',
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='groups',
    )

    # Properties
    @cached_property
    def nomen(self):
        if self.kind is self.KIND.quartet:
            if self.bhs_id:
                suffix = "[{0}]".format(self.bhs_id)
            elif self.code:
                suffix = "({0})".format(self.code)
            else:
                suffix = ""
        else:
            suffix = "({0})".format(self.code)
        return "{0} {1}".format(self.name, suffix)

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    @cached_property
    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return 'https://res.cloudinary.com/barberscore/image/upload/v1554830585/missing_image.jpg'

    # def get_is_senior(self):
    #     if self.kind != self.KIND.quartet:
    #         raise ValueError('Must be quartet')
    #     Person = apps.get_model('bhs.person')
    #     midwinter = datetime.date(2020, 1, 11)
    #     persons = Person.objects.filter(
    #         members__group=self,
    #         members__status__gt=0,
    #     )
    #     if persons.count() > 4:
    #         return False
    #     all_over_55 = True
    #     total_years = 0
    #     for person in persons:
    #         try:
    #             years = int((midwinter - person.birth_date).days / 365)
    #         except TypeError:
    #             return False
    #         if years < 55:
    #             all_over_55 = False
    #         total_years += years
    #     if all_over_55 and (total_years >= 240):
    #         is_senior = True
    #     else:
    #         is_senior = False
    #     return is_senior



    # Internals
    objects = GroupManager()

    class Meta:
        verbose_name_plural = 'Groups'

    class JSONAPIMeta:
        resource_name = "group"

    def __str__(self):
        return self.nomen

    # Algolia
    def is_searchable(self):
        return self.status == self.STATUS.active

    def get_owner_ids(self):
        return list(self.owners.values_list('id', flat=True))


    def get_chart_ids(self):
        return list(self.charts.values_list('id', flat=True))


    def get_owners_emails(self):
        owners = self.owners.order_by(
            'last_name',
            'first_name',
        )
        return ["{0} <{1}>".format(x.name, x.email) for x in owners]

    def get_charts_nomens(self):
        charts = self.charts.order_by(
            'title',
        )
        return ["{0}".format(x.nomen) for x in charts]

    # Group Methods

    # def clean(self):
    #     if self.mc_pk and self.status == self.STATUS.active:
    #         if self.kind == self.KIND.international:
    #             if self.parent:
    #                 raise ValidationError("Toplevel must be Root")
    #         if self.kind in [
    #             self.KIND.district,
    #             self.KIND.noncomp,
    #             self.KIND.affiliate,
    #         ]:
    #             if self.parent.kind != self.KIND.international:
    #                 raise ValidationError("Districts must have International parent.")
    #         if self.kind in [
    #             self.KIND.chapter,
    #         ]:
    #             if self.parent.kind not in [
    #                 self.KIND.district,
    #             ]:
    #                 raise ValidationError("Chapter must have District parent.")
    #             if self.division and not self.parent.is_divided:
    #                     raise ValidationError("Non-divisionals should not have divisions.")
    #             if not self.division and self.parent.is_divided and not self.name.startswith("Frank Thorne") and self.bhs_id not in [505990, 505883, 505789, 505863, 505936, 505442]:
    #                     raise ValidationError("Divisionals should have divisions.")
    #             if self.division:
    #                 if self.parent.code == 'EVG' and not 10 <= self.division <= 50:
    #                         raise ValidationError("Division must be within EVG.")
    #                 elif self.parent.code == 'FWD' and not 60 <= self.division <= 100:
    #                         raise ValidationError("Division must be within FWD.")
    #                 elif self.parent.code == 'LOL' and not 110 <= self.division <= 150:
    #                         raise ValidationError("Division must be within LOL.")
    #                 elif self.parent.code == 'MAD' and not 160 <= self.division <= 200:
    #                         raise ValidationError("Division must be within MAD.")
    #                 elif self.parent.code == 'NED' and not 210 <= self.division <= 250:
    #                         raise ValidationError("Division must be within NED.")
    #                 elif self.parent.code == 'SWD' and not 260 <= self.division <= 290:
    #                         raise ValidationError("Division must be within SWD.")
    #         if self.kind in [
    #             self.KIND.chorus,
    #             self.KIND.vlq,
    #         ]:
    #             if self.parent.kind not in [
    #                 self.KIND.chapter,
    #             ]:
    #                 raise ValidationError("Chorus/VLQ must have Chapter parent.")
    #             if self.division and not self.parent.parent.is_divided:
    #                     raise ValidationError("Non-divisionals should not have divisions.")
    #             if not self.division and self.parent.parent.is_divided and not self.name.startswith("Frank Thorne") and self.bhs_id not in [505990, 505883, 505789, 505863, 505936, 505442]:
    #                     raise ValidationError("Divisionals should have divisions.")
    #             if self.division:
    #                 if self.parent.parent.code == 'EVG' and not 10 <= self.division <= 50:
    #                         raise ValidationError("Division must be within EVG.")
    #                 elif self.parent.parent.code == 'FWD' and not 60 <= self.division <= 100:
    #                         raise ValidationError("Division must be within FWD.")
    #                 elif self.parent.parent.code == 'LOL' and not 110 <= self.division <= 150:
    #                         raise ValidationError("Division must be within LOL.")
    #                 elif self.parent.parent.code == 'MAD' and not 160 <= self.division <= 200:
    #                         raise ValidationError("Division must be within MAD.")
    #                 elif self.parent.parent.code == 'NED' and not 210 <= self.division <= 250:
    #                         raise ValidationError("Division must be within NED.")
    #                 elif self.parent.parent.code == 'SWD' and not 260 <= self.division <= 290:
    #                         raise ValidationError("Division must be within SWD.")
    #         if self.kind in [
    #             self.KIND.quartet,
    #         ] and self.parent:
    #             if self.parent.kind not in [
    #                 self.KIND.district,
    #             ]:
    #                 raise ValidationError("Quartet must have District parent.")
    #             if self.division and not self.parent.is_divided:
    #                     raise ValidationError("Non-divisionals should not have divisions.")
    #             if not self.division and self.parent.is_divided and not self.name.startswith("Frank Thorne") and self.bhs_id not in [505990, 505883, 505789, 505863, 505936, 505442]:
    #                     raise ValidationError("Divisionals should have divisions.")
    #             if self.division:
    #                 if self.parent.code == 'EVG' and not 10 <= self.division <= 50:
    #                         raise ValidationError("Division must be within EVG.")
    #                 elif self.parent.code == 'FWD' and not 60 <= self.division <= 100:
    #                         raise ValidationError("Division must be within FWD.")
    #                 elif self.parent.code == 'LOL' and not 110 <= self.division <= 150:
    #                         raise ValidationError("Division must be within LOL.")
    #                 elif self.parent.code == 'MAD' and not 160 <= self.division <= 200:
    #                         raise ValidationError("Division must be within MAD.")
    #                 elif self.parent.code == 'NED' and not 210 <= self.division <= 250:
    #                         raise ValidationError("Division must be within NED.")
    #                 elif self.parent.code == 'SWD' and not 260 <= self.division <= 290:
    #                         raise ValidationError("Division must be within SWD.")
    #     return

    # Group Permissions
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
        return bool(request.user.roles.filter(
            name__in=[
                'SCJC',
                'Librarian',
                'Manager',
                'CA',
                'ADM',
            ]
        ))

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.roles.filter(
                name__in=[
                    'SCJC',
                    'Librarian',
                    'CA',
                    'ADM',
                ]
            ),
            request.user in self.owners.all(),
        ])

    # Conditions:
    def can_activate(self):
        return

    # Transitions
    @notification_user
    @fsm_log_by
    @fsm_log_description
    @transition(
        field=status,
        source=[
            STATUS.active,
            STATUS.inactive,
            STATUS.new,
        ],
        target=STATUS.active,
        conditions=[
            can_activate,
        ]
    )
    def activate(self, description=None, *args, **kwargs):
        """Activate the Group."""
        self.denormalize()
        return

    @notification_user
    @fsm_log_by
    @fsm_log_description
    @transition(
        field=status,
        source=[
            STATUS.active,
            STATUS.inactive,
            STATUS.new,
        ],
        target=STATUS.inactive,
    )
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Group."""
        return


class Person(TimeStampedModel):
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

    name = models.CharField(
        help_text="""
            The common name of the person.""",
        max_length=255,
        validators=[
            validate_punctuation,
        ],
    )

    first_name = models.CharField(
        help_text="""
            The first name of the person.""",
        max_length=255,
        validators=[
            validate_punctuation,
        ],
    )

    last_name = models.CharField(
        help_text="""
            The last name of the person.""",
        max_length=255,
        validators=[
            validate_punctuation,
        ],
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        blank=True,
        null=True,
    )

    GENDER = Choices(
        (10, 'male', 'Male'),
        (20, 'female', 'Female'),
    )

    gender = models.IntegerField(
        choices=GENDER,
        blank=True,
        null=True,
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        related_name='+',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    DISTRICT = Choices(
        (110, 'bhs', 'BHS'),
        (200, 'car', 'CAR'),
        (205, 'csd', 'CSD'),
        (210, 'dix', 'DIX'),
        (215, 'evg', 'EVG'),
        (220, 'fwd', 'FWD'),
        (225, 'ill', 'ILL'),
        (230, 'jad', 'JAD'),
        (235, 'lol', 'LOL'),
        (240, 'mad', 'MAD'),
        (345, 'ned', 'NED'),
        (350, 'nsc', 'NSC'),
        (355, 'ont', 'ONT'),
        (360, 'pio', 'PIO'),
        (365, 'rmd', 'RMD'),
        (370, 'sld', 'SLD'),
        (375, 'sun', 'SUN'),
        (380, 'swd', 'SWD'),
        (430, 'hi', 'HI'),
    )

    district = models.IntegerField(
        choices=DISTRICT,
        null=True,
        blank=True,
    )

    email = LowerEmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
    )

    address = models.TextField(
        help_text="""
            The complete address of the resource.""",
        max_length=1000,
        blank=True,
        default='',
    )

    home_phone = PhoneNumberField(
        help_text="""
            The home phone number of the resource.  Include country code.""",
        blank=True,
    )

    work_phone = PhoneNumberField(
        help_text="""
            The work phone number of the resource.  Include country code.""",
        blank=True,
    )

    cell_phone = PhoneNumberField(
        help_text="""
            The cell phone number of the resource.  Include country code.""",
        blank=True,
    )

    airports = ArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=3,
        ),
        blank=True,
        null=True,
        default=list,
    )

    description = models.TextField(
        help_text="""
            A bio of the person.  Max 1000 characters.""",
        max_length=1000,
        blank=True,
        default='',
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
        default='',
    )

    bhs_id = models.IntegerField(
        blank=True,
        null=True,
    )

    source_id = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        unique=True,
        db_index=True,
    )

    image = models.ImageField(
        upload_to=ImageUploadPath('image'),
        null=True,
        blank=True,
    )

    # Relations
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='persons',
        blank=True,

    )

    statelogs = GenericRelation(
        StateLog,
        related_query_name='persons',
    )

    # Properties
    @cached_property
    def nomen(self):
        if self.bhs_id:
            suffix = "[{0}]".format(self.bhs_id)
        else:
            suffix = ""
        return "{0} {1}".format(
            self.name,
            suffix
        )

    def is_searchable(self):
        return True

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    @cached_property
    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return 'https://res.cloudinary.com/barberscore/image/upload/v1554830585/missing_image.jpg'

    @cached_property
    def initials(self):
        return "{0}{1}".format(
            self.first_name[0].upper(),
            self.last_name[0].upper(),
        )


    # Internals
    objects = PersonManager()

    class Meta:
        verbose_name_plural = 'Persons'

    class JSONAPIMeta:
        resource_name = "person"

    def clean(self):
        pass

    def __str__(self):
        return self.nomen

    # Person Methods


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
        return bool(request.user.roles.filter(
            name__in=[
                'SCJC',
                'CA',
                'ADM',
            ]
        ))

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return bool(request.user.roles.filter(
            name__in=[
                'SCJC',
                'CA',
                'ADM',
            ]
        ))

    # Transitions
    @notification_user
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Person."""
        return

    @notification_user
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Person."""
        return
