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
from django.db import models


log = logging.getLogger(__name__)


class Repertory(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
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
        default=STATUS.active,
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
        return str(self.id)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return any([
            request.user.person.officers.filter(office__is_convention_manager=True),
            request.user.person.officers.filter(office__is_round_manager=True),
            request.user.person.officers.filter(office__is_group_manager=True),
            request.user.person.officers.filter(office__is_session_manager=True),
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.group.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
            request.user.person.officers.filter(office__is_convention_manager=True),
            request.user.person.officers.filter(office__is_round_manager=True),
            request.user.person.officers.filter(office__is_session_manager=True),
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.person.officers.filter(office__is_convention_manager=True),
            request.user.person.officers.filter(office__is_round_manager=True),
            request.user.person.officers.filter(office__is_group_manager=True),
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.group.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
            request.user.person.officers.filter(office__is_convention_manager=True),
            request.user.person.officers.filter(office__is_round_manager=True),
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
