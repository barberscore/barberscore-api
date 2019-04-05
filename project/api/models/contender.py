
# Standard Library
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


log = logging.getLogger(__name__)


class Contender(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    appearance = models.ForeignKey(
        'Appearance',
        related_name='contenders',
        on_delete=models.CASCADE,
    )

    outcome = models.ForeignKey(
        'Outcome',
        related_name='contenders',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='contenders',
    )

    # Internals
    class Meta:
        ordering = (
            'outcome__num',
        )
        unique_together = (
            ('appearance', 'outcome',),
        )

    class JSONAPIMeta:
        resource_name = "contender"

    def __str__(self):
        return str(self.id)

    # Methods

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
            request.user.is_session_manager,
            request.user.is_round_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.outcome.round.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.outcome.round.status < self.outcome.round.STATUS.started,
            ]),
        ])

    # contender Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return
