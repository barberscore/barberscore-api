# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps as api_apps
from django.db import models

# First-Party
from api.fields import CloudinaryRenameField
from api.storages import CustomMediaCloudinaryStorage

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


def upload_to(instance, filename):
    return 'chart/{0}'.format(instance.id)


class Chart(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
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

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    image = models.FileField(
        upload_to=upload_to,
        blank=True,
        storage=CustomMediaCloudinaryStorage(),
    )

    # Internals
    class Meta:
        unique_together = (
            ('title', 'arrangers',)
        )

    class JSONAPIMeta:
        resource_name = "chart"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            self.title,
            "[{0}]".format(self.arrangers),
        ]))
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
        return any([
            request.user.is_chart_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_chart_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Award."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Award."""
        return
