
# Standard Library
import logging
import uuid

# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

log = logging.getLogger(__name__)


class Outcome(TimeStampedModel):
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

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    legacy_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'Round',
        related_name='outcomes',
        on_delete=models.CASCADE,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='outcomes',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='outcomes',
    )


    # Internals
    class JSONAPIMeta:
        resource_name = "outcome"

    def __str__(self):
        return str(self.id)

    def clean(self):
        pass

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                status__gt=0,
                category__lte=10,
            ),
            self.round.status == self.round.STATUS.finished,
        ])


    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_round_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.round.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.round.status < self.round.STATUS.started,
            ]),
        ])
