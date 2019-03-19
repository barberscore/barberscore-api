
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
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Min, Max, Count, Avg

from django.apps import apps

log = logging.getLogger(__name__)


class Score(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'verified', 'Verified',),
        # (20, 'entered', 'Entered',),
        (25, 'cleared', 'Cleared',),
        (30, 'flagged', 'Flagged',),
        (35, 'revised', 'Revised',),
        (40, 'confirmed', 'Confirmed',),
        # (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # CATEGORY = Choices(
    #     (30, 'music', 'Music'),
    #     (40, 'performance', 'Performance'),
    #     (50, 'singing', 'Singing'),
    # )

    # category = models.IntegerField(
    #     choices=CATEGORY,
    # )

    # KIND = Choices(
    #     (10, 'official', 'Official'),
    #     (20, 'practice', 'Practice'),
    #     (30, 'composite', 'Composite'),
    # )

    # kind = models.IntegerField(
    #     choices=KIND,
    # )

    # num = models.IntegerField(
    # )

    points = models.IntegerField(
        help_text="""
            The number of points (0-100)""",
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(
                100,
                message='Points must be between 0 - 100',
            ),
            MinValueValidator(
                0,
                message='Points must be between 0 - 100',
            ),
        ]
    )

    legacy_panelist = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # FKs
    song = models.ForeignKey(
        'Song',
        related_name='scores',
        on_delete=models.CASCADE,
    )

    panelist = models.ForeignKey(
        'Panelist',
        related_name='scores',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            ('song', 'panelist',),
        )

    class JSONAPIMeta:
        resource_name = "score"

    def __str__(self):
        return str(self.pk)


    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        Competitor = apps.get_model('api.competitor')
        if not self.panelist:
            return False
        if not self.panelist.person:
            return False
        if not getattr(self.panelist.person, 'user', False):
            return False
        return any([
            self.song.appearance.round.session.convention.assignments.filter(
                person__user=request.user,
                status__gt=0,
                category__lte=10,
            ),
            self.panelist.person.user == request.user,
            all([
                self.song.appearance.round.panelists.filter(
                    person__user=request.user,
                    status__gt=0,
                ),
                self.song.appearance.round.session.competitors.filter(
                    status=Competitor.STATUS.finished,
                ),
            ]),
            all([
                self.song.appearance.group.officers.filter(
                    person__user=request.user,
                    status__gt=0,
                ),
                self.song.appearance.round.session.competitors.filter(
                    status=Competitor.STATUS.finished,
                ),
            ]),
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_round_manager,
            request.user.is_scoring_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.song.appearance.round.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                # self.song.appearance.status != self.song.appearance.STATUS.verified,
                self.song.appearance.round.status != self.song.appearance.round.STATUS.finished,
            ]),
        ])
