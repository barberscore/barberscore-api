
# Standard Library
import datetime
import logging
import uuid

# Third-Party
import django_rq
import pydf
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import Workbook
from django.utils.text import slugify
# Django
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.template.loader import render_to_string
from cloudinary_storage.storage import RawMediaCloudinaryStorage

from api.tasks import send_open_email_from_session
from api.tasks import send_close_email_from_session
from api.tasks import send_verify_email_from_session
from api.tasks import send_verify_report_email_from_session
from api.tasks import send_package_report_email_from_session
from api.fields import FileUploadPath

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
        (20, 'packaged', 'Packaged',),
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
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of session.  Generally this will be either quartet or chorus.
        """,
        choices=KIND,
    )

    num_rounds = models.IntegerField(
        default=0,
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

    legacy_report = models.FileField(
        upload_to=FileUploadPath(),
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
    )

    drcj_report = models.FileField(
        upload_to=FileUploadPath(),
        blank=True,
        default='',
        storage=RawMediaCloudinaryStorage(),
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='sessions',
    )

    # Properties
    # Internals
    class Meta:
        unique_together = (
            ('convention', 'kind')
        )

    class JSONAPIMeta:
        resource_name = "session"

    def __str__(self):
        return "{0} {1}".format(
            self.convention,
            self.get_kind_display(),
        )

    def clean(self):
        pass

    # Methods
    def get_legacy(self):
        Entry = apps.get_model('api.entry')
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'oa',
            'contestant_id',
            'group_name',
            'group_type',
            'song_number',
            'song_title',
        ]
        ws.append(fieldnames)
        entries = self.entries.filter(
            status__in=[
                Entry.STATUS.approved,
            ]
        ).order_by('draw')
        for entry in entries:
            oa = entry.draw
            group_name = entry.group.name.encode('utf-8').strip()
            group_type = entry.group.get_kind_display()
            if group_type == 'Quartet':
                contestant_id = entry.group.bhs_id
            elif group_type == 'Chorus':
                contestant_id = entry.group.code
            else:
                raise RuntimeError("Improper Entity Type")
            i = 1
            for repertory in entry.group.repertories.order_by('chart__title'):
                song_number = i
                song_title = repertory.chart.title.encode('utf-8').strip()
                i += 1
                row = [
                    oa,
                    contestant_id,
                    group_name,
                    group_type,
                    song_number,
                    song_title,
                ]
                ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    def save_legacy(self):
        content = self.get_legacy()
        self.legacy_report.save("legacy_report", content)


    def get_drcj(self):
        Entry = apps.get_model('api.entry')
        Group = apps.get_model('api.group')
        Member = apps.get_model('api.member')
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'OA',
            'Group Name',
            'Representing',
            'Evaluation?',
            'Score/Eval-Only?',
            'BHS ID',
            'Group Status',
            'Repertory Count',
            'Estimated MOS',
            'Members Expiring',
            'Tenor',
            'Lead',
            'Baritone',
            'Bass',
            'Director/Participant(s)',
            'Award(s)',
            'Chapter(s)',
            'Contacts(s)',
        ]
        ws.append(fieldnames)
        entries = self.entries.filter(
            status__in=[
                Entry.STATUS.approved,
            ]
        ).order_by('draw')
        for entry in entries:
            oa = entry.draw
            group_name = entry.group.name
            representing = entry.representing
            evaluation = entry.is_evaluation
            is_private = entry.is_private
            bhs_id = entry.group.bhs_id
            repertory_count = entry.group.repertories.filter(
                status__gt=0,
            ).count()
            group_status = entry.group.get_status_display()
            repertory_count = entry.group.repertories.filter(
                status__gt=0,
            ).count()
            participant_count = entry.pos
            members = entry.group.members.filter(
                status__gt=0,
            )
            expiring_count = 0
            for member in members:
                try:
                    if member.person.current_through <= self.convention.close_date:
                        expiring_count += 1
                except TypeError:
                    continue
            participants = entry.participants
            awards_list = []
            contestants = entry.contestants.filter(
                status__gt=0,
            ).order_by('contest__award__name')
            for contestant in contestants:
                awards_list.append(contestant.contest.award.name)
            awards = "\n".join(filter(None, awards_list))
            parts = {}
            part = 1
            while part <= 4:
                try:
                    member = members.get(
                        part=part,
                    )
                except Member.DoesNotExist:
                    parts[part] = None
                    part += 1
                    continue
                except Member.MultipleObjectsReturned:
                    parts[part] = None
                    part += 1
                    continue
                member_list = []
                member_list.append(
                    member.person.nomen,
                )
                member_list.append(
                    member.person.email,
                )
                member_list.append(
                    member.person.phone,
                )
                member_detail = "\n".join(filter(None, member_list))
                parts[part] = member_detail
                part += 1
            if entry.group.kind == entry.group.KIND.quartet:
                persons = members.values_list('person', flat=True)
                cs = Group.objects.filter(
                    members__person__in=persons,
                    members__status__gt=0,
                    kind=Group.KIND.chapter,
                ).distinct(
                ).order_by(
                    'name',
                ).values_list(
                    'name',
                    flat=True
                )
                chapters = "\n".join(cs)
            elif entry.group.kind == entry.group.KIND.chorus:
                try:
                    chapters = entry.group.parent.name
                except AttributeError:
                    chapters = None
            admins = entry.group.officers.filter(
                status__gt=0,
            )
            admins_list = []
            for admin in admins:
                contact = "; ".join(filter(None, [
                    admin.person.common_name,
                    admin.person.email,
                    admin.person.cell_phone,
                ]))
                admins_list.append(contact)
            contacts = "\n".join(filter(None, admins_list))
            row = [
                oa,
                group_name,
                representing,
                evaluation,
                is_private,
                bhs_id,
                group_status,
                repertory_count,
                participant_count,
                expiring_count,
                parts[1],
                parts[2],
                parts[3],
                parts[4],
                participants,
                awards,
                chapters,
                contacts,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    def save_drcj(self):
        content = self.get_drcj()
        self.drcj_report.save("drcj_report", content)


    def get_officer_emails(self):
        Officer = apps.get_model('api.officer')
        Group = apps.get_model('api.group')
        officers = Officer.objects.filter(
            status=Officer.STATUS.active,
            group__status=Group.STATUS.active,
            person__email__isnull=False,
        )
        if self.kind == self.KIND.quartet:
            officers = officers.filter(
                group__parent=self.convention.group,
                group__kind=self.KIND.quartet,
            )
        else:
            officers = officers.filter(
                group__parent__parent=self.convention.group,
            ).exclude(
                group__kind=self.KIND.quartet,
            )
        if self.convention.divisions:
            officers = officers.filter(
                group__division__in=self.convention.divisions,
            )
        officers = officers.order_by(
            'group__name',
            'person__last_name',
            'person__first_name',
        )
        # Remove duplicates whilst preserving order.
        # http://www.martinbroadhurst.com/removing-duplicates-from-a-list-while-preserving-order-in-python.html
        seen = set()
        result = [
            "{0} ({2}) <{1}>".format(officer.person.common_name, officer.person.email, officer.group.name)
            for officer in officers
            if not (
                "{0} ({2}) <{1}>".format(officer.person.common_name, officer.person.email, officer.group.name) in seen or seen.add(
                "{0} ({2}) <{1}>".format(officer.person.common_name, officer.person.email, officer.group.name)
                )
            )
        ]
        return result


    def queue_open_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_open_email_from_session,
            self,
        )

    def queue_close_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_close_email_from_session,
            self,
        )

    def queue_verify_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_verify_email_from_session,
            self,
        )

    def queue_verify_report_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_verify_report_email_from_session,
            self,
        )

    def queue_package_report_email(self):
        queue = django_rq.get_queue('high')
        return queue.enqueue(
            send_package_report_email_from_session,
            self,
        )

    # Session Permissions
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
            # request.user.is_round_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category=self.convention.assignments.model.CATEGORY.drcj,
                ),
                self.status < self.STATUS.finished,
            ]),
        ])

    # Session Conditions
    def can_build(self):
        return all([
            self.num_rounds,
        ])

    def can_open(self):
        Contest = apps.get_model('api.contest')
        return all([
            self.convention.open_date <= datetime.date.today(),
            self.contests.filter(status=Contest.STATUS.included),
        ])

    def can_close(self):
        return True
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

    def can_finish(self):
        # Session Transitions
        return all([
            not self.rounds.exclude(status=self.rounds.model.STATUS.finished)
        ])

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        """Build session contests."""
        i = 0
        # Get all the active awards for the convention group
        awards = self.convention.group.awards.filter(
            status=self.convention.group.awards.model.STATUS.active,
            kind=self.kind,
            season=self.convention.season,
        ).order_by('tree_sort')
        for award in awards:
            # Create contests for each active award.
            # Could also do some logic here for more precision
            self.contests.create(
                status=self.contests.model.STATUS.included,
                award=award,
            )
        # Create the rounds for the session, along with default # spots
        for i in range(self.num_rounds):
            num = i + 1
            kind = self.num_rounds - i
            if num == 1:
                spots = 10
            elif num == 2 and kind !=1:
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
        conditions=[can_open],
    )
    def open(self, *args, **kwargs):
        """Make session available for entry."""
        # Send notification for all public contests
        if not self.is_invitational:
            self.queue_open_email()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.opened,
        target=STATUS.closed,
        conditions=[can_close]
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
        # Notify for all public contests
        self.queue_close_email()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.closed],
        target=STATUS.verified,
        conditions=[],
    )
    def verify(self, *args, **kwargs):
        """Make draw public."""
        self.queue_verify_email()
        self.queue_verify_report_email()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.verified,
        target=STATUS.packaged,
        conditions=[],
    )
    def package(self, *args, **kwargs):
        """Button up session and transfer to CA."""

        # Save final reports
        self.save_drcj()
        self.save_legacy()
        self.save_contact()

        #  Create and send the reports
        self.queue_package_report_email()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.packaged, STATUS.finished],
        target=STATUS.finished,
        conditions=[can_finish],
    )
    def finish(self, *args, **kwargs):
        return
