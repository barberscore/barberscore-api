# Standard Libary
import logging
import random
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ranking import Ranking

# Django
from django.apps import apps
from django.db import models
from django.utils.functional import cached_property
from django.urls import reverse

# First-Party
from api.tasks import send_csa
from api.tasks import create_oss_report
from api.tasks import create_csa_report

log = logging.getLogger(__name__)


class Round(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (20, 'started', 'Started',),
        (27, 'verified', 'Verified',),
        (30, 'finished', 'Finished',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semi-Finals'),
        (3, 'quarters', 'Quarter-Finals'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    num = models.IntegerField(
        default=0,
    )

    spots = models.IntegerField(
        null=True,
        blank=True,
    )

    date = models.DateField(
        null=True,
        blank=True,
    )

    footnotes = models.TextField(
        help_text="""
            Freeform text field; will print on OSS.""",
        blank=True,
    )

    oss_report = models.FileField(
        null=True,
        blank=True,
    )
    sa_report = models.FileField(
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='rounds',
        on_delete=models.CASCADE,
    )

    @cached_property
    def announcements(self):
        return reverse(
            'round-announcements',
            args=[str(self.id)]
        )

    @cached_property
    def oss(self):
        return reverse(
            'round-oss',
            args=[str(self.id)]
        )

    @cached_property
    def sa(self):
        return reverse(
            'round-sa',
            args=[str(self.id)]
        )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'kind',),
        )
        get_latest_by = [
            'num',
        ]

    class JSONAPIMeta:
        resource_name = "round"

    def __str__(self):
        return "{0} {1} {2}".format(
            self.session.convention.name,
            self.session.get_kind_display(),
            self.get_kind_display(),
        )

    # Methods
    def rank(self):
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
        ).order_by('-tot_points')
        points = [x.tot_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.tot_rank = ranked.rank(appearance.tot_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
        ).order_by('-mus_points')
        points = [x.mus_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.mus_rank = ranked.rank(appearance.mus_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
        ).order_by('-per_points')
        points = [x.per_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.per_rank = ranked.rank(appearance.per_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
        ).order_by('-sng_points')
        points = [x.sng_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.sng_rank = ranked.rank(appearance.sng_points)
            appearance.save()
        # Songs ranked relative to Round
        Song = apps.get_model('api.song')
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_ranked=True,
        ).order_by('-tot_points')
        points = [x.tot_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.tot_rank = ranked.rank(song.tot_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_ranked=True,
        ).order_by('-mus_points')
        points = [x.mus_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.mus_rank = ranked.rank(song.mus_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_ranked=True,
        ).order_by('-per_points')
        points = [x.per_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.per_rank = ranked.rank(song.per_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_ranked=True,
        ).order_by('-sng_points')
        points = [x.sng_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.sng_rank = ranked.rank(song.sng_points)
            song.save()
        return

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
            request.user.is_convention_manager,
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
                self.status != self.STATUS.finished,
            ]),
        ])


    # Methods

    # Round Conditions
    def can_build(self):
        return True

    # Round Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        Assignment = apps.get_model('api.assignment')
        # build the panel
        i = 0
        assignments = self.session.convention.assignments.filter(
            status=Assignment.STATUS.active,
            category__gte=Assignment.CATEGORY.ca,
        )
        for assignment in assignments:
            if assignment.category == Assignment.CATEGORY.ca:
                num = None
            else:
                i += 1
                num = i
            self.panelists.create(
                kind=assignment.kind,
                category=assignment.category,
                person=assignment.person,
                num=num,
            )
        # build the appearances
        Competitor = apps.get_model('api.competitor')
        Grid = apps.get_model('api.grid')
        competitors = self.session.competitors.filter(
            status__gt=0,
        )
        if self.num == 1:
            for competitor in competitors:
                appearance = competitor.appearances.create(
                    round=self,
                    num=competitor.entry.draw,
                )
        else:
            prior_round = self.session.rounds.get(num=self.num - 1)
            prior_appearances = prior_round.appearances.filter(
                draw__isnull=False,
            )
            for prior_appearance in prior_appearances:
                self.appearances.create(
                    competitor=prior_appearance.competitor,
                    num=prior_appearance.draw,
                )
        return


    @fsm_log_by
    @transition(field=status, source=[STATUS.built], target=STATUS.started)
    def start(self, *args, **kwargs):
        appearances = self.appearances.all()
        for appearance in appearances:
            appearance.build()
            appearance.save()
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.verified)
    def verify(self, *args, **kwargs):
        Competitor = apps.get_model('api.competitor')
        Contestant = apps.get_model('api.contestant')
        # If re-verifying, simply re-draw
        if self.status == self.STATUS.verified:
            appearances = self.appearances.filter(
                competitor__status__gt=0,
            ).order_by('?')
            i = 1
            for appearance in appearances:
                appearance.draw = i
                appearance.save()
                i += 1
            return

        # First, calculate all denormalized scores.
        self.session.calculate()
        # Recursively run rankings.
        for round in self.session.rounds.all():
            round.rank()
        self.session.rank()

        # Run contests by round
        contests = self.session.contests.filter(
            status__gt=0,
            award__rounds=self.num,
        )
        for contest in contests:
            contest.calculate()
            contest.save()

        # "Finish" everyone if finals.
        if self.kind == self.KIND.finals:
            competitors = self.session.competitors.filter(
                status__gt=0,
            )
            for competitor in competitors:
                competitor.finish()
                competitor.save()
            return

        # Get spots available
        spots = self.session.rounds.get(num=self.num + 1).spots

        # get primary contest
        contest = self.session.contests.get(is_primary=True)
        if contest.award.level == contest.award.LEVEL.qualifier:
            # Uses absolute cutoff.
            automatics = Competitor.objects.filter(
                status__gt=0,
                entry__contestants__contest=contest,
                entry__contestants__status=Contestant.STATUS.included,
                tot_score__gte=contest.award.advance,
            ).distinct(
            )
        elif contest.award.level == contest.award.LEVEL.championship:
            # Get the top scorer
            top = Competitor.objects.filter(
                status__gt=0,
                entry__contestants__contest=contest,
                entry__contestants__status=Contestant.STATUS.included,
            ).distinct(
            ).order_by(
                '-tot_points',
            ).first()
            # Derive the approve threshold from that top score.
            # 4.0 points a constant, from SCJC David Mills
            advance = top.tot_score - 4.0
            automatics = Competitor.objects.filter(
                status__gt=0,
                entry__contestants__contest=contest,
                entry__contestants__status=Contestant.STATUS.included,
                tot_score__gte=advance,
            ).distinct(
            )

        # list comprehension since we're slicing queryset
        advancers = [x.id for x in automatics]
        # Append up to spots available.
        if spots:
            diff = spots - len(advancers)
        else:
            diff = 0
        if diff > 0:
            # Append to advancers list if there is room to do so
            excludes = advancers
            adds = self.session.competitors.filter(
                status__gt=0,
                is_multi=True,
            ).exclude(
                id__in=excludes,
            ).distinct(
            ).order_by(
                '-tot_points',
            )[:diff]
            for a in adds:
                advancers.append(a.id)

        # Set all remaining to finished..
        competitors = self.session.competitors.filter(
            status__gt=0,
        ).exclude(
            id__in=advancers,
        )
        for competitor in competitors:
            competitor.finish()
            competitor.save()
        # Get advancers and draw
        appearances = self.appearances.filter(
            competitor__status__gt=0,
        ).order_by('?')
        i = 1
        for appearance in appearances:
            appearance.draw = i
            appearance.save()
            i += 1
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.verified], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        Competitor = apps.get_model('api.competitor')
        if self.kind != self.KIND.finals:
            next_round = self.session.rounds.get(num=self.num + 1)
            next_round.build()
            next_round.save()
        content = create_oss_report(self, full=False)
        self.oss_report.save(
            "{0}-oss".format(
                self.id,
            ),
            content,
        )
        cs = self.session.competitors.filter(
            status=Competitor.STATUS.finished,
        )
        for c in cs:
            context = {
                'competitor': c,
                'round': self,
            }
            # send_csa.delay(context)
        return
