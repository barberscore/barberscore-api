
# Standard Library
import logging
import uuid
import django_rq

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Django
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models

from api.tasks import send_invite_email_from_entry
from api.tasks import send_submit_email_from_entry
from api.tasks import send_approve_email_from_entry
from api.tasks import send_withdraw_email_from_entry

log = logging.getLogger(__name__)


class Entry(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'built', 'Built',),
        (5, 'invited', 'Invited',),
        (7, 'withdrawn', 'Withdrawn',),
        (10, 'submitted', 'Submitted',),
        (20, 'approved', 'Approved',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
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

    is_mt = models.BooleanField(
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

    participants = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    pos = models.IntegerField(
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
            Public Notes (usually from group).""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
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

    statelogs = GenericRelation(
        StateLog,
        related_query_name='entries',
    )

    # Properties

    # Internals
    class Meta:
        verbose_name_plural = 'entries'
        unique_together = (
            ('group', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "entry"

    def __str__(self):
        return str(self.id)

    def clean(self):
        if self.is_private and self.contestants.filter(status__gt=0):
            raise ValidationError(
                {'is_private': 'You may not compete for an award and remain private.'}
            )
        # if self.session.status >= self.session.STATUS.packaged:
        #     raise ValidationError(
        #         {'session': 'You may not add entries after the Session has started.'}
        #     )


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
            request.user.is_session_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            # For DRCJs
            all([
                self.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lt=10,
                ),
                self.session.status < self.session.STATUS.packaged,
            ]),
            # For Groups
            all([
                self.group.officers.filter(
                    person__user=request.user,
                    status__gt=0,
                ),
                self.status < self.STATUS.approved,
            ]),
        ])

    # Methods
    def queue_invite_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_invite_email_from_entry,
            self,
        )

    def queue_withdraw_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_withdraw_email_from_entry,
            self,
        )

    def queue_submit_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_submit_email_from_entry,
            self,
        )

    def queue_approve_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_approve_email_from_entry,
            self,
        )

    # Entry Transition Conditions
    def can_build_entry(self):
        return True

    def can_invite_entry(self):
        return all([
            self.group.officers.filter(status__gt=0),
            self.group.status == self.group.STATUS.active,
        ])

    def can_submit_entry(self):
        # Instantiate list
        checklist = []

        # Only active groups can submit.
        checklist.append(bool(self.group.STATUS.active))

        # check to ensure all fields are entered
        if self.group.kind == self.group.KIND.chorus:
            checklist.append(
                all([
                    self.pos,
                    self.participants
                ])
            )
        # ensure they can't submit a private while competiting.
        checklist.append(
            not all([
                self.is_private,
                self.contestants.filter(status__gt=0).count() > 0,
            ]),
        )
        return all(checklist)

    # Entry Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new],
        target=STATUS.built,
        conditions=[can_build_entry],
    )
    def build(self, *args, **kwargs):
        contests = self.session.contests.filter(
            status=self.session.contests.model.STATUS.included,
        )
        for contest in contests:
            # Could also do some default logic here.
            self.contestants.create(
                status=self.contestants.model.STATUS.excluded,
                contest=contest,
            )
        self.representing = self.group.district
        self.participants = self.group.participants
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
        ],
        target=STATUS.invited,
        conditions=[can_invite_entry],
    )
    def invite(self, *args, **kwargs):
        """Invites the group to enter"""
        self.queue_invite_email()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
            STATUS.invited,
            STATUS.submitted,
            STATUS.approved,
        ],
        target=STATUS.withdrawn,
        conditions=[],
    )
    def withdraw(self, *args, **kwargs):
        """Withdraws the Entry from the Session"""
        # If the session has been drawn, re-index.
        if self.draw:
            remains = self.session.entries.filter(draw__gt=self.draw)
            self.draw = None
            self.save()
            for entry in remains:
                entry.draw = entry.draw - 1
                entry.save()
        # Remove from all contestants
        contestants = self.contestants.filter(status__gte=0)
        for contestant in contestants:
            contestant.exclude()
            contestant.save()
        # Queue email
        self.queue_withdraw_email()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
            STATUS.invited,
            STATUS.submitted
        ],
        target=STATUS.submitted,
        conditions=[can_submit_entry],
    )
    def submit(self, *args, **kwargs):
        self.queue_submit_email()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.built,
            STATUS.submitted,
            STATUS.withdrawn,
            STATUS.approved,
        ],
        target=STATUS.approved,
        conditions=[],
    )
    def approve(self, *args, **kwargs):
        self.queue_approve_email()
        return
