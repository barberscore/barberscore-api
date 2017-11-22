# Django
from django.contrib import admin

# Local
from .models import (
    Appearance,
    Assignment,
    Award,
    Contest,
    Contestant,
    Convention,
    Competitor,
    Enrollment,
    Entry,
    Grantor,
    Group,
    Member,
    Officer,
    Panelist,
    Participant,
    Repertory,
    Round,
    Score,
    Session,
    Slot,
    Song,
)


class AppearanceInline(admin.TabularInline):
    model = Appearance
    fields = [
        'entry',
        'status',
        'num',
        'draw',
    ]
    readonly_fields = [
        'entry',
    ]
    ordering = (
        'num',
    )
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'nomen',
        'status',
        'category',
        'kind',
        'person',
        'convention',
    ]
    readonly_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'person',
        'convention',
    ]
    ordering = (
        'category',
        'kind',
        'person__last_name',
        'person__first_name',
    )
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]


class AwardInline(admin.TabularInline):
    model = Award
    fields = [
        'name',
        'kind',
        'rounds',
        'size',
        'is_improved',
        'organization',
    ]
    readonly_fields = [
        'name',
    ]
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]


class ContestInline(admin.TabularInline):
    model = Contest
    fields = [
        'status',
        'award',
        'session',
    ]
    raw_id_fields = [
        'award',
    ]
    ordering = (
        '-award__is_primary',
        'award__is_improved',
        'award__size',
        'award__scope',
    )
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class ContestantInline(admin.TabularInline):
    model = Contestant
    fields = [
        'nomen',
        'entry',
        'contest',
        'status',
    ]
    readonly_fields = [
        'nomen',
        'status',
    ]
    raw_id_fields = [
        'contest',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class ConventionInline(admin.TabularInline):
    model = Convention
    fields = [
        'name',
        'organization',
    ]
    raw_id_fields = [
        'organization',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class CompetitorInline(admin.TabularInline):
    model = Competitor
    fields = [
        'nomen',
        'session',
        'group',
        'tot_score',
    ]
    readonly_fields = [
        'nomen',
        # 'seed',
    ]
    raw_id_fields = [
        'session',
        'group',
    ]
    ordering = [
        'group__nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    fields = [
        'person',
        'organization',
        'status',
    ]
    raw_id_fields = [
        'person',
        'organization',
    ]
    ordering = (
        'person__last_name',
        'person__first_name',
    )
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class EntryInline(admin.TabularInline):
    model = Entry
    fields = [
        'nomen',
        'session',
        'group',
        'prelim',
        'draw',
        'status',
    ]
    readonly_fields = [
        'nomen',
        # 'seed',
    ]
    raw_id_fields = [
        'session',
        'group',
    ]
    ordering = [
        'group__nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class GrantorInline(admin.TabularInline):
    model = Grantor
    fields = [
        'convention',
        'organization',
    ]
    raw_id_fields = [
        'convention',
        'organization',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class GroupInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'organization',
        'kind',
        'bhs_id',
        'status',
    ]
    fk_name = 'organization'
    ordering = [
        'nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class MemberInline(admin.TabularInline):
    model = Member
    fields = [
        'person',
        'group',
        'part',
        'is_admin',
        'status',
    ]
    raw_id_fields = [
        'person',
        'group',
    ]
    ordering = (
        '-status',
        'part',
        'person__last_name',
        'person__first_name',
    )
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class OfficerInline(admin.TabularInline):
    model = Officer
    fields = [
        'office',
        'person',
        'organization',
        'status',
    ]
    raw_id_fields = [
        'office',
        'person',
        'organization',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class PanelistInline(admin.TabularInline):
    model = Panelist
    fields = [
        'nomen',
        'status',
        'category',
        'kind',
        'person',
        'round',
        'num',
    ]
    readonly_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'person',
        'round',
    ]
    ordering = (
        'category',
        'kind',
        'person__last_name',
        'person__first_name',
    )
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]


class ParticipantInline(admin.TabularInline):
    model = Participant
    fields = [
        'person',
        'entry',
        'status',
        'part',
    ]
    raw_id_fields = [
        'person',
        'entry',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class RepertoryInline(admin.TabularInline):
    model = Repertory
    fields = [
        'chart',
        'group',
        'status',
    ]
    raw_id_fields = [
        'chart',
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class ScoreInline(admin.TabularInline):
    model = Score
    fields = [
        'song',
        'num',
        'panelist',
        'category',
        'kind',
        'points',
    ]
    raw_id_fields = [
        'song',
    ]
    readonly_fields = [
        'song',
        'category',
        'panelist',
    ]
    ordering = (
        'num',
        'panelist',
    )
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class SongInline(admin.TabularInline):
    model = Song
    fields = [
        'num',
    ]
    ordering = (
        'num',
    )
    show_change_link = True
    extra = 0
    can_delete = False
    classes = [
        'collapse',
    ]


class SessionInline(admin.TabularInline):
    model = Session
    fields = [
        'convention',
        'kind',
    ]
    raw_id_fields = [
        'convention',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class SlotInline(admin.TabularInline):
    model = Slot
    fields = [
        'num',
        'onstage',
        'round',
    ]
    raw_id_fields = [
        'round',
    ]
    show_change_link = True
    extra = 0
    ordering = [
        'num',
    ]
    classes = [
        'collapse',
    ]


class RoundInline(admin.TabularInline):
    model = Round
    fields = [
        'nomen',
        'session',
        'kind',
        'status',
        'num',
    ]
    ordering = (
        'session',
        'kind',
    )
    readonly_fields = [
        'nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
