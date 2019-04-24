import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from model_utils import Choices
from django_fsm import FSMIntegerField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from api.fields import LowerEmailField

from .validators import validate_bhs_id
from .validators import validate_birth_date
from .validators import validate_tin
from .validators import validate_nopunctuation
from .managers import PersonManager
from .managers import GroupManager
from .managers import StreamManager

class Person(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    STATUS = Choices(
        (-20, 'expelled', 'Expelled'),
        (-10, 'suspended', 'Suspended'),
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
    )
    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )
    prefix = models.CharField(
        max_length=255,
        default='',
        blank=True,
        validators=[
            validate_nopunctuation,
        ],
    )
    first_name = models.CharField(
        max_length=255,
        validators=[
            validate_nopunctuation,
        ],
    )
    middle_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
        validators=[
            validate_nopunctuation,
        ],
    )
    last_name = models.CharField(
        max_length=255,
        validators=[
            validate_nopunctuation,
        ],
    )
    suffix = models.CharField(
        max_length=255,
        default='',
        blank=True,
        validators=[
            validate_nopunctuation,
        ],
    )
    nick_name = models.CharField(
        max_length=255,
        default='',
        blank=True,
        validators=[
            validate_nopunctuation,
        ],
    )
    email = LowerEmailField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        validators=[
            validate_birth_date,
        ],
    )
    is_deceased = models.BooleanField(
        default=False,
    )
    home_phone = PhoneNumberField(
        default='',
        blank=True,
    )
    cell_phone = PhoneNumberField(
        default='',
        blank=True,
    )
    work_phone = PhoneNumberField(
        default='',
        blank=True,
    )
    bhs_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        validators=[
            validate_bhs_id,
        ],
    )
    GENDER = Choices(
        (10, 'male', 'Male'),
        (20, 'female', 'Female'),
    )
    gender = models.IntegerField(
        null=True,
        blank=True,
        choices=GENDER,
    )
    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )
    part = models.IntegerField(
        null=True,
        blank=True,
        choices=PART,
    )
    mon = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(999),
        ],
    )

    objects = PersonManager()

    # Internals
    def __str__(self):
        return "{0}".format(
            " ".join([
                self.prefix,
                self.first_name,
                self.middle_name,
                self.last_name,
                self.suffix,
            ])
        )

    class Meta:
        pass

    class JSONAPIMeta:
        resource_name = "person"

    # Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.suspended],
        target=STATUS.active,
    )
    def activate(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.active],
        target=STATUS.expelled,
    )
    def expel(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.active],
        target=STATUS.suspended,
    )
    def suspend(self, *args, **kwargs):
        return


