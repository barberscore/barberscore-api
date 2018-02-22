# Django
from django.contrib import admin

# Local
from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Competitor
from .models import Contest
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grantor
from .models import Grid
from .models import Group
from .models import Member
from .models import Officer
from .models import Panelist
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song


class ActiveChapterInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'parent',
        'code',
        # 'kind',
        'gender',
        # 'bhs_id',
        # 'status',
    ]
    fk_name = 'parent'
    ordering = [
        'nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    verbose_name_plural = 'Active Chapters'

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries."""
        qs = super().get_queryset(request)
        qs = qs.filter(
            status__gt=0,
            kind=Group.KIND.chapter,
        )
        return qs


class ActiveChorusInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'parent',
        'bhs_id',
        # 'code',
        # 'kind',
        'gender',
        # 'status',
    ]
    fk_name = 'parent'
    ordering = [
        'nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    verbose_name_plural = 'Active Choruses'
    readonly_fields = [
        'status',
    ]

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries."""
        qs = super().get_queryset(request)
        qs = qs.filter(
            status__gt=0,
            kind=Group.KIND.chorus,
        )
        return qs


class ActiveQuartetInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'parent',
        'bhs_id',
        'is_senior',
        'gender',
        # 'status',
    ]
    fk_name = 'parent'
    ordering = [
        'nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    verbose_name_plural = 'Active Quartets'
    readonly_fields = [
        'status',
    ]

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries."""
        qs = super().get_queryset(request)
        qs = qs.filter(
            status__gt=0,
            kind=Group.KIND.quartet,
        )
        return qs


class AppearanceInline(admin.TabularInline):
    model = Appearance
    fields = [
        'competitor',
        'status',
        'num',
        'tot_points',
    ]
    readonly_fields = [
        'competitor',
        'status',
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
        'status',
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
        'gender',
        'rounds',
        'size',
        'is_improved',
        'group',
    ]
    readonly_fields = [
        'name',
        'status',
    ]
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]


class ContestInline(admin.TabularInline):
    def primary(self, obj):
        return obj.award.is_primary

    model = Contest
    fields = [
        'status',
        'award',
        'primary',
        'session',
    ]
    readonly_fields = [
        'primary',
        'status',
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
        'entry',
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
        'group',
    ]
    raw_id_fields = [
        'group',
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
        'status',
        'session',
        'group',
        'tot_score',
        'draw',
    ]
    readonly_fields = [
        'nomen',
        'status',
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
        'status',
    ]
    raw_id_fields = [
        'session',
        'group',
    ]
    ordering = [
        'group__nomen',
        'session__convention__year',
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
        'group',
    ]
    raw_id_fields = [
        'convention',
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class GridInline(admin.TabularInline):
    model = Grid
    fields = [
        'num',
        'onstage',
        'start',
        'round',
        'competitor',
        'renditions',
    ]
    raw_id_fields = [
        'round',
        'competitor',
    ]
    show_change_link = True
    extra = 0
    ordering = [
        'num',
    ]
    classes = [
        'collapse',
    ]


class GroupInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'parent',
        'kind',
        'gender',
        'bhs_id',
        'status',
    ]
    fk_name = 'parent'
    ordering = [
        'nomen',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    readonly_fields = [
        'status',
    ]


class MemberInline(admin.TabularInline):
    model = Member
    fields = [
        'person',
        'group',
        'part',
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
    readonly_fields = [
        'status',
    ]

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
        'group',
        'status',
    ]
    raw_id_fields = [
        'office',
        'person',
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    ordering = [
        'person__last_name',
        'person__first_name',
    ]
    readonly_fields = [
        'status',
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
        'status',
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
    readonly_fields = [
        'status',
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
        'status',
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
    readonly_fields = [
        'status',
    ]


class SessionInline(admin.TabularInline):
    model = Session
    fields = [
        'convention',
        'kind',
        'gender',
        'num_rounds',
    ]
    raw_id_fields = [
        'convention',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    readonly_fields = [
        'status',
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
        'status',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
