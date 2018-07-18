# Standard Libary
import datetime
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
from ranking import Ranking

# Django
from django.apps import apps
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property

# First-Party
from api.tasks import send_session
from api.tasks import send_session_reports

log = logging.getLogger(__name__)


class Session(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'built', 'Built',),
        (4, 'opened', 'Opened',),
        (8, 'closed', 'Closed',),
        (10, 'verified', 'Verified',),
        (20, 'started', 'Started',),
        (30, 'finished', 'Finished',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of session.  Generally this will be either quartet or chorus.
        """,
        choices=KIND,
    )

    GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    gender = models.IntegerField(
        help_text="""
            The gender of session.
        """,
        choices=GENDER,
        null=True,
        blank=True,
    )

    num_rounds = models.IntegerField(
    )

    is_invitational = models.BooleanField(
        help_text="""Invite-only (v. Open).""",
        default=False,
    )

    description = models.TextField(
        help_text="""
            The Public Description.  Will be sent in all email communications.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).  Will not be sent.""",
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
    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
        on_delete=models.CASCADE,
    )

    # Properties
    @cached_property
    def legacy(self):
        return reverse(
            'session-legacy',
            args=[str(self.id)]
        )

    @cached_property
    def drcj(self):
        return reverse(
            'session-drcj',
            args=[(self.id)]
        )

    @cached_property
    def contact(self):
        return reverse(
            'session-contact',
            args=[str(self.id)]
        )

    @cached_property
    def oss(self):
        return reverse(
            'session-oss',
            args=[str(self.id)]
        )

    @cached_property
    def sa(self):
        return reverse(
            'session-sa',
            args=[str(self.id)]
        )

    # Internals
    class JSONAPIMeta:
        resource_name = "session"

    def __str__(self):
        return "{0} {1}".format(
            self.convention,
            self.get_kind_display(),
        )

    # Methods
    def calculate(self):
        competitors = self.competitors.filter(
            status__gt=0,
        )
        for competitor in competitors:
            for appearance in competitor.appearances.all():
                for song in appearance.songs.all():
                    song.calculate()
                    song.save()
                appearance.calculate()
                appearance.save()
            competitor.calculate()
            competitor.save()
        return


    def rank(self):
        competitors = self.competitors.filter(
            is_ranked=True,
        ).order_by('-tot_points')
        points = [x.tot_points for x in competitors]
        ranked = Ranking(points, start=1)
        for competitor in competitors:
            competitor.tot_rank = ranked.rank(competitor.tot_points)
            competitor.save()
        competitors = self.competitors.filter(
            is_ranked=True,
        ).order_by('-mus_points')
        points = [x.mus_points for x in competitors]
        ranked = Ranking(points, start=1)
        for competitor in competitors:
            competitor.mus_rank = ranked.rank(competitor.mus_points)
            competitor.save()
        competitors = self.competitors.filter(
            is_ranked=True,
        ).order_by('-per_points')
        points = [x.per_points for x in competitors]
        ranked = Ranking(points, start=1)
        for competitor in competitors:
            competitor.per_rank = ranked.rank(competitor.per_points)
            competitor.save()
        competitors = self.competitors.filter(
            is_ranked=True,
        ).order_by('-sng_points')
        points = [x.sng_points for x in competitors]
        ranked = Ranking(points, start=1)
        for competitor in competitors:
            competitor.sng_rank = ranked.rank(competitor.sng_points)
            competitor.save()
        return

    # Session Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.convention.assignments.filter(
                person__user=request.user,
                category__lt=30,
                kind=10,
            ),
        ])

    # Session Conditions
    def can_build_session(self):
        return all([
            self.convention.grantors.count() > 0,
            self.num_rounds,
        ])

    def can_open_session(self):
        Contest = apps.get_model('api.contest')
        return all([
            self.contests.filter(status=Contest.STATUS.included),
        ])

    def can_close_session(self):
        Entry = apps.get_model('api.entry')
        return all([
            self.convention.close_date < datetime.date.today(),
            self.entries.all(),
            self.entries.exclude(
                status__in=[
                    Entry.STATUS.approved,
                    Entry.STATUS.withdrawn,
                ],
            ).count() == 0,
        ])

    # Session Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build_session],
    )
    def build(self, *args, **kwargs):
        """Build session contests."""
        grantors = self.convention.grantors.order_by('group__tree_sort')
        i = 0
        for grantor in grantors:
            awards = grantor.group.awards.filter(
                status=grantor.group.awards.model.STATUS.active,
                kind=self.kind,
                season=self.convention.season,
            ).order_by('tree_sort')
            for award in awards:
                i += 1
                # Could also do some logic here for more precision
                self.contests.create(
                    status=self.contests.model.STATUS.included,
                    award=award,
                    num=i,
                )
        for i in range(self.num_rounds):
            num = i + 1
            kind = self.num_rounds - i
            if kind == 1:
                spots = 10
            else:
                spots = None
            self.rounds.create(
                num=num,
                kind=kind,
                spots=spots,
            )
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.built,
        target=STATUS.opened,
        conditions=[can_open_session],
    )
    def open(self, *args, **kwargs):
        """Make session available for entry."""
        if not self.is_invitational:
            context = {'session': self}
            send_session.delay('session_open.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.opened,
        target=STATUS.closed,
        conditions=[can_close_session]
    )
    def close(self, *args, **kwargs):
        """Make session unavailable and set initial draw."""
        # Remove orphaned entries
        entries = self.entries.filter(
            status=self.entries.model.STATUS.new,
        )
        for entry in entries:
            entry.delete()
        # Withdraw dangling invitations
        entries = self.entries.filter(
            status=self.entries.model.STATUS.invited,
        )
        for entry in entries:
            entry.withdraw()
            entry.save()
        # Set initial draw for all Approved entries.
        entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        ).order_by('?')
        i = 1
        for entry in entries:
            entry.draw = i
            entry.save()
            i += 1
        if not self.is_invitational:
            context = {'session': self}
            send_session.delay('session_close.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.closed, STATUS.verified],
        target=STATUS.verified,
        conditions=[],
    )
    def verify(self, *args, **kwargs):
        """Make draw public."""
        context = {
            'session': self,
            'host_name': settings.HOST_NAME,
        }
        send_session_reports.delay('session_reports.txt', context)
        # approved_entries = self.entries.filter(
        #     status=self.entries.model.STATUS.approved,
        # ).order_by('draw')
        # context = {'session': self, 'approved_entries': approved_entries}
        # send_session.delay('session_verify.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.verified,
        target=STATUS.started,
        conditions=[],
    )
    def start(self, *args, **kwargs):
        """Button up session and transfer to CA."""
        #  Create and send the reports
        context = {
            'session': self,
            'host_name': settings.HOST_NAME,
        }
        send_session_reports.delay('session_reports.txt', context)
        # delete orphans
        # for entry in self.entries.filter(status=Entry.STATUS.new):
        #     entry.delete()
        # Build Competitor List
        entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        )
        for entry in entries:
            # Set is_ranked=True if they are competing for a primary award.
            is_ranked = bool(entry.contestants.filter(
                contest__award__is_primary=True,
                status__gt=0,
            ))
            # Set is_multi=True if they are competiting for at least
            # one multi-round award.
            is_multi = bool(entry.contestants.filter(
                contest__award__rounds__gt=1,
                status__gt=0,
            ))
            competitor = self.competitors.create(
                entry=entry,
                group=entry.group,
                is_ranked=is_ranked,
                is_multi=is_multi,
            )
            competitor.start()
            competitor.save()
        # Build Round
        round = self.rounds.get(
            num=1,
        )
        round.build()
        round.save()
        # notify entrants
        context = {
            'session': self,
        }
        send_session.delay('session_start.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.started, STATUS.finished],
        target=STATUS.finished,
        conditions=[],
    )
    def finish(self, *args, **kwargs):
        # create_oss_report(self)
        # create_sa_report(self)
        return
