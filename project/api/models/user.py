# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.functional import cached_property
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError

# First-Party
from api.managers import UserManager
from api.fields import LowerEmailField

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class User(AbstractBaseUser):
    USERNAME_FIELD = settings.USERNAME_FIELD
    REQUIRED_FIELDS = settings.REQUIRED_FIELDS

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

    username = models.CharField(
        max_length=100,
        unique=True,
        editable=True,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        editable=True,
    )

    email = LowerEmailField(
        max_length=100,
        unique=True,
        editable=True,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    current_through = models.DateField(
        null=True,
        blank=True,
        editable=True,
    )

    mc_pk = models.CharField(
        null=True,
        blank=True,
        max_length=36,
        unique=True,
        db_index=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    person = models.OneToOneField(
        'Person',
        related_name='user',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='users',
    )

    objects = UserManager()

    @cached_property
    def is_mc(self):
        """Proxy status."""
        return bool(getattr(getattr(self, 'person'), 'mc_pk', None))

    @cached_property
    def is_active(self):
        """Proxy status."""
        return bool(self.status >= 0)

    @cached_property
    def is_superuser(self):
        return bool(self.is_staff)

    @cached_property
    def is_convention_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_convention_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_session_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_session_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_round_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_round_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_scoring_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_scoring_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_group_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_group_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_person_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_person_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_award_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_award_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_officer_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_officer_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_chart_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_chart_manager=True,
                status__gt=0,
            )
        )

    @cached_property
    def is_assignment_manager(self):
        return bool(
            self.person.officers.filter(
                office__is_assignment_manager=True,
                status__gt=0,
            )
        )

    class JSONAPIMeta:
        resource_name = "user"

    # User Internals
    def __str__(self):
        if self.is_staff:
            return self.name
        if self.bhs_id:
            suffix = "[{0}]".format(self.bhs_id)
        else:
            suffix = "[No BHS ID]"
        full = "{0} {1}".format(
            self.name,
            suffix,
        )
        return " ".join(full.split())


    def clean(self):
        if self.is_staff:
            return
        if not self.person:
            raise ValidationError(
                {'person': 'Non-staff user accounts must have Person attached.'}
            )
        if self.email != self.person.email:
            raise ValidationError(
                {'email': 'Email does not match person'}
            )
        if self.name != self.person.common_name:
            raise ValidationError(
                {'name': 'Name does not match person'}
            )
        if self.bhs_id != self.person.bhs_id:
            raise ValidationError(
                {'bhs_id': 'BHS ID does not match person'}
            )

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # User Permissions
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
        if request.user == self:
            return True
        return False

    # User Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        # Should deactive AUTH0
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        # Should deactive AUTH0
        return
