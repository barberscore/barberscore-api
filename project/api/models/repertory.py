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
from django.utils.encoding import smart_text


config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Repertory(TimeStampedModel):
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

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='repertories',
        on_delete=models.CASCADE,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='repertories',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        verbose_name_plural = 'repertories'
        unique_together = (
            ('group', 'chart',),
        )

    class JSONAPIMeta:
        resource_name = "repertory"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.group,
                    self.chart,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_group_manager,
            request.user.is_session_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.group.officers.filter(
                person__newuser=request.user,
                status__gt=0,
            ),
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_session_manager,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.group.officers.filter(
                person__newuser=request.user,
                status__gt=0,
            ),
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Repertory."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Repertory."""
        return
