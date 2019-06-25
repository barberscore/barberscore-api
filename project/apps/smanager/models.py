
# Standard Library
import uuid
import datetime

# Third-Party
from django_fsm import FSMIntegerField
from django.core.files.base import ContentFile
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Func
from django.db.models import F

from .fields import FileUploadPath
from .tasks import build_email
from .tasks import send_invite_email_from_entry
from .tasks import send_submit_email_from_entry
from .tasks import send_withdraw_email_from_entry
from .tasks import send_approve_email_from_entry
from .tasks import send_open_email_from_session
from .tasks import send_close_email_from_session
from .tasks import send_verify_email_from_session
from .tasks import send_verify_report_email_from_session
from .tasks import send_package_email_from_session
from .tasks import send_package_report_email_from_session


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    result = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    # Private
    group = models.ForeignKey(
        'bhs.group',
        null=True,
        blank=True,
        related_name='contests',
        on_delete=models.SET_NULL,
        help_text="""The Winner of the Contest.""",
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='contests',
        on_delete=models.CASCADE,
    )

    award = models.ForeignKey(
        'cmanager.award',
        related_name='contests',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='contests',
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'award',)
        )

    class JSONAPIMeta:
        resource_name = "contest"

    def __str__(self):
        return "{0}".format(
            self.award.name,
        )

    def clean(self):
        if self.award.level == self.award.LEVEL.qualifier and self.group:
            raise ValidationError(
                {'level': 'Qualifiers can not select winners'}
            )


    # Contest Permissions
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
            # request.user.is_session_manager,
            # request.user.is_round_manager,
        ])


    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.session.convention.assignments.filter(
                    # person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                # self.session.status < self.session.STATUS.opened,
            ]),
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.excluded], target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.included], target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return


