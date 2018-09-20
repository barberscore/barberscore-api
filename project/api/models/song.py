
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
from django.apps import apps
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Sum, Min, Max, Count
from django.contrib.postgres.fields import ArrayField

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

    legacy_chart = models.CharField(
        max_length=255,
        blank=True,
        null=True,
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
        Score = apps.get_model('api.score')
        tot = Sum('points')
        mus = Sum('points', filter=Q(category=Score.CATEGORY.music))
        per = Sum('points', filter=Q(category=Score.CATEGORY.performance))
        sng = Sum('points', filter=Q(category=Score.CATEGORY.singing))
        officials = Score.objects.filter(
            song=self,
            kind=Score.KIND.official,
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
            category=Score.CATEGORY.music,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        per = officials.filter(
            category=Score.CATEGORY.performance,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        sng = officials.filter(
            category=Score.CATEGORY.singing,
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

    # Methods
    def get_asterisks(self):
        """Check to see if the score produces a category variance (asterisk)"""
        asterisks = []
        scores = self.scores.all()
        categories = self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).values(
            'category',
        ).annotate(
            avg=Avg('points'),
        )
        for category in categories:
            is_asterisk = [
                abs(i.points - category['avg']) > 5
                for i in scores
                if i.category == category['category']
            ][0]
            if is_asterisk:
                asterisks.append(category['category'])
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
            kind=self.scores.model.KIND.official,
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
                output.append(ascending[0].category)
            if abs(descending[0].points - descending[1].points) >= 10:
                output.append(descending[0].category)
            return output
        critical = confidence[str(aggregates['cnt'])]
        ascending_distance = abs(ascending[0].points - ascending[1].points)
        ascending_q = ascending_distance / aggregates['spread']
        if ascending_q > critical and ascending_distance > 5:
            output.append(ascending[0].category)
        descending_distance = abs(descending[0].points - descending[1].points)
        descending_q = descending_distance / aggregates['spread']
        if descending_q > critical and descending_distance > 5:
            output.append(descending[0].category)
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
                self.appearance.status != self.appearance.STATUS.verified,
                self.appearance.round.status != self.appearance.round.STATUS.finished,
            ]),
        ])
