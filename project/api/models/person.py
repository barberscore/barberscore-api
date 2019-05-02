
# Standard Library
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

# Django
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.timezone import now

# First-Party
from api.fields import LowerEmailField
from api.fields import ImageUploadPath
from api.managers import PersonManager

log = logging.getLogger(__name__)


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

    # current_through = models.DateField(
    #     null=True,
    #     blank=True,
    #     editable=True,
    # )

    # Relations
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
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        user = getattr(self, 'user', None)
        return any([
            all([
                user == request.user,
                self.status > 0,
                self.mc_pk == None,
            ]),
            all([
                self.members.filter(
                    group__officers__person__user=request.user,
                    group__officers__status__gt=0,
                ),
                self.mc_pk == None,
            ]),
        ])

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
