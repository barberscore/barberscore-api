# Standard Libary
import logging
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.apps import apps
from django.db import models

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

    # Privates
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    mus_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    per_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_rank = models.IntegerField(
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
    def calculate(self):
        self.mus_points = self.scores.filter(
            kind=10,
            category=30,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']
        self.per_points = self.scores.filter(
            kind=10,
            category=40,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']
        self.sng_points = self.scores.filter(
            kind=10,
            category=50,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

        self.tot_points = self.scores.filter(
            kind=10,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']
        self.mus_score = self.scores.filter(
            kind=10,
            category=30,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']
        self.per_score = self.scores.filter(
            kind=10,
            category=40,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']
        self.sng_score = self.scores.filter(
            kind=10,
            category=50,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']
        self.tot_score = self.scores.filter(
            kind=10,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    def check_variance(self):
        is_variance = False
        # Category Average
        mus_scores = self.scores.filter(
            category=self.scores.model.CATEGORY.music,
        )
        mus_avg = mus_scores.filter(
            kind=self.scores.model.KIND.official,
        ).aggregate(avg=models.Avg('points'))['avg']
        for score in mus_scores:
            if abs(score.points - mus_avg) > 5:
                score.is_flagged = True
                if score.kind == score.KIND.official:
                    is_variance = True
            else:
                score.is_flagged = False
            score.save()
        per_scores = self.scores.filter(
            category=self.scores.model.CATEGORY.performance,
        )
        per_avg = per_scores.filter(
            kind=self.scores.model.KIND.official,
        ).aggregate(avg=models.Avg('points'))['avg']
        for score in per_scores:
            if abs(score.points - per_avg) > 5:
                score.is_flagged = True
                if score.kind == score.KIND.official:
                    is_variance = True
            else:
                score.is_flagged = False
            score.save()
        sng_scores = self.scores.filter(
            category=self.scores.model.CATEGORY.singing,
        )
        sng_avg = sng_scores.filter(
            kind=self.scores.model.KIND.official,
        ).aggregate(avg=models.Avg('points'))['avg']
        for score in sng_scores:
            if abs(score.points - sng_avg) > 5:
                score.is_flagged = True
                if score.kind == score.KIND.official:
                    is_variance = True
            else:
                score.is_flagged = False
            score.save()
        if is_variance:
            return True

        # Dixon's Q Test
        confidence = {
            '3': 0.941,
            '6': .56,
            '9': .376,
            '12': .437,
            '15': .338,
        }

        ordered_dsc = self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).order_by('-points')
        spread = ordered_dsc.first().points - ordered_dsc.last().points
        size = str(ordered_dsc.count())

        if size == '3':
            ultimate = ordered_dsc[0]
            penultimate = ordered_dsc[1]
            triultimate = ordered_dsc[2]
            if ultimate.points - penultimate.points >= 10:
                ultimate.is_flagged = True
                is_variance = True
            elif penultimate.points - triultimate.points >= 10:
                triultimate.is_flagged = True
                is_variance = True
            else:
                ultimate.is_flagged = False
                triultimate.is_flagged = False
            ultimate.save()
            triultimate.save()
        else:
            ordered_asc = self.scores.filter(
                kind=self.scores.model.KIND.official,
            ).order_by('points')
            ultimate = ordered_asc[0]
            penultimate = ordered_asc[1]
            distance = abs(ultimate.points - penultimate.points)
            q = distance / spread
            critical = confidence[size]
            if q > critical and penultimate.points - ultimate.points > 5:
                ultimate.is_flagged = True
                is_variance = True
            else:
                ultimate.is_flagged = False
            ultimate.save()
            practice_scores = self.scores.filter(
                kind=self.scores.model.KIND.practice,
                points__lte=ultimate.points,
            )
            practice_scores.update(is_flagged=True)
            ordered_dsc = self.scores.filter(
                kind=self.scores.model.KIND.official,
            ).order_by('-points')
            ultimate = ordered_dsc[0]
            penultimate = ordered_dsc[1]
            distance = abs(ultimate.points - penultimate.points)
            q = distance / spread
            critical = confidence[size]
            if q > critical and ultimate.points - penultimate.points > 5:
                ultimate.is_flagged = True
                is_variance = True
            else:
                ultimate.is_flagged = False
            ultimate.save()
            practice_scores = self.scores.filter(
                kind=self.scores.model.KIND.practice,
                points__gte=ultimate.points,
            )
            practice_scores.update(is_flagged=True)
        return is_variance

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
            self.appearance.round.status == self.appearance.round.STATUS.finished,
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
                self.appearance.round.status != self.appearance.round.STATUS.finished,
            ]),
        ])

