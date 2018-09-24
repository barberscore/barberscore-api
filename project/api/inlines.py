
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
        'legacy_group',
        'status',
        'num',
        'draw',
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
        'status',
        'category',
        'kind',
        'person',
        'convention',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
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
    model = Contest
    fields = [
        'award',
        'group',
        'num',
        'is_primary',
        'session',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        'award',
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class ContestantInline(admin.TabularInline):
    model = Contestant
    fields = [
        'entry',
        'contest',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
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
    autocomplete_fields = [
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
        'status',
        'session',
        'group',
        'tot_score',
        'tot_rank',
        'is_ranked',
    ]
    readonly_fields = [
        'status',
        # 'seed',
    ]
    autocomplete_fields = [
        'session',
        'group',
    ]
    ordering = [
        'group__name',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class EntryInline(admin.TabularInline):
    model = Entry
    fields = [
        'session',
        'group',
        'prelim',
        'draw',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        'session',
        'group',
    ]
    ordering = [
        'group__name',
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
    autocomplete_fields = [
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
        'period',
        'num',
        'onstage',
        'start',
        'round',
        'renditions',
    ]
    autocomplete_fields = [
        'round',
    ]
    show_change_link = True
    extra = 0
    ordering = [
        'period',
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
        'start_date',
        'end_date',
        'status',
    ]
    autocomplete_fields = [
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
    autocomplete_fields = [
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
        'status',
        'category',
        'kind',
        'person',
        'legacy_name',
        'round',
        'num',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
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
    autocomplete_fields = [
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
    ordering = [
        'chart__title',
    ]


class ScoreInline(admin.TabularInline):
    model = Score
    fields = [
        'song',
        'num',
        'panelist__person__common_name',
        'category',
        'kind',
        'points',
    ]
    autocomplete_fields = [
        'song',
    ]
    readonly_fields = [
        'song',
        'category',
        'panelist__person__common_name',
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
    def panelist__person__common_name(self, obj):
        return getattr(getattr(obj.panelist, 'person'), 'common_name', getattr(obj.panelist, 'legacy_name'))


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
        'num_rounds',
    ]
    autocomplete_fields = [
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
        'status',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
