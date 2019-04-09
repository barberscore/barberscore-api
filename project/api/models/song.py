
# Standard Library
import logging
import uuid
from builtins import round as rnd

# Third-Party
from django_fsm import FSMIntegerField
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Sum, Min, Max, Count, StdDev
from django.contrib.postgres.fields import ArrayField, JSONField

log = logging.getLogger(__name__)


class Song(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'verified', 'Verified',),
        # (20, 'entered', 'Entered',),
        # (30, 'flagged', 'Flagged',),
        # (35, 'verified', 'Verified',),
        (38, 'finished', 'Finished',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
        (90, 'announced', 'Announced',),
        (95, 'archived', 'Archived',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
    )

    legacy_num = models.IntegerField(
        null=True,
        blank=True,
    )

    legacy_chart = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    legacy_total = models.IntegerField(
        null=True,
        blank=True,
    )

    asterisks = ArrayField(
        base_field=models.IntegerField(
        ),
        default=list,
        blank=True,
    )

    dixons = ArrayField(
        base_field=models.IntegerField(
        ),
        default=list,
        blank=True,
    )

    PENALTY = Choices(
        (10, 'patreg', 'Primarily Patriotic/Religious Intent',),
        (30, 'accompaniment', 'Instrumental Accompaniment',),
        (40, 'texture', 'Chorus Exceeding 4-Part Texture',),
        (50, 'enhancement', 'Sound Equipment or Electronic Enhancement',),
    )

    penalties = ArrayField(
        base_field=models.IntegerField(
            choices=PENALTY,
        ),
        default=list,
        blank=True,
    )

    stats = JSONField(
        null=True,
        blank=True,
    )

    # FKs
    appearance = models.ForeignKey(
        'Appearance',
        related_name='songs',
        on_delete=models.CASCADE,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class Meta:
        unique_together = (
            ('appearance', 'num',),
        )
        get_latest_by = ['num']

    class JSONAPIMeta:
        resource_name = "song"

    def __str__(self):
        return str(self.id)

    # Methods
    def get_asterisks(self):
        """
        Check to see if the song produces a category variance (asterisk)

        Returns a list of categories that produced an asterisk.
        """
        # Set Flag
        asterisks = []
        # Get Averages by category
        categories = self.scores.filter(
            panelist__kind=10,
        ).values(
            'panelist__category',
        ).annotate(
            avg=Avg('points'),
        )
        for category in categories:
            category_scores = self.scores.filter(
                panelist__category=category['panelist__category'],
                panelist__kind=10,
            )
            for score in category_scores:
                is_asterisk = abs(score.points - category['avg']) > 5
                if is_asterisk:
                    asterisks.append(category['panelist__category'])
                    continue
        asterisks = list(set(asterisks))
        return asterisks

    def get_dixons(self):
        """
        Check to see if the song produces a spread error (Dixon's Q)

        Returns a list of categories that produced a Dixon's Q.
        """
        # Set flag
        output = []
        # Confidence thresholds
        confidence = {
            '3': 0.941,
            '6': .56,
            '9': .376,
            '12': .437,
            '15': .338,
        }
        # Only use official scores.
        scores = self.scores.filter(
            panelist__kind=10,
        )
        # Get the totals
        aggregates = scores.aggregate(
            cnt=Count('id'),
            max=Max('points'),
            min=Min('points'),
            spread=Max('points') - Min('points'),
        )
        # Check for validity.
        if aggregates['cnt'] < 3:
            return RuntimeError('Panel too small error')
        # Bypass to avoid division by zero
        if not aggregates['spread']:
            return output
        # Order the scores
        ascending = scores.order_by('points')
        descending = scores.order_by('-points')
        # Separate check for single-panel
        if aggregates['cnt'] == '3':
            if abs(ascending[0].points - ascending[1].points) >= 10:
                output.append(ascending[0].panelist.category)
            if abs(descending[0].points - descending[1].points) >= 10:
                output.append(descending[0].panelist.category)
            return output

        # Otherwise, run the checks, both ascending and descending
        critical = confidence[str(aggregates['cnt'])]
        ascending_distance = abs(ascending[0].points - ascending[1].points)
        ascending_q = ascending_distance / aggregates['spread']
        if ascending_q > critical and ascending_distance > 4:
            output.append(ascending[0].panelist.category)
        descending_distance = abs(descending[0].points - descending[1].points)
        descending_q = descending_distance / aggregates['spread']
        if descending_q > critical and descending_distance > 4:
            output.append(descending[0].panelist.category)
        return output


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
            self.appearance.round.status == self.appearance.round.STATUS.published,
            self.appearance.round.session.convention.assignments.filter(
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
                self.appearance.round.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.appearance.round.status < self.appearance.round.STATUS.verified,
            ]),
        ])
