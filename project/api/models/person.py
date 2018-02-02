# Standard Libary
import datetime
import logging
import random
import uuid

# Third-Party
from cloudinary.models import CloudinaryField
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ranking import Ranking
from timezone_field import TimeZoneField

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField  # CIEmailField,
from django.contrib.postgres.fields import FloatRangeField
from django.contrib.postgres.fields import IntegerRangeField
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import smart_text
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.timezone import now

# First-Party
from api.fields import CloudinaryRenameField
from api.managers import ChartManager
from api.managers import ConventionManager
from api.managers import EnrollmentManager
from api.managers import GroupManager
from api.managers import MemberManager
from api.managers import OrganizationManager
from api.managers import PersonManager
from api.managers import UserManager
from api.tasks import create_admins_report
from api.tasks import create_bbscores_report
from api.tasks import create_csa_report
from api.tasks import create_drcj_report
from api.tasks import create_ors_report
from api.tasks import create_oss_report
from api.tasks import create_sa_report
from api.tasks import create_variance_report
from api.tasks import send_entry
from api.tasks import send_session
from api.tasks import send_session_reports

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Person(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    first_name = models.CharField(
        help_text="""
            The first name of the person.""",
        max_length=255,
        blank=False,
    )

    middle_name = models.CharField(
        help_text="""
            The middle name of the person.""",
        max_length=255,
        blank=True,
    )

    last_name = models.CharField(
        help_text="""
            The last name of the person.""",
        max_length=255,
        blank=False,
    )

    nick_name = models.CharField(
        help_text="""
            The nickname of the person.""",
        max_length=255,
        blank=True,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
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
        (-1, 'director', 'Director'),
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

    GENDER = Choices(
        (10, 'male', 'Male'),
        (20, 'female', 'Female'),
    )

    gender = models.IntegerField(
        choices=GENDER,
        null=True,
        blank=True,
    )

    is_deceased = models.BooleanField(
        default=False,
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
        default='',
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
        default='',
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
        default='',
    )

    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        unique=False,
    )

    phone = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    address = models.TextField(
        help_text="""
            The complete address of the resource.""",
        blank=True,
        max_length=1000,
        default='',
    )

    home_phone = models.CharField(
        help_text="""
            The home phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    work_phone = models.CharField(
        help_text="""
            The work phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    cell_phone = models.CharField(
        help_text="""
            The cell phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    airports = ArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=3,
        ),
        null=True,
        blank=True,
    )

    img = CloudinaryRenameField(
        'image',
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
        null=True,
        blank=True,
        unique=True,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    current_through = models.DateField(
        null=True,
        blank=True,
        editable=False,
    )

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
        return "{0}{1}".format(
            self.last_name[0].upper(),
            self.first_name[0].upper(),
        )

    # Person FKs
    user = models.OneToOneField(
        'User',
        related_name='person',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    objects = PersonManager()

    class JSONAPIMeta:
        resource_name = "person"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        pass
        # validate_email(self.email)
        # if hasattr(self, 'user') and not self.email:
        #     raise ValidationError(
        #         {'email': 'User account must have email.'}
        #     )
        # if not hasattr(self, 'user') and self.email:
        #     raise ValidationError(
        #         {'email': 'Person with email should have User account.'}
        #     )
        # if self.status == self.STATUS.exempt and (self.bhs_id or self.bhs_pk):
        #     raise ValidationError(
        #         {'status': 'Exempt users should not be in BHS or MC.'}
        #     )
        # if self.current_through:
        #     if self.status == self.STATUS.active and self.current_through < datetime.date.today():
        #         raise ValidationError(
        #             {'status': 'Active user beyond current_through date.'}
        #         )
        #     if self.status == self.STATUS.inactive and self.current_through > datetime.date.today():
        #         raise ValidationError(
        #             {'status': 'Inactive user within current_through date.'}
        #         )
        # else:
        #     if self.status == self.STATUS.active:
        #         raise ValidationError(
        #             {'status': 'Active status without current_through date.'}
        #         )

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x),
                filter(
                    None, [
                        self.full_name,
                        "[{0}]".format(self.bhs_id),
                    ]
                )
            )
        )
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    # Permissions
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
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.user == request.user,
        ])

    # Person transitions
    # @transition(field=status, source=[STATUS.new, STATUS.inactive], target=STATUS.active)
    # def activate(self, *args, **kwargs):
    #     """Activate the Person."""
    #     try:
    #         user = self.user
    #     except ObjectDoesNotExist:
    #         User.objects.create_user(
    #             email=self.email,
    #             person=self,
    #         )
    #         return
    #     user.is_active = True
    #     user.full_clean()
    #     user.save()
    #     return

    # @transition(field=status, source=[STATUS.new, STATUS.active], target=STATUS.inactive)
    # def deactivate(self, *args, **kwargs):
    #     self.user.is_active = False
    #     self.user.save()
    #     """Deactivate the Person."""
    #     return
