
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
from phonenumber_field.modelfields import PhoneNumberField

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

from .fields import UploadPath
from .fields import DivisionsField
from .fields import LowerEmailField

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



class Assignment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    # Denorm
    person_id = models.UUIDField(
        null=True,
        blank=True,
    )

    name = models.CharField(
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
        blank=True,
        default='',
    )

    last_name = models.CharField(
        help_text="""
            The last name of the person.""",
        max_length=255,
        blank=True,
        default='',
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
    )

    district = models.IntegerField(
        choices=DISTRICT,
        null=True,
        blank=True,
    )

    representing = models.CharField(
        help_text="""
            District""",
        max_length=10,
        blank=True,
        default='',
    )

    email = LowerEmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
    )

    cell_phone = PhoneNumberField(
        help_text="""
            The cell phone number of the resource.  Include country code.""",
        blank=True,
        null=True,
    )

    airports = ArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=3,
        ),
        null=True,
        blank=True,
        default=list,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to=UploadPath('image'),
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='assignments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

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
        return request.user.roles.filter(
            name__in=[
                'SCJC',
            ]
        )

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user in self.session.owners.all(),
        ])


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # Denormalized from BHS Award
    award_id = models.UUIDField(
        null=True,
        blank=True,
    )

    name = models.CharField(
        help_text="""Award Name.""",
        max_length=255,
        null=True,
        blank=True,
    )

    KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    kind = models.IntegerField(
        choices=KIND,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    season = models.IntegerField(
        choices=SEASON,
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            The Public description of the award.""",
        max_length=1000,
        null=True,
        blank=True,
    )

    district = models.CharField(
        max_length=255,
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
        null=True,
        blank=True,
    )

    is_single = models.BooleanField(
        default=False,
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

    scope_range = DecimalRangeField(
        null=True,
        blank=True,
    )

    tree_sort = models.IntegerField(
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
    class Meta:
        pass
        # unique_together = (
        #     ('session', 'award',)
        # )

    class JSONAPIMeta:
        resource_name = "contest"

    def __str__(self):
        return "{0}".format(
            self.name,
            # self.session,
        )

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
        return request.user.roles.filter(
            name__in=[
                'SCJC',
                'DRCJ',
            ]
        ),

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        if self.session.status >= self.session.STATUS.opened:
            return False
        return any([
            request.user in self.session.owners.all(),
        ])


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

    is_senior = models.BooleanField(
        help_text="""Qualifies as a Senior Group.  This can be set manually, but is denormlized nightly for quartets.""",
        default=False,
    )

    is_youth = models.BooleanField(
        help_text="""Qualifies as a Youth Group.  Must be set manually.""",
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

    chapters = models.CharField(
        help_text="""The Chapter(s) that the comprise the group members.""",
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

    name = models.CharField(
        help_text="""
            The name of the resource.
        """,
        max_length=255,
        blank=True,
        default='',
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
        null=True,
        blank=True,
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
        blank=True,
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
    )

    district = models.IntegerField(
        choices=DISTRICT,
        null=True,
        blank=True,
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
    )

    code = models.CharField(
        help_text="""
            Short-form code.""",
        max_length=255,
        blank=True,
        default='',
    )

    # FKs
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='entries',
        blank=True,
    )

    contests = models.ManyToManyField(
        'Contest',
        related_name='entries',
        blank=True,
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
        return "{0}".format(
            self.name,
        )

    def clean(self):
        if self.is_private and self.contests.all():
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
        return request.user.roles.filter(
            name__in=[
                'SCJC',
                'DRCJ',
                'Manager',
            ]
        ),

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        if self.session.status >= self.session.STATUS.packaged:
            return False
        return any([
            request.user in self.session.owners.all(),
            all([
                request.user in self.owners.all(),
                # self.status < self.STATUS.approved,
            ]),
        ])

    # Methods
    def update_from_group(self):
        Group = apps.get_model('bhs.group')
        group = Group.objects.get(id=self.group_id)
        self.name = group.name
        self.kind = group.kind
        self.gender = group.gender
        self.district = group.district
        self.division = group.division
        self.participants = group.participants
        self.chapters = group.chapters
        self.image.name = group.image.name
        self.bhs_id = group.bhs_id
        self.code = group.code
        self.owners.set(group.owners.all())
        for chart in group.charts.all():
            self.repertories.create(
                chart_id=chart.id,
                title=chart.title,
                arrangers=chart.arrangers,
            )
        return

    def get_owners_emails(self):
        if not self.owners:
            raise ValueError("No owners for {0}".format(self))
        owners = self.owners.order_by(
            'last_name',
            'first_name',
        )
        return ["{0} <{1}>".format(x.name, x.email) for x in owners]

    def get_invite_email(self):
        template = 'emails/entry_invite.txt'
        context = {'entry': self}
        subject = "[Barberscore] Contest Invitation for {0}".format(
            self.name,
        )
        to = self.get_owners_emails()
        cc = self.session.get_owners_emails()
        # cc.extend(self.session.convention.get_ca_emails())
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
            self.name,
        )
        to = self.get_owners_emails()
        cc = self.session.get_owners_emails()
        # cc.extend(self.session.convention.get_ca_emails())
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
        contests = self.contests.order_by(
            'name',
        )
        context = {
            'entry': self,
            'contests': contests,
        }
        subject = "[Barberscore] Submission Notification for {0}".format(
            self.name,
        )
        to = self.get_owners_emails()
        cc = self.session.get_owners_emails()
        # cc.extend(self.session.convention.get_ca_emails())
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
        repertories = self.repertories.order_by(
            'title',
            'arrangers',
        )
        contests = self.contests.order_by(
            'tree_sort',
        )
        context = {
            'entry': self,
            'repertories': repertories,
            'contests': contests,
        }
        subject = "[Barberscore] Approval Notification for {0}".format(
            self.name,
        )
        to = self.get_owners_emails()
        cc = self.session.get_owners_emails()
        # cc.extend(self.session.convention.get_ca_emails())
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
            # self.group_status == self.GROUP_STATUS.active,
        ])

    def can_submit_entry(self):
        return all([
            # Only active groups can submit.
            # self.group_status == self.GROUP_STATUS.active,
            # Check POS for choruses only
            self.pos if self.kind == self.KIND.chorus else True,
            # ensure they can't submit a private while competiting.
            not all([
                self.is_private,
                self.contests.all(),
            ]),
            # Check participants
            self.participants,
        ])

    def can_approve(self):
        if self.is_private and self.contests.all():
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
        if self.group_id:
            self.update_from_group()
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


class Repertory(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # Chart Denorm
    chart_id = models.UUIDField(
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=255,
    )

    arrangers = models.CharField(
        max_length=255,
    )

    # FKs
    entry = models.ForeignKey(
        'Entry',
        related_name='repertories',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='repertories',
    )

    # Internals
    class Meta:
        verbose_name_plural = 'repertories'
        # unique_together = (
        #     ('group', 'chart',),
        # )

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
        return any([
            request.user in self.entry.session.owners.all(),
            request.user in self.entry.owners.all(),
            request.user.roles.filter(name__in=[
                'SCJC',
                'DRCJ',
                'CA',
                'Librarian',
            ]),
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return request.user.roles.filter(
            name__in=[
                'SCJC',
                'Librarian',
                'Manager',
            ]
        ),

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user in self.entry.owners.all(),
            request.user.roles.filter(name='Librarian'),
        ])


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

    group_emails = ArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=100,
        ),
        null=True,
        blank=True,
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

    # Denorm
    convention_id = models.UUIDField(
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        default='',
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
    )

    district = models.IntegerField(
        choices=DISTRICT,
        blank=True,
        null=True,
    )

    SEASON = Choices(
        # (1, 'summer', 'Summer',),
        # (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    season = models.IntegerField(
        choices=SEASON,
        blank=True,
        null=True,
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
        blank=True,
        null=True,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        blank=True,
        null=True,
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
        blank=True,
        default='(TBD)',
    )

    location = models.CharField(
        help_text="""
            The general location in the form "City, State".""",
        max_length=255,
        blank=True,
        default='(TBD)',
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the convention.""",
        null=True,
        blank=True,
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

    image = models.ImageField(
        upload_to=UploadPath('image'),
        max_length=255,
        null=True,
        blank=True,
    )


    # FKs
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='sessions',
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

    # Session Properties

    # Session Internals
    class Meta:
        pass
        # unique_together = (
        #     ('convention', 'kind')
        # )

    class JSONAPIMeta:
        resource_name = "session"

    def __str__(self):
        return str(self.get_kind_display())

    def clean(self):
        pass

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

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

    def get_legacy_report(self):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'oa',
            'group_id',
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
            oa = entry.draw
            group_name = entry.group_name
            group_type = entry.get_group_kind_display()
            if group_type == 'Quartet':
                group_id = entry.group_bhs_id
            elif group_type == 'Chorus':
                group_id = entry.group_code
            elif group_type == 'VLQ':
                group_id = entry.group_code
            else:
                raise RuntimeError("Improper Entity Type: {0}".format(entry.get_group_kind_display()))
            i = 0
            charts_sorted = sorted(entry.group_charts, key=lambda x: x['title'])
            for chart in charts_sorted:
                i += 1
                song_number = i
                song_title = chart['title']
                row = [
                    oa,
                    group_id,
                    group_name,
                    group_type,
                    song_number,
                    song_title,
                ]
                ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    def save_legacy_report(self):
        content = self.get_legacy_report()
        self.legacy_report.save("legacy_report", content)

    def get_drcj_report(self):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'OA',
            'Group Name',
            'BHS ID',
            'Representing',
            'Chapter(s)',
            'Director/Participant(s)',
            'Estimated POS',
            'Evaluation?',
            'Score/Eval-Only?',
            'Award(s)',
            'Charts(s)',
            'Contacts(s)',
        ]
        ws.append(fieldnames)
        entries = self.entries.filter(
            status__in=[
                Entry.STATUS.approved,
            ]
        ).order_by('draw')
        for entry in entries:
            oa = entry.draw
            group_name = entry.group_name
            bhs_id = entry.group_bhs_id
            representing = entry.representing
            chapters = entry.chapters
            participants = entry.participants
            pos = entry.pos
            is_evaluation = entry.is_evaluation
            is_private = entry.is_private

            award_names = "\n".join(
                filter(
                    None,
                    ["{0}".format(i.name) for i in entry.contests.order_by('award_tree_sort')],
                )
            )

            chart_titles = "\n".join(
                filter(
                    None,
                    ["{0}".format(i['nomen']) for i in sorted(entry.group_charts, key=lambda x: x['nomen'])],
                )
            )

            contact_emails = "\n".join(
                filter(
                    None,
                    ["{0} <{1}>".format(i.name, i.email) for i in entry.owners.order_by('family_name')],
                )
            )

            row = [
                oa,
                group_name,
                bhs_id,
                representing,
                chapters,
                participants,
                pos,
                is_evaluation,
                is_private,
                award_names,
                chart_titles,
                contact_emails,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    def save_drcj_report(self):
        content = self.get_drcj_report()
        self.drcj_report.save("drcj_report", content)

    def get_owners_emails(self):
        owners = self.owners.order_by(
            'last_name',
            'first_name',
        )
        return ["{0} <{1}>".format(x.name, x.email) for x in owners]

    def get_open_email(self):
        template = 'emails/session_open.txt'
        context = {'session': self}
        subject = "[Barberscore] {0} {1} is OPEN".format(
            self.get_district_display(),
            self.name,
        )
        to = self.get_owners_emails()
        bcc = self.group_emails
        # context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=bcc,
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
            xlsx = self.get_drcj_report()
        file_name = '{0} Session DRCJ Report DRAFT.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        if self.legacy_report:
            xlsx = self.legacy_report.file
        else:
            xlsx = self.get_legacy_report()
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
            xlsx = self.get_drcj_report()
        file_name = '{0} Session DRCJ Report FINAL.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        if self.legacy_report:
            xlsx = self.legacy_report.file
        else:
            xlsx = self.get_legacy_report()
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
        return request.user.roles.filter(
            name__in=[
                'SCJC',
                'DRCJ',
            ]
        )

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        if self.status >= self.STATUS.packaged:
            return False
        return any([
            request.user in self.owners.all(),
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
        return True
        # try:
        #     return all([
        #         # # self.convention.open_date <= datetime.date.today(),
        #         # self.contests.filter(status=self.contests.model.STATUS.included),
        #     ])
        # except TypeError:
        #     return False

    def can_close(self):
        return True
        Entry = apps.get_model('smanager.entry')
        return all([
            # self.convention.close_date < datetime.date.today(),
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
        return True
        # return all([
        #     not self.rounds.exclude(status=self.rounds.model.STATUS.published)
        # ])

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
        entries = self.entries.all()
        contests.delete()
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
        """Build Session."""
        Award = apps.get_model('bhs.award')

        # Reset for indempotence
        self.reset()

        # Get all the active awards for the convention group
        awards = Award.objects.filter(
            status=Award.STATUS.active,
            kind=self.kind,
            season=self.season,
            district=self.district,
            # division__in=self.convention.divisions,
        ).order_by('tree_sort')
        if self.divisions:
            awards = awards.filter(
                division__in=self.divisions,
            ).order_by('tree_sort')
        for award in awards:
            # Create contests for each active award.
            # Could also do some logic here for more precision
            self.contests.create(
                award_id=award.id,
                name=award.name,
                kind=award.kind,
                gender=award.gender,
                level=award.level,
                season=award.season,
                description=award.description,
                district=award.district,
                division=award.division,
                age=award.age,
                is_novice=award.is_novice,
                is_single=award.is_single,
                size=award.size,
                size_range=award.size_range,
                scope=award.scope,
                scope_range=award.scope_range,
                tree_sort=award.tree_sort,
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
        self.save_drcj_report()
        self.save_legacy_report()

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
