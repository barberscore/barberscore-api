
# Standard Library
import logging
import uuid

# Third-Party
from auth0.v3.exceptions import Auth0Error
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from django.apps import apps

# Django
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property

# First-Party
from api.fields import LowerEmailField
from api.managers import UserManager


log = logging.getLogger(__name__)


class User(AbstractBaseUser):
    USERNAME_FIELD = settings.USERNAME_FIELD
    REQUIRED_FIELDS = settings.REQUIRED_FIELDS

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = models.CharField(
        max_length=100,
        unique=True,
        editable=True,
    )

    email = LowerEmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
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
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = UserManager()

    @cached_property
    def is_mc(self):
        """Proxy status."""
        return bool(getattr(getattr(self, 'person'), 'mc_pk', None))

    @cached_property
    def is_active(self):
        """Proxy status."""
        if self.is_staff:
            return True
        if self.person:
            return bool(self.person.status > 0)
        return False

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
        if getattr(self, 'person'):
            return self.person.common_name
        return self.username

    def clean(self):
        pass

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
