# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from timezone_field import TimeZoneField

# Django
from django.apps import apps as api_apps
from django.db import models

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Venue(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
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

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=255,
        blank=True,
    )

    state = models.CharField(
        max_length=255,
        blank=True,
    )

    airport = models.CharField(
        max_length=30,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the venue.""",
        blank=True,
    )

    # Methods
    def __str__(self):
        return str(self.id)

    # Internals
    class JSONAPIMeta:
        resource_name = "venue"

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_convention_manager,
        ])
