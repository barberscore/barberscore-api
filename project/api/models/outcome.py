
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
from django.db import models
from django.db.models import Sum, Q

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
        max_length=1024,
        null=True,
        blank=True,
    )

    LEVEL = Choices(
        (10, 'championship', "Championship"),
        (30, 'qualifier', "Qualifier"),
        (45, 'representative', "Representative"),
        (50, 'deferred', "Deferred"),
        (60, 'manual', "Manual"),
        (70, 'raw', "Improved - Raw"),
        (80, 'standard', "Improved - Standard"),
    )

    level = models.IntegerField(
        choices=LEVEL,
    )

    num_rounds = models.IntegerField(
        help_text="""Number of rounds to determine the championship""",
    )

    threshold = models.FloatField(
        help_text="""
            The score threshold for automatic qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    minimum = models.FloatField(
        help_text="""
            The minimum score required for qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    advance = models.FloatField(
        help_text="""
            The score threshold to advance to next round (if any) in
            multi-round qualification.
        """,
        null=True,
        blank=True,
    )

    spots = models.IntegerField(
        help_text="""Number of top spots which qualify""",
        null=True,
        blank=True,
    )

    legacy_num = models.IntegerField(
        blank=True,
        null=True,
    )

    legacy_name = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'Round',
        related_name='outcomes',
        on_delete=models.CASCADE,
    )

    award = models.ForeignKey(
        'Award',
        related_name='outcomes',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='outcomes',
    )

    # Methods
    def get_name(self):
        Panelist = apps.get_model('api.panelist')
        if self.level == self.LEVEL.deferred:
            return "(Result determined post-contest)"
        if self.level in [self.LEVEL.manual, self.LEVEL.raw, self.LEVEL.standard]:
            return "MUST ENTER WINNER MANUALLY"
        if self.level == self.LEVEL.qualifier:
            threshold = self.threshold
            num = [self.num]
            qualifiers = self.round.appearances.filter(
                run_score__gte=threshold,
                contesting__contains=num,
            ).distinct(
            ).order_by(
                'group__name',
            ).values_list('group__name', flat=True)
            if qualifiers:
                return ", ".join(qualifiers)
            return "(No qualifiers)"
        if self.level in [self.LEVEL.championship, self.LEVEL.representative]:
            num = [self.num]
            winner = self.round.appearances.filter(
                contesting__contains=num,
            ).earliest(
                '-run_points',
            )
            if winner:
                return str(winner.group.name)
            return "(No Recipient)"
        raise RuntimeError("Level mismatch")

    # Internals
    class Meta:
        unique_together = (
            ('round', 'award',)
        )

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
            self.round.status == self.round.STATUS.finished,
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                status__gt=0,
                category__lte=10,
            ),
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
                self.round.status < self.round.STATUS.finished,
            ]),
        ])
