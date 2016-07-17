# Django
from django.contrib import admin

# Local
from .models import (
    Award,
    Certification,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Member,
    Performance,
    Performer,
    Role,
    Round,
    Score,
    Session,
    Song,
    Submission,
)


class AwardInline(admin.TabularInline):
    model = Award
    fields = [
        'name',
        'organization',
        'kind',
        'championship_rounds',
        'size',
        'is_improved',
        'idiom',
    ]
    readonly_fields = [
        'name',
    ]
    extra = 0
    show_change_link = True


class CertificationInline(admin.TabularInline):
    model = Certification
    fields = [
        'name',
        'person',
        'status',
        'category',
    ]
    raw_id_fields = [
        'person',
    ]
    readonly_fields = [
        'name',
    ]
    extra = 0
    show_change_link = True


class ContestInline(admin.TabularInline):
    model = Contest
    fields = [
        'status',
        'award',
        'session',
        'is_qualifier',
    ]
    raw_id_fields = [
        'award',
    ]
    readonly_fields = [
        'name',
        'is_qualifier',
    ]
    ordering = (
        'award__organization__level',
        'award__organization__name',
        'award__kind',
        '-award__is_primary',
        'award__is_improved',
        'award__size',
        'award__scope',
        'award__is_novice',
        'award__idiom',
    )
    show_change_link = True
    extra = 0


class ContestantInline(admin.TabularInline):
    model = Contestant
    fields = [
        'name',
        'status',
    ]
    readonly_fields = [
        'name',
        'performer',
        'status',
    ]
    show_change_link = True
    extra = 0


class ConventionInline(admin.TabularInline):
    model = Convention
    fields = (
        'name',
    )
    ordering = (
        'name',
    )
    readonly_fields = [
        'name',
    ]
    show_change_link = True
    extra = 0


class GroupInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'status',

    ]
    ordering = (
        'name',
    )
    show_change_link = True
    extra = 0


class JudgeInline(admin.TabularInline):
    model = Judge
    fields = [
        'certification',
        'category',
        'kind',
        'session',
        'slot',
    ]
    raw_id_fields = [
        'certification',
    ]
    ordering = (
        'session',
        'kind',
        'category',
    )
    show_change_link = True
    extra = 0


class PerformanceInline(admin.TabularInline):
    model = Performance
    fields = [
        'performer',
        'status',
        'num',
    ]
    readonly_fields = [
        'performer',
    ]
    ordering = (
        'num',
    )
    show_change_link = True
    extra = 0


class MemberInline(admin.TabularInline):
    model = Member
    fields = [
        'chapter',
        'person',
        'status',
    ]
    raw_id_fields = [
        'chapter',
        'person',
    ]
    show_change_link = True
    extra = 0


class PerformerInline(admin.TabularInline):
    model = Performer
    fields = [
        'name',
        'session',
        'prelim',
        'men',
    ]
    raw_id_fields = [
        'group',
    ]
    readonly_fields = [
        'name',
        'total_score',
        'seed',
    ]
    ordering = (
        'group__kind',
        'group',
    )
    show_change_link = True
    extra = 0


class ScoreInline(admin.TabularInline):
    model = Score
    fields = [
        'song',
        'judge',
        'category',
        'points',
    ]
    raw_id_fields = [
        'song',
    ]
    readonly_fields = [
        'song',
        'category',
        'judge',
    ]
    ordering = (
        'judge',
    )
    show_change_link = True
    extra = 0


class SongInline(admin.TabularInline):
    model = Song
    fields = [
        'num',
        'submission',
        'mus_points',
        'prs_points',
        'sng_points',
    ]
    ordering = (
        'num',
    )
    raw_id_fields = [
        'submission',
    ]
    show_change_link = True
    extra = 0
    can_delete = False


class SessionInline(admin.TabularInline):
    model = Session
    fields = [
        'name',
        'status',
        'convention',
        'kind',
    ]
    raw_id_fields = [
        'convention',
    ]
    readonly_fields = [
        'name',
    ]
    show_change_link = True
    extra = 0


class RoleInline(admin.TabularInline):
    model = Role
    fields = [
        'person',
        'part',
        'status',
        'start_date',
        'end_date',
    ]
    raw_id_fields = [
        'person',
    ]
    ordering = (
        'start_date',
    )
    show_change_link = True
    extra = 0


class RoundInline(admin.TabularInline):
    model = Round
    fields = [
        'name',
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
        'name',
    ]
    show_change_link = True
    extra = 0


class SubmissionInline(admin.TabularInline):
    model = Submission
    fields = [
        'title',
        'arranger',
        'source',
        'is_medley',
        'is_parody',
        'performer',
    ]

    show_change_link = True
    extra = 0