class Contestant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    entry = models.ForeignKey(
        'Entry',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='contestants',
    )

    # Internals
    class Meta:
        ordering = (
            'contest__award__tree_sort',
        )
        unique_together = (
            ('entry', 'contest',),
        )

    class JSONAPIMeta:
        resource_name = "contestant"

    def __str__(self):
        return str(self.id)

    # Methods

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
            # request.user.is_session_manager,
            # request.user.is_round_manager,
            # request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.contest.session.convention.assignments.filter(
                    # person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.contest.session.status < self.contest.session.STATUS.packaged,
            ]),
            all([
                self.entry.group.officers.filter(
                    # person__user=request.user,
                    status__gt=0,
                ),
                self.entry.status < self.entry.STATUS.approved,
            ]),
        ])

    # Contestant Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return


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

    base = models.FloatField(
        help_text="""
            The incoming base score used to determine most-improved winners.""",
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
        'bhs.group',
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
            # request.user.is_session_manager,
            # request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            # For DRCJs
            all([
                self.session.convention.assignments.filter(
                    # person__user=request.user,
                    status__gt=0,
                    category__lt=10,
                ),
                self.session.status < self.session.STATUS.packaged,
            ]),
            # For Groups
            all([
                self.group.officers.filter(
                    # person__user=request.user,
                    status__gt=0,
                ),
                self.status <= self.STATUS.approved,
            ]),
        ])

    # Methods
    def get_invite_email(self):
        template = 'emails/entry_invite.txt'
        context = {'entry': self}
        subject = "[Barberscore] Contest Invitation for {0}".format(
            self.group.name,
        )
        to = self.group.get_officer_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_invite_email(self):
        email = self.get_invite_email()
        return email.send()


    def get_withdraw_email(self):
        # Send confirmation email
        template = 'emails/entry_withdraw.txt'
        context = {'entry': self}
        subject = "[Barberscore] Withdrawl Notification for {0}".format(
            self.group.name,
        )
        to = self.group.get_officer_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_withdraw_email(self):
        email = self.get_withdraw_email()
        return email.send()


    def get_submit_email(self):
        template = 'emails/entry_submit.txt'
        contestants = self.contestants.filter(
            status__gt=0,
        ).order_by('contest__award__name')
        context = {
            'entry': self,
            'contestants': contestants,
        }
        subject = "[Barberscore] Submission Notification for {0}".format(
            self.group.name,
        )
        to = self.group.get_officer_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_submit_email(self):
        email = self.get_submit_email()
        return email.send()


    def get_approve_email(self):
        template = 'emails/entry_approve.txt'
        repertories = self.group.repertories.order_by(
            'chart__title',
        )
        contestants = self.contestants.filter(
            status__gt=0,
        ).order_by(
            'contest__award__name',
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
        subject = "[Barberscore] Approval Notification for {0}".format(
            self.group.name,
        )
        to = self.group.get_officer_emails()
        cc = self.session.convention.get_drcj_emails()
        cc.extend(self.session.convention.get_ca_emails())
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
        )
        return email


    def send_approve_email(self):
        email = self.get_approve_email()
        return email.send()


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

    def can_approve(self):
        if self.is_private and self.contestants.filter(status__gt=0):
            return False
        return True

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
        send_invite_email_from_entry.delay(self)
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
        send_withdraw_email_from_entry.delay(self)
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
        send_submit_email_from_entry.delay(self)
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
        conditions=[
            can_approve,
        ],
    )
    def approve(self, *args, **kwargs):
        send_approve_email_from_entry.delay(self)
        return


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
        'cmanager.convention',
        related_name='sessions',
        on_delete=models.CASCADE,
    )

    target = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='feeders',
        on_delete=models.SET_NULL,
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
    def get_invitees(self):
        Entry = apps.get_model('smanager.entry')
        Panelist = apps.get_model('rmanager.panelist')
        target = self.contests.filter(
            status__gt=0,
            award__children__isnull=False,
        ).distinct().first().award
        feeders = self.feeders.all()
        entries = Entry.objects.filter(
            session__in=feeders,
            contestants__contest__award__parent=target,
            contestants__contest__status__gt=0,
        ).annotate(
            raw_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
            tot_score=Func(
                F('raw_score'),
                function='ROUND',
                template='%(function)s(%(expressions)s, 1)'
            ),
        ).exclude(
            tot_score=None,
        ).order_by(
            '-tot_score',
        )
        return entries


    def get_legacy(self):
        Entry = apps.get_model('smanager.entry')
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
            elif group_type == 'VLQ':
                contestant_id = entry.group.code
            else:
                raise RuntimeError("Improper Entity Type: {0}".format(entry.group.get_kind_display()))
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
        Entry = apps.get_model('smanager.entry')
        Group = apps.get_model('bhs.group')
        Member = apps.get_model('bhs.member')
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
            # expiring_count = 0
            # for member in members:
            #     try:
            #         if member.person.current_through <= self.convention.close_date:
            #             expiring_count += 1
            #     except TypeError:
            #         continue
            expiring_count = "N/A"
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
                phone = member.person.cell_phone.as_national if member.person.cell_phone else None
                member_list.append(
                    phone,
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
                phone = admin.person.cell_phone.as_national if admin.person.cell_phone else None
                contact = "; ".join(filter(None, [
                    admin.person.common_name,
                    admin.person.email,
                    phone,
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


    def get_district_emails(self):
        Officer = apps.get_model('bhs.officer')
        Group = apps.get_model('bhs.group')
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
            "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
            for officer in officers
            if not (
                "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,) in seen or seen.add(
                    "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
                )
            )
        ]
        return result


    def get_participant_emails(self):
        Officer = apps.get_model('bhs.officer')
        Entry = apps.get_model('smanager.entry')
        officers = Officer.objects.filter(
            group__entries__in=self.entries.filter(status=Entry.STATUS.approved),
        ).order_by(
            'group__name',
            'person__last_name',
            'person__first_name',
        )
        seen = set()
        result = [
            "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
            for officer in officers
            if not (
                "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,) in seen or seen.add(
                    "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
                )
            )
        ]
        return result

    def get_open_email(self):
        template = 'emails/session_open.txt'
        context = {'session': self}
        subject = "[Barberscore] {0} Session is OPEN".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_district_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email

    def send_open_email(self):
        email = self.get_open_email()
        return email.send()


    def get_close_email(self):
        template = 'emails/session_close.txt'
        context = {'session': self}
        subject = "[Barberscore] {0} Session is CLOSED".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_district_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email


    def send_close_email(self):
        email = self.get_close_email()
        return email.send()


    def get_verify_email(self):
        template = 'emails/session_verify.txt'
        approved_entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        ).order_by('draw')
        context = {
            'session': self,
            'approved_entries': approved_entries,
        }
        subject = "[Barberscore] {0} Session Draw".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_participant_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email

    def send_verify_email(self):
        email = self.get_verify_email()
        return email.send()


    def get_verify_report_email(self):
        template = 'emails/session_verify_report.txt'
        context = {
            'session': self,
        }
        subject = "[Barberscore] {0} Session Draft Reports".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        attachments = []
        if self.drcj_report:
            xlsx = self.drcj_report.file
        else:
            xlsx = self.get_drcj()
        file_name = '{0} Session DRCJ Report DRAFT.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        if self.legacy_report:
            xlsx = self.legacy_report.file
        else:
            xlsx = self.get_legacy()
        file_name = '{0} Session Legacy Report DRAFT.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            attachments=attachments,
        )
        return email

    def send_verify_report_email(self):
        email = self.get_verify_report_email()
        return email.send()


    def get_package_email(self):
        template = 'emails/session_package.txt'
        approved_entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        ).order_by('draw')
        context = {
            'session': self,
            'approved_entries': approved_entries,
        }
        subject = "[Barberscore] {0} Session Starting".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()
        bcc = self.get_participant_emails()
        context['bcc'] = [x.partition(" <")[0] for x in bcc]
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            bcc=bcc,
        )
        return email

    def send_package_email(self):
        email = self.get_package_email()
        return email.send()


    def get_package_report_email(self):
        template = 'emails/session_package_report.txt'
        context = {
            'session': self,
        }
        subject = "[Barberscore] {0} Session FINAL Reports".format(
            self,
        )
        to = self.convention.get_drcj_emails()
        cc = self.convention.get_ca_emails()

        attachments = []
        if self.drcj_report:
            xlsx = self.drcj_report.file
        else:
            xlsx = self.get_drcj()
        file_name = '{0} Session DRCJ Report FINAL.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        if self.legacy_report:
            xlsx = self.legacy_report.file
        else:
            xlsx = self.get_legacy()
        file_name = '{0} Session Legacy Report FINAL.xlsx'.format(self)
        attachments.append((
            file_name,
            xlsx,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ))
        email = build_email(
            template=template,
            context=context,
            subject=subject,
            to=to,
            cc=cc,
            attachments=attachments,
        )
        return email


    def send_package_report_email(self):
        email = self.get_package_report_email()
        return email.send()


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
            # request.user.is_convention_manager,
            # request.user.is_session_manager,
            # request.user.is_round_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.convention.assignments.filter(
                    # person__user=request.user,
                    status__gt=0,
                    category=self.convention.assignments.model.CATEGORY.drcj,
                ),
                self.status < self.STATUS.finished,
            ]),
        ])

    # Session Conditions
    def can_reset(self):
        if self.status <= self.STATUS.built:
            return True
        return False

    def can_build(self):
        return all([
            self.num_rounds,
        ])

    def can_open(self):
        Contest = apps.get_model('smanager.contest')
        try:
            return all([
                # self.convention.open_date <= datetime.date.today(),
                self.contests.filter(status=Contest.STATUS.included),
            ])
        except TypeError:
            return False

    def can_close(self):
        return True
        Entry = apps.get_model('smanager.entry')
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

    def can_verify(self):
        Entry = apps.get_model('smanager.entry')
        return all([
            self.entries.filter(status=Entry.STATUS.approved).count() > 0,
            not self.entries.filter(
                status=Entry.STATUS.approved,
                draw__isnull=True,
            ),
        ])

    def can_finish(self):
        return all([
            not self.rounds.exclude(status=self.rounds.model.STATUS.published)
        ])

    # Session Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.new,
        conditions=[can_reset]
    )
    def reset(self, *args, **kwargs):
        self.drcj_report.delete()
        contests = self.contests.all()
        rounds = self.rounds.all()
        contests.delete()
        rounds.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        """Build session contests."""

        # Reset for indempotence
        self.reset()

        i = 0
        # Get all the active awards for the convention group
        awards = self.convention.group.awards.filter(
            status=self.convention.group.awards.model.STATUS.active,
            kind=self.kind,
            season=self.convention.season,
            # division__in=self.convention.divisions,
        ).order_by('tree_sort')
        if self.convention.divisions:
            awards = awards.filter(
                division__in=self.convention.divisions,
            ).order_by('tree_sort')
        for award in awards:
            # Create contests for each active award.
            # Could also do some logic here for more precision
            self.contests.create(
                status=self.contests.model.STATUS.included,
                award=award,
            )
        # Create the rounds for the session, along with default # spots
        # for next round.
        for i in range(self.num_rounds):
            num = i + 1
            kind = self.num_rounds - i
            if kind == 3: # Unique to International
                spots = 20
            elif num == 2 and kind != 1: # All Semis
                spots = 10
            else:
                spots = 0
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
            send_open_email_from_session.delay(self)
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
        # Send notification for all public contests only
        if not self.is_invitational:
            send_close_email_from_session.delay(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.closed],
        target=STATUS.verified,
        conditions=[
            can_verify,
        ],
    )
    def verify(self, *args, **kwargs):
        """Make draw public."""
        send_verify_email_from_session.delay(self)
        send_verify_report_email_from_session.delay(self)
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

        #  Create and send the reports
        send_package_email_from_session.delay(self)
        send_package_report_email_from_session.delay(self)
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
