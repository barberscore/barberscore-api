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


class Song(TimeStampedModel):
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
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.appearance,
                    self.num,
                ]
            )
        )
        super().save(*args, **kwargs)

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
        mus_scores = self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.music,
        )
        mus_avg = mus_scores.aggregate(avg=models.Avg('points'))['avg']
        for score in mus_scores:
            if abs(score.points - mus_avg) > 5:
                return True
        per_scores = self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.performance,
        )
        per_avg = per_scores.aggregate(avg=models.Avg('points'))['avg']
        for score in per_scores:
            if abs(score.points - per_avg) > 5:
                return True
        sng_scores = self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.singing,
        )
        sng_avg = sng_scores.aggregate(avg=models.Avg('points'))['avg']
        for score in sng_scores:
            if abs(score.points - sng_avg) > 5:
                return True

        ordered_asc = self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).order_by('points')
        ultimate = ordered_asc[0].points
        penultimate = ordered_asc[1].points
        if penultimate - ultimate > 5:
            return True
        ordered_dsc = self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).order_by('-points')
        ultimate = ordered_dsc[0].points
        penultimate = ordered_dsc[1].points
        if ultimate - penultimate > 5:
            return True
        return False

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return request.user.is_scoring_manager

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        assi = bool(self.appearance.competitor.session.convention.assignments.filter(
            person__user=request.user,
            status__gt=0,
        ))
        return assi

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return request.user.is_scoring_manager

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        assi = bool(self.appearance.competitor.session.convention.assignments.filter(
            person__user=request.user,
            status__gt=0,
        ))
        return assi

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.announced)
    def announce(self, *args, **kwargs):
        return
