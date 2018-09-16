
# Standard Library
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps as api_apps
from django.db import models
from django.utils.encoding import smart_text

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Grantor(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='grantors',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='grantors',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            ('convention', 'group',),
        )

    class JSONAPIMeta:
        resource_name = "grantor"

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
        return True

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
