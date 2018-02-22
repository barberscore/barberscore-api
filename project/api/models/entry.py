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
from django.core.exceptions import ValidationError
from django.db import models

# First-Party
from api.tasks import send_entry

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Entry(TimeStampedModel):
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
        (5, 'invited', 'Invited',),
        (7, 'withdrawn', 'Withdrawn',),
        (10, 'submitted', 'Submitted',),
        (20, 'approved', 'Approved',),
        (52, 'scratched', 'Scratched',),
        (55, 'disqualified', 'Disqualified',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    is_archived = models.BooleanField(
        default=False,
    )

    is_evaluation = models.BooleanField(
        help_text="""
            Entry requests evaluation.""",
        default=True,
    )

    is_private = models.BooleanField(
        help_text="""
            Keep scores private.""",
        default=False,
    )

    draw = models.IntegerField(
        help_text="""
            The draw for the initial round only.""",
        null=True,
        blank=True,
    )

    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    directors = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    mos = models.IntegerField(
        help_text='Estimated Participants-on-Stage',
        null=True,
        blank=True,
    )

    representing = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    description = models.TextField(
        help_text="""
            Public Notes (usually from competitor).""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
    )

    # Entry Results
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
    session = models.ForeignKey(
        'Session',
        related_name='entries',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='entries',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        verbose_name_plural = 'entries'
        unique_together = (
            ('group', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "entry"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        if self.is_private and self.contestants.filter(status__gt=0):
            raise ValidationError(
                {'is_private': 'You may not compete for an award and remain private.'}
            )

    def save(self, *args, **kwargs):
        self.nomen = "{0}; {1}".format(
            self.group,
            self.session,
        )
        super().save(*args, **kwargs)

    # Methods

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
            request.user.is_group_manager,
            request.user.is_session_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        result = any([
            # For Judges
            all([
                self.session.convention.assignments.filter(
                    person__user=request.user,
                    category__lt=10,
                    kind=10,
                ),
            ]),
            # For Groups
            all([
                self.group.officers.filter(
                    person__user=request.user,
                    status__gt=0,
                ),
                self.status < self.STATUS.submitted,
            ]),
        ])
        return result

    # Methods

    # Entry Transition Conditions
    def can_invite_entry(self):
        return all([
            self.group.officers.filter(status__gt=0),
            self.group.status == self.group.STATUS.active,
        ])

    def can_submit_entry(self):
        return all([
            any([
                self.group.status == self.group.STATUS.active,
                self.group.status == self.group.STATUS.new,
            ]),
            not all([
                self.is_private,
                self.contestants.filter(status__gt=0).count() > 0,
            ])
        ])

    # Entry Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new],
        target=STATUS.invited,
        conditions=[can_invite_entry],
    )
    def invite(self, *args, **kwargs):
        context = {'entry': self}
        send_entry.delay('entry_invite.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.invited, STATUS.submitted],
        target=STATUS.withdrawn,
        conditions=[],
    )
    def withdraw(self, *args, **kwargs):
        if self.session.status == self.session.STATUS.verified:
            remains = self.session.entries.filter(draw__gt=self.draw)
            self.draw = None
            self.save()
            for entry in remains:
                entry.draw = entry.draw - 1
                entry.save()
        contestants = self.contestants.filter(status__gte=0)
        for contestant in contestants:
            contestant.exclude()
            contestant.save()
        context = {'entry': self}
        send_entry.delay('entry_withdraw.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.invited],
        target=STATUS.submitted,
        conditions=[can_submit_entry],
    )
    def submit(self, *args, **kwargs):
        contestants = self.contestants.filter(
            status__gt=0,
        ).order_by(
            'nomen',
        )
        context = {
            'entry': self,
            'contestants': contestants,
        }
        send_entry.delay('entry_submit.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.submitted, STATUS.withdrawn, STATUS.scratched],
        target=STATUS.approved,
        conditions=[],
    )
    def approve(self, *args, **kwargs):
        repertories = self.group.repertories.order_by('chart__title')
        contestants = self.contestants.filter(
            status__gt=0,
        ).order_by(
            'nomen',
        )
        members = self.group.members.filter(
            status__gt=0,
        ).order_by(
            'person__last_name',
            'person__first_name',
        )
        context = {
            'entry': self,
            'repertories': repertories,
            'contestants': contestants,
            'members': members,
        }
        send_entry.delay('entry_approve.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.approved],
        target=STATUS.scratched,
        conditions=[],
    )
    def scratch(self, *args, **kwargs):
        if self.session.status == self.session.STATUS.verified and self.draw:
            remains = self.session.entries.filter(draw__gt=self.draw)
            self.draw = None
            self.save()
            for entry in remains:
                entry.draw = entry.draw - 1
                entry.save()
        contestants = self.contestants.filter(status__gte=0)
        for contestant in contestants:
            contestant.exclude()
            contestant.save()
        context = {'entry': self}
        send_entry.delay('entry_scratch.txt', context)
        return
