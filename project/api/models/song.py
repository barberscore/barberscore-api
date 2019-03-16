
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

    def save(self, *args, **kwargs):
        # Save all scores as single-digit
        if self.mus_score:
            self.mus_score = rnd(self.mus_score, 1)
        if self.per_score:
            self.per_score = rnd(self.per_score, 1)
        if self.sng_score:
            self.sng_score = rnd(self.sng_score, 1)
        if self.tot_score:
            self.tot_score = rnd(self.tot_score, 1)
        super().save(*args, **kwargs)

    # Methods
    def calculate(self):
        Panelist = apps.get_model('api.panelist')
        Score = apps.get_model('api.score')
        tot = Sum('points')
        mus = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.music))
        per = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.performance))
        sng = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.singing))
        officials = Score.objects.filter(
            song=self,
            panelist__kind=Panelist.KIND.official,
        ).annotate(
            tot=tot,
            mus=mus,
            per=per,
            sng=sng,
        )
        tot = officials.aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        mus = officials.filter(
            panelist__category=Panelist.CATEGORY.music,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        per = officials.filter(
            panelist__category=Panelist.CATEGORY.performance,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        sng = officials.filter(
            panelist__category=Panelist.CATEGORY.singing,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        self.tot_points = tot['sum']
        self.tot_score = tot['avg']
        self.mus_points = mus['sum']
        self.mus_score = mus['avg']
        self.per_points = per['sum']
        self.per_score = per['avg']
        self.sng_points = sng['sum']
        self.sng_score = sng['avg']

    def get_stats(self):
        stats = {}
        totals = self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).aggregate(
            avg=Avg('points'),
            sum=Sum('points'),
            dev=StdDev('points'),
        )
        stats['tot'] = totals
        category_map = {
            30: 'mus',
            40: 'per',
            50: 'sng',
        }
        categories = self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).values(
            'category',
        ).annotate(
            avg=Avg('points'),
            sum=Sum('points'),
            dev=StdDev('points'),
        )
        for category in categories:
            name = category_map[category.pop('category')]
            stats[name] = category
        return stats

    # Methods
    def get_asterisks(self):
        """Check to see if the score produces a category variance (asterisk)"""
        asterisks = []
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
        # Dixon's Q Test
        output = []
        confidence = {
            '3': 0.941,
            '6': .56,
            '9': .376,
            '12': .437,
            '15': .338,
        }
        scores = self.scores.filter(
            panelist__kind=10,
        )
        aggregates = scores.aggregate(
            max=Max('points'),
            min=Min('points'),
            cnt=Count('id'),
            spread=Max('points') - Min('points'),
        )
        # Bypass to avoid division by zero
        if not aggregates['spread']:
            return output
        if aggregates['cnt'] < 3:
            return RuntimeError('Panel too small error')
        ascending = scores.order_by('points')
        descending = scores.order_by('-points')
        if aggregates['cnt'] == '3':
            if abs(ascending[0].points - ascending[1].points) >= 10:
                output.append(ascending[0].panelist.category)
            if abs(descending[0].points - descending[1].points) >= 10:
                output.append(descending[0].panelist.category)
            return output
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

    def get_variance(self):
        variance = any([
            self.get_asterisks(),
            self.get_dixons(),
        ])
        return variance

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
                # self.appearance.status != self.appearance.STATUS.verified,
                self.appearance.round.status != self.appearance.round.STATUS.finished,
            ]),
        ])
