import uuid
import datetime

# Third-Party
from model_utils import Choices
from django_fsm import FSMIntegerField
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.apps import apps
from django.core.files.base import ContentFile
from django.conf import settings

# First-Party
from .managers import HumanManager
from .managers import JoinManager
from .managers import RoleManager
from .managers import StructureManager

from .managers import PersonManager
from .managers import GroupManager
from .managers import MemberManager
from .managers import OfficerManager
from .managers import ChartManager

from .fields import ValidatedPhoneField
from .fields import LowerEmailField
from .fields import ReasonableBirthDate
from .fields import VoicePartField
from .fields import NoPunctuationCharField
from .fields import ImageUploadPath


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

    prefix = models.CharField(
        help_text="""
            The prefix of the person.""",
        max_length=255,
        blank=True,
        default='',
    )

    first_name = models.CharField(
        help_text="""
            The first name of the person.""",
        max_length=255,
        editable=False,
    )

    middle_name = models.CharField(
        help_text="""
            The middle name of the person.""",
        max_length=255,
        editable=False,
    )

    last_name = models.CharField(
        help_text="""
            The last name of the person.""",
        max_length=255,
        editable=False,
    )

    nick_name = models.CharField(
        help_text="""
            The nickname of the person.""",
        max_length=255,
        editable=False,
    )

    suffix = models.CharField(
        help_text="""
            The suffix of the person.""",
        max_length=255,
        blank=True,
        default='',
    )

    birth_date = models.DateField(
        null=True,
        editable=False,
    )

    spouse = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
        blank=True,
        default='',
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        null=True,
        editable=False,
    )

    mon = models.IntegerField(
        help_text="""
            Men of Note.""",
        null=True,
        editable=False,
    )

    GENDER = Choices(
        (10, 'male', 'Male'),
        (20, 'female', 'Female'),
    )

    gender = models.IntegerField(
        choices=GENDER,
        null=True,
        editable=False,
    )

    district = models.CharField(
        help_text="""
            District (used primarily for judges.)""",
        max_length=10,
        blank=True,
        default='',
    )

    is_deceased = models.BooleanField(
        default=False,
        editable=False,
    )
    is_honorary = models.BooleanField(
        default=False,
        editable=False,
    )
    is_suspended = models.BooleanField(
        default=False,
        editable=False,
    )
    is_expelled = models.BooleanField(
        default=False,
        editable=False,
    )
    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
        default='',
    )

    email = LowerEmailField(
        help_text="""
            The contact email of the resource.""",
        null=True,
        editable=False,
    )

    address = models.TextField(
        help_text="""
            The complete address of the resource.""",
        blank=True,
        max_length=1000,
        default='',
    )

    home_phone = PhoneNumberField(
        help_text="""
            The home phone number of the resource.  Include country code.""",
        editable=False,
    )

    work_phone = PhoneNumberField(
        help_text="""
            The work phone number of the resource.  Include country code.""",
        editable=False,
    )

    cell_phone = PhoneNumberField(
        help_text="""
            The cell phone number of the resource.  Include country code.""",
        editable=False,
    )


    airports = ArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=3,
        ),
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
            A bio of the person.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
        default='',
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
        default='',
    )

    bhs_id = models.IntegerField(
        editable=False,
    )

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=True,
        db_index=True,
    )

    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    statelogs = GenericRelation(
        StateLog,
        related_query_name='persons',
    )

    # Properties
    def is_active(self):
        # For Algolia indexing
        return bool(
            self.members.filter(group__bhs_id=1)
        )

    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

    @cached_property
    def nomen(self):
        if self.nick_name:
            nick = "({0})".format(self.nick_name)
        else:
            nick = ""
        if self.bhs_id:
            suffix = "[{0}]".format(self.bhs_id)
        else:
            suffix = "[No BHS ID]"
        full = "{0} {1} {2} {3} {4}".format(
            self.first_name,
            self.middle_name,
            self.last_name,
            nick,
            suffix,
        )
        return " ".join(full.split())

    @cached_property
    def full_name(self):
        if self.nick_name:
            nick = "({0})".format(self.nick_name)
        else:
            nick = ""
        full = "{0} {1} {2} {3}".format(
            self.first_name,
            self.middle_name,
            self.last_name,
            nick,
        )
        return " ".join(full.split())

    @cached_property
    def common_name(self):
        if self.nick_name:
            first = self.nick_name
        else:
            first = self.first_name
        return "{0} {1}".format(first, self.last_name)

    @cached_property
    def sort_name(self):
        return "{0}, {1}".format(self.last_name, self.first_name)

    @cached_property
    def initials(self):
        if self.nick_name:
            first = self.nick_name[0].upper()
        else:
            first = self.first_name[0].upper()
        return "{0}{1}".format(
            first,
            self.last_name[0].upper(),
        )

    @cached_property
    def current_through(self):
        try:
            current_through = self.members.get(
                group__bhs_id=1,
            ).end_date
        except self.members.model.DoesNotExist:
            current_through = None
        return current_through

    @cached_property
    def current_status(self):
        today = now().date()
        if self.current_through:
            if self.current_through >= today:
                return True
            return False
        return True

    @cached_property
    def current_district(self):
        return bool(
            self.members.filter(
                group__kind=11, # hardcoded for convenience
                status__gt=0,
            )
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
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Person."""
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Person."""
        return


class Group(TimeStampedModel):
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
        ('Chapter', [
            (30, 'chapter', "Chapter"),
        ]),
        ('Group', [
            (32, 'chorus', "Chorus"),
            (41, 'quartet', "Quartet"),
            (46, 'vlq', "VLQ"),
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
        blank=True,
        null=True,
        unique=True,
    )

    code = models.CharField(
        help_text="""
            Short-form code.""",
        max_length=255,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
    )

    email = LowerEmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
    )

    fax_phone = models.CharField(
        help_text="""
            The fax number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
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

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
    )

    twitter = models.URLField(
        help_text="""
            The twitter URL of the resource.""",
        blank=True,
    )

    youtube = models.URLField(
        help_text="""
            The youtube URL of the resource.""",
        blank=True,
        default='',
    )
    pinterest = models.URLField(
        help_text="""
            The pinterest URL of the resource.""",
        blank=True,
        default='',
    )
    flickr = models.URLField(
        help_text="""
            The flickr URL of the resource.""",
        blank=True,
        default='',
    )
    instagram = models.URLField(
        help_text="""
            The instagram URL of the resource.""",
        blank=True,
        default='',
    )
    soundcloud = models.URLField(
        help_text="""
            The soundcloud URL of the resource.""",
        blank=True,
        default='',
    )
    image = models.ImageField(
        upload_to=ImageUploadPath(),
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A description of the group.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    visitor_information = models.TextField(
        max_length=255,
        blank=True,
        default='',
    )

    participants = models.CharField(
        help_text='Director(s) or Members (listed TLBB)',
        max_length=255,
        blank=True,
        default='',
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
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

    chapter = models.TextField(
        help_text="""
            The denormalized chapter group.""",
        blank=True,
        max_length=255,
    )

    is_senior = models.BooleanField(
        help_text="""Qualifies as a Senior Group.  This can be set manually, but is denormlized nightly for quartets.""",
        default=False,
    )

    is_youth = models.BooleanField(
        help_text="""Qualifies as a Youth Group.  Must be set manually.""",
        default=False,
    )

    is_divided = models.BooleanField(
        help_text="""This district has divisions.""",
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
        if self.code:
            code = "({0})".format(self.code)
        else:
            code = ""
        full = [
            self.name,
            code,
            suffix,
        ]
        return " ".join(full)

    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

    # Methods
    def get_roster(self):
        Member = apps.get_model('bhs.member')
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'BHS ID',
            'First Name',
            'Last Name',
            'Expiration Date',
            'Status',
        ]
        ws.append(fieldnames)
        members = self.members.filter(
            status=Member.STATUS.active,
        ).order_by('person__last_name', 'person__first_name')
        for member in members:
            bhs_id = member.person.bhs_id
            first_name = member.person.first_name
            last_name = member.person.last_name
            expiration = member.person.current_through
            status = member.person.get_status_display()
            row = [
                bhs_id,
                first_name,
                last_name,
                expiration,
                status,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    def is_active(self):
        # For Algolia indexing
        return bool(self.status == self.STATUS.active)


    def get_officer_emails(self):
        officers = self.officers.filter(
            status__gt=0,
            person__email__isnull=False,
        ).order_by(
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


    # Internals
    objects = GroupManager()

    class Meta:
        ordering = ['tree_sort']
        verbose_name_plural = 'Groups'
        unique_together = (
            ('bhs_id', 'kind'),
        )

    class JSONAPIMeta:
        resource_name = "group"

    def __str__(self):
        return self.nomen

    def clean(self):
        if self.mc_pk and self.status == self.STATUS.active:
            if self.kind == self.KIND.international:
                if self.parent:
                    raise ValidationError("Toplevel must be Root")
            if self.kind in [
                self.KIND.district,
                self.KIND.noncomp,
                self.KIND.affiliate,
            ]:
                if self.parent.kind != self.KIND.international:
                    raise ValidationError("Districts must have International parent.")
            if self.kind in [
                self.KIND.chapter,
            ]:
                if self.parent.kind not in [
                    self.KIND.district,
                ]:
                    raise ValidationError("Chapter must have District parent.")
                if self.division and not self.parent.is_divided:
                        raise ValidationError("Non-divisionals should not have divisions.")
                if not self.division and self.parent.is_divided and not self.name.startswith("Frank Thorne") and self.bhs_id not in [505990, 505883, 505789, 505863, 505936, 505442]:
                        raise ValidationError("Divisionals should have divisions.")
                if self.division:
                    if self.parent.code == 'EVG' and not 10 <= self.division <= 50:
                            raise ValidationError("Division must be within EVG.")
                    elif self.parent.code == 'FWD' and not 60 <= self.division <= 100:
                            raise ValidationError("Division must be within FWD.")
                    elif self.parent.code == 'LOL' and not 110 <= self.division <= 150:
                            raise ValidationError("Division must be within LOL.")
                    elif self.parent.code == 'MAD' and not 160 <= self.division <= 200:
                            raise ValidationError("Division must be within MAD.")
                    elif self.parent.code == 'NED' and not 210 <= self.division <= 250:
                            raise ValidationError("Division must be within NED.")
                    elif self.parent.code == 'SWD' and not 260 <= self.division <= 290:
                            raise ValidationError("Division must be within SWD.")
            if self.kind in [
                self.KIND.chorus,
                self.KIND.vlq,
            ]:
                if self.parent.kind not in [
                    self.KIND.chapter,
                ]:
                    raise ValidationError("Chorus/VLQ must have Chapter parent.")
                if self.division and not self.parent.parent.is_divided:
                        raise ValidationError("Non-divisionals should not have divisions.")
                if not self.division and self.parent.parent.is_divided and not self.name.startswith("Frank Thorne") and self.bhs_id not in [505990, 505883, 505789, 505863, 505936, 505442]:
                        raise ValidationError("Divisionals should have divisions.")
                if self.division:
                    if self.parent.parent.code == 'EVG' and not 10 <= self.division <= 50:
                            raise ValidationError("Division must be within EVG.")
                    elif self.parent.parent.code == 'FWD' and not 60 <= self.division <= 100:
                            raise ValidationError("Division must be within FWD.")
                    elif self.parent.parent.code == 'LOL' and not 110 <= self.division <= 150:
                            raise ValidationError("Division must be within LOL.")
                    elif self.parent.parent.code == 'MAD' and not 160 <= self.division <= 200:
                            raise ValidationError("Division must be within MAD.")
                    elif self.parent.parent.code == 'NED' and not 210 <= self.division <= 250:
                            raise ValidationError("Division must be within NED.")
                    elif self.parent.parent.code == 'SWD' and not 260 <= self.division <= 290:
                            raise ValidationError("Division must be within SWD.")
            if self.kind in [
                self.KIND.quartet,
            ] and self.parent:
                if self.parent.kind not in [
                    self.KIND.district,
                ]:
                    raise ValidationError("Quartet must have District parent.")
                if self.division and not self.parent.is_divided:
                        raise ValidationError("Non-divisionals should not have divisions.")
                if not self.division and self.parent.is_divided and not self.name.startswith("Frank Thorne") and self.bhs_id not in [505990, 505883, 505789, 505863, 505936, 505442]:
                        raise ValidationError("Divisionals should have divisions.")
                if self.division:
                    if self.parent.code == 'EVG' and not 10 <= self.division <= 50:
                            raise ValidationError("Division must be within EVG.")
                    elif self.parent.code == 'FWD' and not 60 <= self.division <= 100:
                            raise ValidationError("Division must be within FWD.")
                    elif self.parent.code == 'LOL' and not 110 <= self.division <= 150:
                            raise ValidationError("Division must be within LOL.")
                    elif self.parent.code == 'MAD' and not 160 <= self.division <= 200:
                            raise ValidationError("Division must be within MAD.")
                    elif self.parent.code == 'NED' and not 210 <= self.division <= 250:
                            raise ValidationError("Division must be within NED.")
                    elif self.parent.code == 'SWD' and not 260 <= self.division <= 290:
                            raise ValidationError("Division must be within SWD.")
        return

    # Methods
    def denormalize(self):
        parent = self.parent
        if not parent:
            self.international = ""
            self.district = ""
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
        Person = apps.get_model('bhs.person')
        midwinter = datetime.date(2020, 1, 11)
        persons = Person.objects.filter(
            members__group=self,
            members__status__gt=0,
        )
        if persons.count() > 4:
            return False
        all_over_55 = True
        total_years = 0
        for person in persons:
            try:
                years = int((midwinter - person.birth_date).days / 365)
            except TypeError:
                return False
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
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Conditions:
    def can_activate(self):
        return all([
            bool(self.officers.filter(status__gt=0)),
        ])

    # Transitions
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


class Member(TimeStampedModel):
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
        default=STATUS.new,
    )

    PART = Choices(
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

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=False,
        db_index=True,
    )

    # Properties
    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

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

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='members',
    )

    # Internals
    objects = MemberManager()

    class Meta:
        unique_together = (
            ('group', 'person',),
        )
        verbose_name_plural = 'Members'

    class JSONAPIMeta:
        resource_name = "member"

    def __str__(self):
        return str(self.id)

    def clean(self):
        return

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
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Member."""
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Member."""
        return


class Officer(TimeStampedModel):
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
        default=STATUS.new,
    )

    OFFICE = Choices(
        ('International', [
            (100, 'scjc_chair', "SCJC Chair"),
            (110, 'scjc_past', "SCJC Chair Past"),
            (120, 'scjc_ca', "SCJC CA"),
            (130, 'scjc_mus', "SCJC MUS"),
            (140, 'scjc_per', "SCJC PER"),
            (150, 'scjc_sng', "SCJC SNG"),
            (160, 'scjc_chart', "SCJC Chart"),
            (170, 'scjc_admin', "SCJC Admin"),
            (230, 'judge_ca', "JUDGE CA"),
            (240, 'judge_mus', "JUDGE MUS"),
            (250, 'judge_per', "JUDGE PER"),
            (260, 'judge_sng', "JUDGE SNG"),
            (270, 'candidate_ca', "CANDIDATE CA"),
            (280, 'candidate_mus', "CANDIDATE MUS"),
            (290, 'candidate_per', "CANDIDATE PER"),
            (295, 'candidate_sng', "CANDIDATE SNG"),
        ]),
        ('District', [
            (210, 'drcj', "DRCJ"),
            (220, 'drcj_asst', "DRCJ Assistant"),
        ]),
        ('Chapter', [
            (310, 'chapter_pres', "CPRES"),
            (320, 'chapter_sec', "CSEC"),
        ]),
        ('Chorus', [
            (330, 'chorus_dir', "KDIR"),
            (340, 'chorus_asst', "KASS"),
            (350, 'chorus_man', "KMAN"),
        ]),
        ('Quartet', [
            (410, 'quartet_admin', "QADM"),
        ]),
    )

    office = models.IntegerField(
        choices=OFFICE,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=False,
        db_index=True,
    )

    # FKs
    person = models.ForeignKey(
        'Person',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='officers',
    )

    objects = OfficerManager()

    # Properties
    @cached_property
    def is_mc(self):
        return bool(self.mc_pk)

    # Internals
    class Meta:
        unique_together = (
            ('group', 'person', 'office'),
        )
        verbose_name_plural = 'Officers'

    class JSONAPIMeta:
        resource_name = "officer"

    def __str__(self):
        return str(self.id)

    def clean(self):
        pass
        # if self.group.kind != self.group.KIND.vlq:
        #     if self.office.kind != self.group.kind:
        #         raise ValidationError({
        #             'office': 'Office does not match Group Type.',
        #         })
        # else:
        #     if self.office.code != self.office.CODE.chorus_man:
        #         raise ValidationError({
        #             'office': 'VLQ officers must be Chorus Managers.',
        #         })

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
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
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
    )

    lyricists = models.CharField(
        max_length=255,
    )

    holders = models.TextField(
        blank=True,
    )

    description = models.TextField(
        help_text="""
            Fun or interesting facts to share about the chart (ie, 'from Disney's Lion King, first sung by Elton John'.)""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
    )

    image = models.ImageField(
        upload_to=ImageUploadPath(),
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
        return bool(self.status == self.STATUS.active)

    # Internals
    objects = ChartManager()

    class Meta:
        unique_together = (
            ('title', 'arrangers',)
        )

    class JSONAPIMeta:
        resource_name = "chart"

    def __str__(self):
        return "{0} [{1}]".format(
            self.title,
            self.arrangers,
        )

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
        roles = [
            'SCJC',
            'Librarian',
        ]
        return any(item in roles for item in request.user.roles)

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        roles = [
            'SCJC',
            'Librarian',
        ]
        return any(item in roles for item in request.user.roles)

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Chart."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Chart."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.protected)
    def protect(self, *args, **kwargs):
        """Protect the Chart."""
        return


class Repertory(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
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
        default=STATUS.active,
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

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='repertories',
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
        roles = [
            'SCJC',
            'DRCJ',
            'CA',
            'Librarian',
        ]
        return any([
            [item in roles for item in request.user.roles],
            self.group.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        roles = [
            'SCJC',
            'DRCJ',
            'Librarian',
            'Manager',
        ]
        return any([item in roles for item in request.user.roles])


    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        roles = [
            'SCJC',
            'DRCJ',
            'Librarian',
        ]
        return any([
            [item in roles for item in request.user.roles],
            self.group.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
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


class Human(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    first_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
    )
    middle_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
        db_column='middle_initial',
    )
    last_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
    )
    nick_name = NoPunctuationCharField(
        max_length=255,
        editable=False,
        db_column='preferred_name',
    )
    email = LowerEmailField(
        editable=False,
        null=True,
        db_column='username',
    )
    birth_date = ReasonableBirthDate(
        editable=False,
        null=True,
        db_column='birthday'
    )
    home_phone = ValidatedPhoneField(
        max_length=255,
        editable=False,
        db_column='phone'
    )
    cell_phone = ValidatedPhoneField(
        max_length=255,
        editable=False,
    )
    work_phone = ValidatedPhoneField(
        max_length=255,
        editable=False,
    )
    bhs_id = models.IntegerField(
        editable=False,
        unique=True,
        null=True,
        db_column='legacy_id',
    )
    GENDER = Choices(
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(
        max_length=255,
        editable=False,
        choices=GENDER,
        db_column='sex',
    )
    PART = Choices(
        ('tenor', 'Tenor'),
        ('lead', 'Lead'),
        ('baritone', 'Baritone'),
        ('bass', 'Bass'),
    )
    part = VoicePartField(
        max_length=255,
        editable=False,
        choices=PART,
        db_column='primary_voice_part',
    )
    mon = models.IntegerField(
        editable=False,
        db_column='trusted_mon',
    )
    is_deceased = models.BooleanField(
        editable=False,
    )
    is_honorary = models.BooleanField(
        editable=False,
        db_column='honorary_member',
    )
    is_suspended = models.BooleanField(
        editable=False,
    )
    is_expelled = models.BooleanField(
        editable=False,
    )
    merged_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='merged_into',
    )
    deleted_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='deleted_by_id',
    )
    created = models.DateTimeField(
        db_column='created',
        null=True,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        null=True,
        editable=False,
    )

    objects = HumanManager()

    # Internals
    def __str__(self):
        if self.nick_name:
            first = self.nick_name
        else:
            first = self.first_name
        return " ".join([
            first,
            self.last_name,
        ])

    # Methods
    class Meta:
        managed=False
        db_table = 'vwMembers'


class Structure(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    KIND = Choices(
        ('organization', 'Organization'),
        ('district', 'District'),
        ('group', 'Group'),
        ('chapter', 'Chapter'),
        ('chorus', 'Chorus'),
        ('quartet', 'Quartet'),
    )
    kind = models.CharField(
        max_length=255,
        editable=False,
        choices=KIND,
        db_column='object_type',
    )
    GENDER = Choices(
        ('men', 'Male'),
        ('women', 'Female'),
        ('mixed', 'Mixed'),
    )
    gender = models.CharField(
        max_length=255,
        editable=False,
        choices=GENDER,
        db_column='category'
    )
    DIVISION = Choices(
        ('EVG', [
            'EVG Division I',
            'EVG Division II',
            'EVG Division III',
            'EVG Division IV',
            'EVG Division V',
        ]),
        ('FWD', [
            'FWD Arizona',
            'FWD Northeast',
            'FWD Northwest',
            'FWD Southeast',
            'FWD Southwest',
        ]),
        ('LOL', [
            'LOL 10000 Lakes',
            'LOL Division One',
            'LOL Northern Plains',
            'LOL Packerland',
            'LOL Southwest',
        ]),
        ('MAD', [
            # (160, 'madatl', 'MAD Atlantic'),
            'MAD Central',
            'MAD Northern',
            'MAD Southern',
            # (200, 'madwst', 'MAD Western'),
        ]),
        ('NED', [
            'NED Granite and Pine',
            'NED Mountain',
            'NED Patriot',
            'NED Sunrise',
            'NED Yankee',
        ]),
        ('SWD', [
            'SWD Northeast',
            'SWD Northwest',
            'SWD Southeast',
            'SWD Southwest',
        ]),
    )
    division = models.CharField(
        max_length=255,
        editable=False,
        null=True,
        db_column='division',
        choices=DIVISION,
    )
    bhs_id = models.IntegerField(
        editable=False,
        unique=True,
        null=True,
        db_column='legacy_id',
    )
    chapter_code = models.CharField(
        max_length=255,
        editable=False,
        db_column='legacy_code',
    )
    website = models.CharField(
        max_length=255,
        editable=False,
    )
    email = models.CharField(
        max_length=255,
        editable=False,
    )
    chorus_name = models.CharField(
        max_length=255,
        editable=False,
    )
    phone = models.CharField(
        max_length=255,
        editable=False,
    )
    fax = models.CharField(
        max_length=255,
        editable=False,
    )
    facebook = models.CharField(
        max_length=255,
        editable=False,
    )
    twitter = models.CharField(
        max_length=255,
        editable=False,
    )
    youtube = models.CharField(
        max_length=255,
        editable=False,
    )
    pinterest = models.CharField(
        max_length=255,
        editable=False,
    )
    flickr = models.CharField(
        max_length=255,
        editable=False,
    )
    instagram = models.CharField(
        max_length=255,
        editable=False,
    )
    soundcloud = models.CharField(
        max_length=255,
        editable=False,
    )
    tin = models.CharField(
        max_length=18,
        editable=False,
    )
    preferred_name = models.CharField(
        max_length=255,
        editable=False,
    )
    first_alternate_name = models.CharField(
        max_length=255,
        editable=False,
    )
    second_alternate_name = models.CharField(
        max_length=255,
        editable=False,
    )
    visitor_information = models.TextField(
        editable=False,
    )
    established_date = models.DateField(
        editable=False,
    )
    chartered_date = models.DateField(
        editable=False,
    )
    licenced_date = models.DateField(
        editable=False,
    )
    deleted_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='deleted_by_id',
    )
    created = models.DateTimeField(
        db_column='created',
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        editable=False,
    )
    # FKs
    status = models.ForeignKey(
        'Status',
        related_name='structures',
        # editable=False,
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_column='parent_id',
        on_delete=models.CASCADE,
    )

    objects = StructureManager()

    def __str__(self):
        if self.name:
            name = self.name.strip()
        else:
            name = 'UNKNOWN'
        return "{0} [{1}]".format(
            name,
            self.bhs_id,
        )


    class Meta:
        managed=False
        db_table = 'vwStructures'


class Status(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    # Internals
    def __str__(self):
        return str(self.name)

    class Meta:
        managed=False
        db_table = 'vwStatuses'
        verbose_name_plural = 'statuses'


class Membership(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )

    code = models.CharField(
        max_length=255,
        editable=False,
    )

    created = models.DateTimeField(
        db_column='created',
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='modified',
        editable=False,
    )
    deleted_id = models.CharField(
        max_length=255,
        null=True,
        editable=False,
        db_column='deleted_by_id',
    )

    # FKs
    structure = models.ForeignKey(
        'Structure',
        related_name='memberships',
        editable=False,
        db_column='object_id',
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        'Status',
        related_name='memberships',
        editable=False,
        on_delete=models.CASCADE,
    )

    # Internals
    def __str__(self):
        return "{0} {1}".format(
            self.structure,
            self.code,
        )

    class Meta:
        managed=False
        db_table = 'vwMemberships'


class Subscription(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    current_through = models.DateField(
        db_column='valid_through',
        null=True,
        editable=False,
    )
    status = models.CharField(
        max_length=255,
        editable=False,
    )
    items_editable = models.BooleanField(
        editable=False,
    )
    deleted = models.DateTimeField(
        null=True,
        editable=False,
        db_column='deleted',
    )
    created = models.DateTimeField(
        null=True,
        editable=False,
        db_column='created',
    )
    modified = models.DateTimeField(
        null=True,
        editable=False,
        db_column='updated',
    )

    # FKs
    human = models.ForeignKey(
        'Human',
        related_name='subscriptions',
        editable=False,
        db_column='members_id',
        on_delete=models.CASCADE,
    )

    # Internals
    def __str__(self):
        return str(self.human)

    class Meta:
        managed = False
        db_table = 'vwSubscriptions'


class Role(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    abbv = models.CharField(
        max_length=255,
        editable=False,
    )
    officer_roles_id = models.CharField(
        max_length=255,
        editable=False,
    )
    start_date = models.DateField(
        null=True,
        editable=False,
    )
    end_date = models.DateField(
        null=True,
        editable=False,
    )
    # FKs
    human = models.ForeignKey(
        'Human',
        related_name='roles',
        editable=False,
        db_column='member_id',
        on_delete=models.CASCADE,
    )
    structure = models.ForeignKey(
        'Structure',
        related_name='roles',
        editable=False,
        db_column='object_id',
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(
        db_column='created',
        null=True,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        null=True,
        editable=False,
    )

    objects = RoleManager()

    # Internals
    def __str__(self):
        return "{0} {1} {2}".format(
            self.name,
            self.human,
            self.structure,
        )

    def clean(self):
        if self.name.partition(" ")[0].lower() != self.structure.kind:
            raise ValidationError({
                'name': 'Role name does not match structure type.',
            })


    class Meta:
        managed=False
        db_table = 'vwOfficers'


class Join(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    status = models.BooleanField(
        editable=False,
    )
    paid = models.BooleanField(
        editable=False,
    )
    PART = Choices(
        ('tenor', 'Tenor'),
        ('lead', 'Lead'),
        ('baritone', 'Baritone'),
        ('bass', 'Bass'),
    )
    part = VoicePartField(
        max_length=255,
        editable=False,
        choices=PART,
        db_column='vocal_part',
    )
    established_date = models.DateField(
        db_column='created',
        null=True,
        editable=False,
    )
    inactive_date = models.DateField(
        db_column='inactive',
        null=True,
        editable=False,
    )
    inactive_reason = models.CharField(
        max_length=255,
        db_column='inactive_reason',
        editable=False,
    )
    deleted = models.DateTimeField(
        null=True,
        editable=False,
        db_column='deleted',
    )
    created = models.DateTimeField(
        db_column='created_on',
        null=True,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='modified',
        null=True,
        editable=False,
    )
    objects = JoinManager()

    # FKs
    subscription = models.ForeignKey(
        'Subscription',
        editable=False,
        related_name='joins',
        on_delete=models.CASCADE,
    )
    membership = models.ForeignKey(
        'Membership',
        editable=False,
        related_name='joins',
        on_delete=models.CASCADE,
    )
    structure = models.ForeignKey(
        'Structure',
        editable=False,
        related_name='joins',
        db_column='reference_structure_id',
        on_delete=models.CASCADE,
    )

    # Internals
    def clean(self):
        if all([
            not self.inactive_date,
            self.subscription.items_editable,
            self.subscription.status == 'expired',
        ]):
            raise ValidationError({
                'inactive_date': 'Inactive Date is missing on expired subscription.',
            })

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'vwSubscriptions_Memberships'
        verbose_name = 'Join'
        verbose_name_plural = 'Joins'


