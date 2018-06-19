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
from api.tasks import create_ors_report

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
    )

    spots = models.IntegerField(
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
        return "{0} {1}".format(
            self.session.convention.name,
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
        return

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.person.officers.filter(office__is_scoring_manager=True),
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.session.convention.assignments.filter(
                person__user=request.user,
                category__in=[
                    10,
                    20,
                ],
                kind=10,
            ),
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
        # build the panel
        assignments = self.session.convention.assignments.filter(
            status=self.session.convention.assignments.model.STATUS.active,
            category__gt=self.session.convention.assignments.model.CATEGORY.ca,
        )
        for assignment in assignments:
            self.panelists.create(
                kind=assignment.kind,
                category=assignment.category,
                person=assignment.person,
            )
        # build the appearances
        Competitor = apps.get_model('api.competitor')
        competitors = self.session.competitors.filter(
            status__gt=0,
        )
        for competitor in competitors:
            appearance = competitor.appearances.create(
                round=self,
                num=competitor.draw,
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
    @transition(field=status, source=[STATUS.started], target=STATUS.verified)
    def verify(self, *args, **kwargs):
        # First, calculate all denormalized scores.
        self.session.calculate()
        # Recursively run rankings.
        for round in self.session.rounds.all():
            for appearance in round.appearances.all():
                appearance.rank()
            round.rank()
        self.session.rank()

        # "Finish" everyone if finals.
        if self.kind == self.KIND.finals:
            competitors = self.session.competitors.filter(
                status__gt=0,
            )
            for competitor in competitors:
                competitor.finish()
                competitor.save()
            contests = self.session.contests.filter(
                status__gt=0,
            )
            for contest in contests:
                contest.calculate()
                contest.save()
            return

        # Get spots available
        spots = self.session.rounds.get(num=self.num + 1).spots

        # Instantiate the advancing list
        advancers = []

        for contest in self.session.contests.filter(award__rounds__gt=1):
            # Qualifiers have an absolute score cutoff
            if contest.award.level == contest.award.LEVEL.qualifier:
                # Uses absolute cutoff.
                contestants = contest.contestants.filter(
                    status__gt=0,
                    entry__competitor__tot_score__gte=contest.award.advance,
                )
                for contestant in contestants:
                    advancers.append(contestant.entry.competitor)
            # Championships are relative.
            elif contest.award.level == contest.award.LEVEL.championship:
                # Get the top scorer
                contestants = contest.contestants.filter(
                    status__gt=0,
                    tot_points__gt=0,
                ).order_by(
                    '-entry__competitor__tot_points',
                )
                if contestants:
                    top = contestants.first()
                else:
                    continue
                # Derive the approve threshold from that top score.
                approve = top.entry.competitor.tot_score - 4.0
                contestants = contest.contestants.filter(
                    status__gt=0,
                    tot_score__gte=approve,
                )
                for contestant in contestants:
                    advancers.append(contestant.competitor)
        # Remove duplicates
        advancers = list(set(advancers))
        # Append up to spots available.
        if spots:
            diff = spots - len(advancers)
        else:
            diff = 0
        if diff > 0:
            adds = self.session.competitors.filter(
                entry__contestants__contest__award__rounds__gt=1,
            ).distinct(
            ).order_by(
                '-tot_points',
            )[:diff]
            for add in adds:
                if add not in advancers:
                    advancers.append(add)

        # Set all remaining to finished..
        advancers_id = [x.id for x in advancers]
        competitors = self.session.competitors.filter(
            status__gt=0,
        ).exclude(
            id__in=advancers_id,
        )
        for competitor in competitors:
            competitor.finish()
            competitor.save()
        competitors = self.session.competitors.filter(
            status__gt=0,
        ).order_by('?')
        i = 1
        for competitor in competitors:
            competitor.draw = i
            competitor.save()
            i += 1
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.verified], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        if self.kind == self.KIND.finals:
            return
        round = self.session.rounds.get(num=self.num + 1)
        round.build()
        round.save()
        return

