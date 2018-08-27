# Standard Libary
import datetime
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

# Django
from django.apps import apps
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.urls import reverse

# First-Party
from api.managers import GroupManager
from api.fields import UploadPath
from api.fields import LowerEmailField


log = logging.getLogger(__name__)


class Group(TimeStampedModel):
    AIC = {
        "501972": "Main Street",
        "501329": "Forefront",
        "500922": "Instant Classic",
        "304772": "Musical Island Boys",
        "500000": "Masterpiece",
        "501150": "Ringmasters",
        "317293": "Old School",
        "286100": "Storm Front",
        "500035": "Crossroads",
        "297201": "OC Times",
        "299233": "Max Q",
        "302244": "Vocal Spectrum",
        "299608": "Realtime",
        "6158": "Gotcha!",
        "2496": "Power Play",
        "276016": "Four Voices",
        "5619": "Michigan Jake",
        "6738": "Platinum",
        "3525": "FRED",
        "5721": "Revival",
        "2079": "Yesteryear",
        "2163": "Nightlife",
        "4745": "Marquis",
        "3040": "Joker's Wild",
        "1259": "Gas House Gang",
        "2850": "Keepsake",
        "1623": "The Ritz",
        "3165": "Acoustix",
        "1686": "Second Edition",
        "492": "Chiefs of Staff",
        "1596": "Interstate Rivals",
        "1654": "Rural Route 4",
        "406": "The New Tradition",
        "1411": "Rapscallions",
        "1727": "Side Street Ramblers",
        "545": "Classic Collection",
        "490": "Chicago News",
        "329": "Boston Common",
        "4034": "Grandma's Boys",
        "318": "Bluegrass Student Union",
        "362": "Most Happy Fellows",
        "1590": "Innsiders",
        "1440": "Happiness Emporium",
        "1427": "Regents",
        "627": "Dealer's Choice",
        "1288": "Golden Staters",
        "1275": "Gentlemen's Agreement",
        "709": "Oriole Four",
        "711": "Mark IV",
        "2047": "Western Continentals",
        "1110": "Four Statesmen",
        "713": "Auto Towners",
        "715": "Four Renegades",
        "1729": "Sidewinders",
        "718": "Town and Country 4",
        "719": "Gala Lads",
        "1871": "The Suntones",
        "722": "Evans Quartet",
        "724": "Four Pitchikers",
        "726": "Gaynotes",
        "729": "Lads of Enchantment",
        "731": "Confederates",
        "732": "Four Hearsemen",
        "736": "The Orphans",
        "739": "Vikings",
        "743": "Four Teens",
        "746": "Schmitt Brothers",
        "748": "Buffalo Bills",
        "750": "Mid-States Four",
        "753": "Pittsburghers",
        "756": "Doctors of Harmony",
        "759": "Garden State Quartet",
        "761": "Misfits",
        "764": "Harmony Halls",
        "766": "Four Harmonizers",
        "770": "Elastic Four",
        "773": "Chord Busters",
        "775": "Flat Foot Four",
        "776": "Bartlesville Barflies",
    }
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.
        """,
        max_length=255,
        default='UNKNOWN',
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
        ('International', [
            (1, 'international', "International"),
        ]),
        ('District', [
            (11, 'district', "District"),
            (12, 'noncomp', "Noncompetitive"),
            (13, 'affiliate', "Affiliate"),
        ]),
        ('Division', [
            (21, 'division', "Division"),
        ]),
        ('Chapter', [
            (30, 'chapter', "Chapter"),
        ]),
        ('Group', [
            (32, 'chorus', "Chorus"),
            (41, 'quartet', "Quartet"),
        ]),
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
        default=GENDER.male,
    )

    code = models.CharField(
        help_text="""
            Short-form code.""",
        max_length=255,
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
            The geographical location of the resource.""",
        max_length=255,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the resource.""",
        blank=True,
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'@([A-Za-z0-9_]+)',
                message="""
                    Must be a single Twitter handle
                    in the form `@twitter_handle`.
                """,
            ),
        ],
    )

    email = LowerEmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
    )

    phone = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
    )

    image = models.ImageField(
        upload_to=UploadPath(),
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A description of the group.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    bhs_id = models.IntegerField(
        # unique=True,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
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

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=True,
        db_index=True,
    )

    # FKs
    parent = models.ForeignKey(
        'Group',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    # Denormalizations
    tree_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    international = models.TextField(
        help_text="""
            The denormalized international group.""",
        blank=True,
        max_length=255,
    )

    district = models.TextField(
        help_text="""
            The denormalized district group.""",
        blank=True,
        max_length=255,
    )

    division = models.TextField(
        help_text="""
            The denormalized division group.""",
        blank=True,
        max_length=255,
    )

    chapter = models.TextField(
        help_text="""
            The denormalized chapter group.""",
        blank=True,
        max_length=255,
    )

    is_senior = models.BooleanField(
        help_text="""Qualifies as a Senior Group.  This is set once, at creation.  If the group 'ages' into Senior status that needs to be edited manually here.""",
        default=False,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='groups',
    )

    # Properties
    @cached_property
    def nomen(self):
        if self.bhs_id:
            suffix = "[{0}]".format(self.bhs_id)
        else:
            suffix = "[No BHS ID]"
        full = "{0} {1}".format(
            self.name,
            suffix,
        )
        return " ".join(full.split())

    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

    # Methods
    def is_active(self):
        # For Algolia indexing
        return bool(self.status == self.STATUS.active)

    # Internals
    objects = GroupManager()

    class Meta:
        ordering = ['tree_sort']
        verbose_name_plural = 'groups'

    class JSONAPIMeta:
        resource_name = "group"

    def __str__(self):
        return self.nomen

    def clean(self):
        if self.mc_pk and self.status == self.STATUS.active:
            if self.kind == self.KIND.international:
                if self.parent:
                    raise ValidationError("Toplevel must be Root")
            else:
                if not self.parent:
                    raise ValidationError("Non-Root must have parent")
            if self.kind in [
                self.KIND.district,
                self.KIND.noncomp,
                self.KIND.affiliate,
            ]:
                if self.parent.kind != self.KIND.international:
                    raise ValidationError("Districts must have International parent.")
            if self.kind in [
                self.KIND.division,
            ]:
                if self.parent.kind != self.KIND.district:
                    raise ValidationError("Divisions must have District parent.")
            if self.kind in [
                self.KIND.chapter,
            ]:
                if self.parent.kind not in [
                    self.KIND.district,
                    self.KIND.division,
                ]:
                    raise ValidationError("Chapter must have District or Division parent.")
            if self.kind in [
                self.KIND.chorus,
            ]:
                if self.parent.kind not in [
                    self.KIND.chapter,
                ]:
                    raise ValidationError("Chorus must have Chapter parent.")
            if self.kind in [
                self.KIND.quartet,
            ]:
                if self.parent.kind not in [
                    self.KIND.district,
                    self.KIND.division,
                ]:
                    raise ValidationError("Quartet must have District or Division parent.")
        return

    # Methods
    def denormalize(self):
        parent = self.parent
        if not parent:
            self.international = ""
            self.district = ""
            self.division = ""
            self.chapter = ""
        else:
            international = parent
            if international.kind >= self.KIND.international:
                try:
                    while international.kind != self.KIND.international:
                        international = international.parent
                    self.international = international.code
                except AttributeError:
                    self.international = ""
            else:
                self.international = ""
            district = parent
            if district.kind >= self.KIND.district:
                try:
                    while district.kind not in [
                        self.KIND.district,
                        self.KIND.noncomp,
                        self.KIND.affiliate,
                    ]:
                        district = district.parent
                    self.district = district.code
                except AttributeError:
                    self.district = ""
            else:
                self.district = ""
            division = parent
            if division.kind >= self.KIND.division:
                try:
                    while division.kind != self.KIND.division:
                        division = division.parent
                    self.division = division.name
                except AttributeError:
                    self.division = ""
            else:
                self.division = ""
            chapter = parent
            if chapter.kind >= self.KIND.chapter:
                try:
                    while chapter.kind != self.KIND.chapter:
                        chapter = chapter.parent
                    self.chapter = chapter.name
                except AttributeError:
                    self.chapter = ""
            else:
                self.chapter = ""

    def get_is_senior(self):
        if self.kind != self.KIND.quartet:
            raise ValueError('Must be quartet')
        Person = apps.get_model('api.person')
        midwinter = datetime.date(2019, 1, 26)
        persons = Person.objects.filter(
            members__group=self,
            members__status__gt=0,
        )
        if persons.count() > 4:
            return False
        all_over_55 = True
        total_years = 0
        for person in persons:
            years = int((midwinter - person.birth_date).days / 365)
            if years < 55:
                all_over_55 = False
            total_years += years
        if all_over_55 and (total_years >= 240):
            is_senior = True
        else:
            is_senior = False
        return is_senior

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
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.officers.filter(
                    person__user=request.user,
                    status__gt=0,
                ),
                self.status > 0,
                self.mc_pk == None,
            ])
        ])

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source=[
        STATUS.active,
        STATUS.inactive,
        STATUS.new,
    ], target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Group."""
        self.denormalize()
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source=[
        STATUS.active,
        STATUS.inactive,
        STATUS.new,
    ], target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Group."""
        return
