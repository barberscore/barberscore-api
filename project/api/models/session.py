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

# Django
from django.apps import apps as api_apps
from django.db import models
from django.utils.text import slugify

# First-Party
# from api.tasks import create_admins_report
# from api.tasks import create_bbscores_report
# from api.tasks import create_drcj_report
# from api.tasks import create_oss_report
# from api.tasks import create_sa_report
from api.tasks import send_session
from api.tasks import send_session_reports


config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


def upload_to_bbscores(instance, filename):
    return 'session/{0}/{1}-bbscores_report.xlsx'.format(
        instance.id,
        slugify(instance.nomen)
    )


def upload_to_drcj(instance, filename):
    return 'session/{0}/{1}-drcj_report.xlsx'.format(
        instance.id,
        slugify(instance.nomen)
    )


def upload_to_admins(instance, filename):
    return 'session/{0}/{1}-admins_report.xlsx'.format(
        instance.id,
        slugify(instance.nomen)
    )


def upload_to_oss(instance, filename):
    return 'session/{0}/{1}-oss_report.pdf'.format(
        instance.id,
        slugify(instance.nomen)
    )


def upload_to_sa(instance, filename):
    return 'session/{0}/{1}-sa_report.pdf'.format(
        instance.id,
        slugify(instance.nomen)
    )


class Session(TimeStampedModel):
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

    bbscores_report = models.FileField(
        upload_to=upload_to_bbscores,
        blank=True,
        max_length=255,
    )

    drcj_report = models.FileField(
        upload_to=upload_to_drcj,
        blank=True,
        max_length=255,
    )

    admins_report = models.FileField(
        upload_to=upload_to_admins,
        blank=True,
        max_length=255,
    )

    oss_report = models.FileField(
        upload_to=upload_to_oss,
        blank=True,
        max_length=255,
    )

    sa_report = models.FileField(
        upload_to=upload_to_sa,
        blank=True,
        max_length=255,
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
        on_delete=models.CASCADE,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "session"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        gender = self.gender
        if gender == self.GENDER.male:
            gender = None
        else:
            gender = self.get_gender_display()
        self.nomen = " ".join(
            filter(None, [
                str(self.convention),
                gender,
                self.get_kind_display(),
                'Session',
            ])
        )
        super().save(*args, **kwargs)

    # Methods

    # Session Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
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
            request.user.is_session_manager,
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
        Contest = config.get_model('Contest')
        return all([
            self.contests.filter(status=Contest.STATUS.included),
        ])

    def can_close_session(self):
        Entry = config.get_model('Entry')
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
        grantors = self.convention.grantors.all()
        for grantor in grantors:
            awards = grantor.group.awards.filter(
                status=grantor.group.awards.model.STATUS.active,
                kind=self.kind,
                season=self.convention.season,
            )
            for award in awards:
                # Could also do some logic here for more precision
                self.contests.create(
                    status=self.contests.model.STATUS.included,
                    award=award,
                )
        for i in range(self.num_rounds):
            num = i + 1
            kind = self.num_rounds - i
            self.rounds.create(
                num=num,
                kind=kind,
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
        # bbscores_report = create_bbscores_report(self)
        # drcj_report = create_drcj_report(self)
        # admins_report = create_admins_report(self)
        context = {
            'session': self,
            # 'bbscores_report': bbscores_report,
            # 'drcj_report': drcj_report,
            # 'admins_report': admins_report,
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
        }
        send_session_reports.delay('session_reports.txt', context)
        # Get models for constants
        Entry = config.get_model('Entry')
        # delete orphans
        for entry in self.entries.filter(status=Entry.STATUS.new):
            entry.delete()
        # notify entrants
        context = {'session': self}
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
