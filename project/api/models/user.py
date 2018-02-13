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

# First-Party
from api.managers import UserManager

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
        default=STATUS.new,
    )

    name = models.CharField(
        max_length=255,
        editable=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        editable=True,
    )

    auth0_id = models.CharField(
        max_length=100,
        unique=True,
        editable=True,
        null=True,
        blank=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(
        # auto_now_add=True,
        editable=False,
        null=True,
    )

    modified = models.DateTimeField(
        # auto_now=True,
        editable=False,
        null=True,
    )

    objects = UserManager()

    @property
    def is_active(self):
        """Proxy status."""
        if self.status == self.STATUS.active:
            return True
        else:
            return False

    @property
    def is_superuser(self):
        return self.is_staff

    @cached_property
    def is_convention_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_convention_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_session_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_session_manager=True,
                status=self.person.officers.model.STATUS.active,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_scoring_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_scoring_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_group_manager(self):
        try:
            is_manager = bool(
                self.person.officers.filter(
                    status__gt=0,
                )
            )
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_person_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_person_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_award_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_award_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_judge_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_judge_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_chart_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_chart_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    class JSONAPIMeta:
        resource_name = "user"

    # User Internals
    def __str__(self):
        return self.name

    def clean(self):
        pass
        # if self.email != self.person.email:
        #     raise ValidationError(
        #         {'email': 'Email does not match person'}
        #     )
        # if self.name != self.person.full_name:
        #     raise ValidationError(
        #         {'name': 'Name does not match person'}
        #     )
        # if self.is_active and self.person.status <= 0:
        #     raise ValidationError(
        #         {'name': 'Should not be active.'}
        #     )
        # if not self.is_active and self.person.status > 0:
        #     raise ValidationError(
        #         {'is_active': 'Should be active.'}
        #     )

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # User Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return self == request.user

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # User Transitions
    # @fsm_log_by
    # @transition(field=status, source='*', target=STATUS.active)
    # def activate(self, *args, **kwargs):
    #     self.is_active = True
    #     return

    # @fsm_log_by
    # @transition(field=status, source='*', target=STATUS.inactive)
    # def deactivate(self, *args, **kwargs):
    #     self.is_active = False
    #     pass
