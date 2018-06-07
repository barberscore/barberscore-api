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

# Django
from django.apps import apps as api_apps
from django.db import models
from django.utils.functional import cached_property

# First-Party
from api.tasks import create_ors_report

config = api_apps.get_app_config('api')

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
        (25, 'reviewed', 'Reviewed',),
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

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='rounds',
        on_delete=models.CASCADE,
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
        return str(self.id)

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
        # set the panel
        for assignment in self.session.convention.assignments.filter(
            status=self.session.convention.assignments.model.STATUS.active,
            category__gt=self.session.convention.assignments.model.CATEGORY.ca,
        ):
            self.panelists.create(
                kind=assignment.kind,
                category=assignment.category,
                person=assignment.person,
            )
        return


    @fsm_log_by
    @transition(field=status, source=[STATUS.built], target=STATUS.started)
    def start(self, *args, **kwargs):
        panelists = self.panelists.all()
        appearances = self.appearances.all()
        for appearance in appearances:
            i = 1
            while i <= 2:  # Number songs constant
                song = appearance.songs.create(
                    num=i
                )
                for panelist in panelists:
                    song.scores.create(
                        category=panelist.category,
                        kind=panelist.kind,
                        panelist=panelist,
                    )
                i += 1
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.started, STATUS.reviewed], target=STATUS.reviewed)
    def review(self, *args, **kwargs):
        Competitor = config.get_model('Competitor')
        # First, calculate all denormalized scores.
        for competitor in self.session.competitors.all():
            for appearance in competitor.appearances.all():
                for song in appearance.songs.all():
                    song.calculate()
                    song.save()
                appearance.calculate()
                appearance.save()
            competitor.calculate()
            competitor.save()
        # Next run the competitor ranking.
        for competitor in self.session.competitors.all():
            competitor.ranking()
            competitor.save()

        # Switch based on round
        if self.kind == self.KIND.finals:
            # All remaining competitors are "missed" in the sense
            # that they didn't make the (non-existent) cut.
            competitors = self.session.competitors.filter(
                status=Competitor.STATUS.started,
            )
            # All remaining 'miss' the next round.
            for competitor in competitors:
                competitor.miss()
                competitor.save()
            # Determine all the awards.
            for contest in self.session.contests.filter(status__gt=0):
                contest.calculate()
                contest.save()
            create_ors_report(self)
            return
        elif self.kind == self.KIND.quarters:
            spots = 20
        elif self.kind == self.KIND.semis:
            spots = 2
        else:
            raise RuntimeError("No Rounds Remaining")

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
        diff = spots - len(advancers)
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

        # Randomize the list
        random.shuffle(advancers)

        # Set Draw
        i = 1
        for competitor in advancers:
            competitor.draw = i
            competitor.make()
            competitor.save()
            i += 1

        # Set all remaining to missed..
        finishers = Competitor.objects.filter(
            status=Competitor.STATUS.started,
        )
        for competitor in finishers:
            competitor.draw = None
            competitor.miss()
            competitor.save()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.reviewed], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        # Switch based on rounds
        Competitor = config.get_model('Competitor')
        misses = self.session.competitors.filter(
            status=Competitor.STATUS.missed,
        )
        for miss in misses:
            miss.finish()
            miss.save()
        mades = self.session.competitors.filter(
            status=Competitor.STATUS.made,
        )
        for made in mades:
            made.start()
            made.save()
        return

    # @fsm_log_by
    # @transition(field=status, source='*', target=STATUS.announced)
    # def announce(self, *args, **kwargs):

    #     if self.kind != self.KIND.finals:
    #         round = self.session.rounds.create(
    #             num=self.num + 1,
    #             kind=self.kind - 1,
    #         )
    #         for appearance in self.appearances.filter(draw__gt=0):
    #             round.appearances.create(
    #                 entry=appearance.entry,
    #                 num=appearance.draw,
    #                 status=appearance.STATUS.published,
    #             )
    #         for appearance in self.appearances.filter(draw__lte=0):
    #             e = appearance.entry
    #             e.complete()
    #             e.save()
    #         for assignment in self.session.convention.assignments.filter(
    #             status=Assignment.STATUS.active,
    #         ):
    #             round.panelists.create(
    #                 kind=assignment.kind,
    #                 category=assignment.category,
    #                 person=assignment.person,
    #             )
    #         round.verify()
    #         round.save()
    #         return

    # Competitor = config.get_model('Competitor')
    # for entry in self.entries.filter(status=Entry.STATUS.approved):
    #     # Create competitors
    #     # Set is_ranked=True if they are competing for the primary award.
    #     primary = self.contests.get(award__is_primary=True)
    #     is_ranked = bool(entry.contestants.filter(
    #         contest=primary,
    #         status__gt=0,
    #     ))
    #     # Set is_multi=True if they are competiting for at least
    #     # one multi-round award.
    #     is_multi = bool(entry.contestants.filter(
    #         contest__award__rounds__gt=1
    #     ))

    #     competitor = Competitor.objects.create(
    #         session=self,
    #         group=entry.group,
    #         entry=entry,
    #         draw=entry.draw,
    #         is_ranked=is_ranked,
    #         is_multi=is_multi,
    #     )
    #     competitor.start()
    #     competitor.save()
    #     # set the grid
    #     # competitor.grids.create(
    #     #     round=first_round,
    #     #     num=entry.draw,
    #     #     appearance=appearance,
    #     # )
