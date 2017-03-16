# Django
from django.contrib import admin

# Local
from .models import (
    Assignment,
    Award,
    Contest,
    Contestant,
    Convention,
    Host,
    Membership,
    Officer,
    Performance,
    Performer,
    Round,
    Score,
    Session,
    Song,
    Submission,
)


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'nomen',
        'status',
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
    extra = 0
    show_change_link = True


class AwardInline(admin.TabularInline):
    model = Award
    fields = [
        'name',
        'kind',
        'championship_rounds',
        'size',
        'is_improved',
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
        'kind',
    ]
    raw_id_fields = [
        'award',
    ]
    readonly_fields = [
        'is_qualifier',
    ]
    ordering = (
        'award__kind',
        '-award__is_primary',
        'award__is_improved',
        'award__size',
        'award__scope',
        'award__is_novice',
    )
    show_change_link = True
    extra = 0


class ContestantInline(admin.TabularInline):
    model = Contestant
    fields = [
        'nomen',
        'status',
    ]
    readonly_fields = [
        'nomen',
        'performer',
        'status',
    ]
    show_change_link = True
    extra = 0


class ConventionInline(admin.TabularInline):
    model = Convention
    fields = (
        'nomen',
    )
    ordering = (
        'nomen',
    )
    readonly_fields = [
        'nomen',
    ]
    show_change_link = True
    extra = 0


class HostInline(admin.TabularInline):
    model = Host
    fields = [
        'session',
        'entity',
        'status',
    ]
    raw_id_fields = [
        'session',
        'entity',
    ]
    show_change_link = True
    extra = 0


class MembershipInline(admin.TabularInline):
    model = Membership
    fields = [
        'person',
        'entity',
        'status',
    ]
    raw_id_fields = [
        'person',
        'entity',
    ]
    ordering = (
        'entity__kind',
        'entity__name',
    )
    show_change_link = True
    extra = 0


class OfficerInline(admin.TabularInline):
    model = Officer
    fields = [
        'office',
        'membership',
    ]
    raw_id_fields = [
        'office',
        'membership',
    ]
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


class PerformerInline(admin.TabularInline):
    model = Performer
    fields = [
        'nomen',
        'session',
        'prelim',
        'men',
    ]
    readonly_fields = [
        'nomen',
        'seed',
    ]
    show_change_link = True
    extra = 0


class ScoreInline(admin.TabularInline):
    model = Score
    fields = [
        'song',
        'person',
        'category',
        'points',
    ]
    raw_id_fields = [
        'song',
    ]
    readonly_fields = [
        'song',
        'category',
        'person',
    ]
    ordering = (
        'person',
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
        'convention',
        'kind',
        'age',
        'num_rounds',
        'participants',
    ]
    raw_id_fields = [
        'convention',
    ]
    show_change_link = True
    extra = 0


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


class SubmissionInline(admin.TabularInline):
    model = Submission
    fields = [
        'title',
        'is_medley',
        'is_parody',
        'performer',
    ]

    show_change_link = True
    extra = 0
