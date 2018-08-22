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
from django_fsm_log.models import StateLog
from django.contrib.contenttypes.fields import GenericRelation

# Django
from django.apps import apps as api_apps
from django.db import models
from django.core.exceptions import ValidationError

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Contest(TimeStampedModel):
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

    num = models.IntegerField(
        blank=True,
        null=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    # Private
    group = models.ForeignKey(
        'Group',
        null=True,
        blank=True,
        related_name='contests',
        on_delete=models.SET_NULL,
        help_text="""The Winner of the Contest.""",
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='contests',
        on_delete=models.CASCADE,
    )

    award = models.ForeignKey(
        'Award',
        related_name='contests',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='contests',
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'award',)
        )

    class JSONAPIMeta:
        resource_name = "contest"

    def __str__(self):
        return "{0}".format(
            self.award.name,
        )

    def clean(self):
        if self.award.level == self.award.LEVEL.qualifier and group:
            raise ValidationError(
                {'level': 'Qualifiers can not select winners'}
            )
        if self.is_primary and self.status <= 0:
            raise ValidationError(
                {'is_primary': 'Primary contests must have status of included'}
            )

    # Contest Permissions
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
        ])


    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                # self.session.status < self.session.STATUS.opened,
            ]),
        ])

    # Methods
    def determine(self, *args, **kwargs):
        if self.award.level in [
            self.award.LEVEL.qualifier,
            self.award.LEVEL.top,
            self.award.LEVEL.manual,
            self.award.LEVEL.deferred,
        ]:
            return
        contestants = self.contestants.filter(
            status__gt=0,
        ).order_by(
            '-entry__competitor__tot_points',
            '-entry__competitor__sng_points',
            '-entry__competitor__per_points',
        )
        if contestants:
            group = contestants.first().entry.group
        else:
            group = None
        self.group = group
        return

    # Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.excluded], target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.included], target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return