class Group(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    STATUS = Choices(
        (-50, 'revoked', 'Revoked'),
        (-40, 'suspended', 'Suspended'),
        (-30, 'merged', 'Merged'),
        (-20, 'closed', 'Closed'),
        (-10, 'expired', 'Expired'),
        (0, 'new', 'New'),
        (10, 'pending', 'Pending'),
        (20, 'awaiting', 'Awaiting'),
        (30, 'prospective', 'Prospective'),
        (40, 'penvol', 'Penvol'),
        (60, 'licensed', 'Licensed'),
        (90, 'active', 'Active'),
    )
    status = FSMIntegerField(
        default=STATUS.new,
        choices=STATUS,
    )
    name = models.CharField(
        max_length=255,
    )
    KIND = Choices(
        (10, 'organization', 'Organization'),
        (20, 'district', 'District'),
        (30, 'group', 'Group'),
        (40, 'chapter', 'Chapter'),
        (50, 'chorus', 'Chorus'),
        (60, 'quartet', 'Quartet'),
    )
    kind = models.IntegerField(
        choices=KIND,
    )
    GENDER = Choices(
        (10, 'male', 'Male'),
        (20, 'female', 'Female'),
        (30, 'mixed', 'Mixed'),
    )
    gender = models.IntegerField(
        null=True,
        blank=True,
        choices=GENDER,
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
        unique=True,
        null=True,
        blank=True,
        validators=[
            validate_bhs_id,
        ],
    )
    legacy_code = models.CharField(
        max_length=255,
        blank=True,
        default='',
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
        blank=True,
    )
    main_phone = models.CharField(
        help_text="""
            The main phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )
    fax_phone = models.CharField(
        help_text="""
            The fax phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )
    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
        default='',
    )
    twitter = models.URLField(
        help_text="""
            The twitter URL of the resource.""",
        blank=True,
        default='',
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
    tin = models.CharField(
        help_text="""
            The Tax Identification Number.""",
        blank=True,
        max_length=18,
        validators=[
            validate_tin,
        ],
        default='',
    )
    address = models.TextField(
        help_text="""
            The complete address of the resource.""",
        blank=True,
        max_length=1000,
        default='',
    )
    preferred_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    first_alternate_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    second_alternate_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        default='',
    )
    visitor_information = models.TextField(
        max_length=255,
        blank=True,
        default='',
    )
    established_date = models.DateField(
        null=True,
        blank=True,
    )
    chartered_date = models.DateField(
        null=True,
        blank=True,
    )
    licensed_date = models.DateField(
        null=True,
        blank=True,
    )
    deleted_date = models.DateField(
        null=True,
        blank=True,
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
    objects = GroupManager()

    class JSONAPIMeta:
        resource_name = "member"

    def __str__(self):
        return self.name


class Stream(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    STATUS = Choices(
        (-30, 'cancelled', 'Cancelled',),
        (-20, 'swapped', 'Swapped',),
        (-10, 'expired', 'Expired',),
        (0, 'new', 'New',),
        (10, 'lapsed', 'Lapsed',),
        (20, 'pending', 'Pending',),
        (90, 'active', 'Active',),
    )
    status = FSMIntegerField(
        default=STATUS.new,
        choices=STATUS,
    )
    CODE = Choices(
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
        (120, 'SNA', 'SNA'),
        (120, 'YA2', 'YA2'),
        (120, 'MEP', 'MEP'),
        (120, 'YA1', 'YA1'),
    )
    code = models.IntegerField(
        choices=CODE,
        null=True,
        blank=True,
    )
    PART = Choices(
        (10, 'tenor', 'Tenor'),
        (20, 'lead', 'Lead'),
        (30, 'baritone', 'Baritone'),
        (40, 'bass', 'Bass'),
    )
    part = models.IntegerField(
        choices=PART,
        null=True,
        blank=True,
    )
    is_paid = models.BooleanField(
        default=False,
    )
    is_current = models.BooleanField(
        default=False,
    )
    established_date = models.DateField(
        null=True,
        blank=True,
    )
    inactive_date = models.DateField(
        null=True,
        blank=True,
    )
    INACTIVE = Choices(
        (10, 'nonrenewal', 'Non-Renewal'),
        (20, 'renewed', 'Renewed'),
        (30, 'notcancelled', 'Not Cancelled'),
        (40, 'nonpayment', 'Non-Payment'),
        (50, 'expired', 'Expired'),
        (60, 'deceased', 'Deceased'),
        (70, 'changedoption', 'Changed Option'),
        (80, 'other', 'Other'),
        (90, 'cancelled', 'Cancelled'),
        (100, 'transferred', 'Transferred'),
        (110, 'swappedchapter', 'Swapped Chapter'),
        (120, 'swapped', 'Swapped'),
    )

    inactive = models.IntegerField(
        choices=INACTIVE,
        null=True,
        blank=True,
    )

    current_through = models.DateField(
        null=True,
        blank=True,
    )

    join_created = models.DateTimeField(
        null=True,
        blank=True,
    )
    join_modified = models.DateTimeField(
        null=True,
        blank=True,
    )
    join_deleted = models.DateTimeField(
        null=True,
        blank=True,
    )
    mem_created = models.DateTimeField(
        null=True,
        blank=True,
    )
    mem_modified = models.DateTimeField(
        null=True,
        blank=True,
    )
    mem_deleted = models.DateTimeField(
        null=True,
        blank=True,
    )
    sub_created = models.DateTimeField(
        null=True,
        blank=True,
    )
    sub_modified = models.DateTimeField(
        null=True,
        blank=True,
    )
    sub_deleted = models.DateTimeField(
        null=True,
        blank=True,
    )

    # FK Pointers
    group = models.ForeignKey(
        Group,
        related_name='streams',
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        Person,
        related_name='streams',
        on_delete=models.CASCADE,
    )

    # Internals
    objects = StreamManager()

    class JSONAPIMeta:
        resource_name = "stream"

    def __str__(self):
        return str(self.id)

    def clean(self):
        return
