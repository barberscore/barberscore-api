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
from ranking import ORDINAL
from django_fsm_log.models import StateLog
from django.contrib.contenttypes.fields import GenericRelation

# Django
from django.apps import apps
from django.db import models
from django.utils.functional import cached_property
from django.urls import reverse

# First-Party
from api.tasks import send_csa
from api.tasks import create_round_oss
from api.tasks import create_csa_report
from api.tasks import save_csa_round

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

    oss = models.FileField(
        null=True,
        blank=True,
    )
    sa = models.FileField(
        null=True,
        blank=True,
    )
    csa = models.FileField(
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='rounds',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='rounds',
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
    def calculate(self):
        for appearance in self.appearances.all():
            for song in appearance.songs.all():
                song.calculate()
                song.save()
            appearance.calculate()
            appearance.save()
        return

    def rank(self):
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
            competitor__status__gt=0,
        ).distinct().order_by('-tot_points')
        points = [x.tot_points for x in appearances]
        ranked = Ranking(points, strategy=ORDINAL, start=1)
        for appearance in appearances:
            appearance.tot_rank = ranked.rank(appearance.tot_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
            competitor__status__gt=0,
        ).distinct().order_by('-mus_points')
        points = [x.mus_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.mus_rank = ranked.rank(appearance.mus_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
            competitor__status__gt=0,
        ).distinct().order_by('-per_points')
        points = [x.per_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.per_rank = ranked.rank(appearance.per_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_ranked=True,
            competitor__status__gt=0,
        ).distinct().order_by('-sng_points')
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
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-tot_points')
        points = [x.tot_points for x in songs]
        ranked = Ranking(points, strategy=ORDINAL, start=1)
        for song in songs:
            song.tot_rank = ranked.rank(song.tot_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_ranked=True,
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-mus_points')
        points = [x.mus_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.mus_rank = ranked.rank(song.mus_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_ranked=True,
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-per_points')
        points = [x.per_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.per_rank = ranked.rank(song.per_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_ranked=True,
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-sng_points')
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
        source='*',
        target=STATUS.new,
    )
    def reset(self, *args, **kwargs):
        Grid = apps.get_model('api.grid')
        panelists = self.panelists.all()
        appearances = self.appearances.all()
        grids = Grid.objects.filter(
            appearance__in=appearances,
        )
        grids.update(appearance=None)
        panelists.delete()
        appearances.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        Assignment = apps.get_model('api.assignment')
        # Build the panel
        # First, create all CAs (no num)
        assignments = self.session.convention.assignments.filter(
            status=Assignment.STATUS.active,
            kind__in=[
                Assignment.KIND.official,
                Assignment.KIND.practice,
            ],
            category__gte=Assignment.CATEGORY.ca,
        ).order_by(
            'kind',
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        for assignment in assignments:
            self.panelists.create(
                kind=assignment.kind,
                category=assignment.category,
                person=assignment.person,
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
            # MT
            mt = self.session.competitors.filter(
                status=Competitor.STATUS.finished,
            ).order_by(
                '-tot_points',
                '-sng_points',
                '-per_points',
            ).first()
            self.appearances.create(
                competitor=mt,
                num=0,
            )
        return


    @fsm_log_by
    @transition(field=status, source=[STATUS.built], target=STATUS.started)
    def start(self, *args, **kwargs):
        Panelist = apps.get_model('api.panelist')
        # Number the official panelists
        officials = self.panelists.filter(
            kind=Panelist.KIND.official,
            category__gt=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        i = 0
        for official in officials:
            i += 1
            official.num = i
            official.save()
        # Number the practice panelists
        practices = self.panelists.filter(
            kind=Panelist.KIND.practice,
            category__gt=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        i = 50
        for practice in practices:
            i += 1
            practice.num = i
            practice.save()
        # Build the appearances
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
        # First, calculate all denormalized scores.
        self.calculate()
        # Run rankings.
        self.rank()
        self.session.rank()

        # Run contests by round
        contests = self.session.contests.filter(
            status__gt=0,
            award__rounds=self.num,
        )
        for contest in contests:
            contest.calculate()
            contest.save()

        # No next round.
        if self.kind == self.KIND.finals:
            save_csa_round(self)
            return

        # Get spots available
        spots = self.spots

        # Get all multi competitors.
        multis = self.session.competitors.filter(
            status__gt=0,
            is_multi=True,
        )

        if spots:
            # All those above 73.0 advance automatically
            automatics = multis.filter(
                tot_score__gte=73.0,
            )
            cnt = automatics.count()
            # create list of advancers
            advancers = [a.id for a in automatics]
            diff = spots - cnt
            adds = multis.exclude(
                id__in=advancers,
            ).order_by(
                '-tot_points',
                '-sng_points',
                '-per_points',
            )[:diff]
            for a in adds:
                advancers.append(a.id)
        else:
            advancers = [a.id for a in multis]

        # Reset draw
        self.appearances.update(draw=None)
        # Get advancers and draw
        appearances = self.appearances.filter(
            competitor__id__in=advancers,
        ).order_by('?')
        i = 1
        for appearance in appearances:
            appearance.draw = i
            appearance.save()
            i += 1
        # create MT
        mt = self.appearances.filter(
            draw=None,
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
            ).first()
        mt.draw = 0
        mt.save()
        save_csa_round(self)
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.verified], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        content = create_round_oss(self)
        self.oss.save(
            "{0}-oss".format(
                self.id,
            ),
            content,
        )
        finishers = self.appearances.filter(
            draw=None,
        )
        for finisher in finishers:
            finisher.competitor.finish()
            finisher.competitor.save()
        if self.kind != self.KIND.finals:
            next_round = self.session.rounds.get(num=self.num + 1)
            next_round.build()
            next_round.save()
        return
