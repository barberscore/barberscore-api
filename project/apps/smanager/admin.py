# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

# Django
from django.contrib import admin

# Local
# from .filters import ConventionStatusListFilter
# from .filters import SessionConventionStatusListFilter
# from .filters import ActiveConventionListFilter
from .inlines import AssignmentInline
# from .inlines import ConventionInline
from .inlines import ContestInline
from .inlines import EntryInline
from .inlines import SessionInline

from .models import Assignment
from .models import Contest
from .models import Entry
from .models import Session
from .models import Repertory
from reversion.admin import VersionAdmin

from .inlines import RepertoryInline

# from api.inlines import RoundInline

admin.site.site_header = 'Barberscore Admin Backend'



@admin.register(Assignment)
class AssignmentAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = [
        'status',
        'kind',
        'session',
        'person_id',
        # 'user',
        'category',
    ]

    list_display = [
        'name',
        'bhs_id',
        'session',
        'category',
        'kind',
        'status',
    ]

    list_filter = (
        'status',
        'kind',
        'category',
        # ActiveConventionListFilter,
    )

    list_select_related = [
        'session',
    ]

    search_fields = [
        'id',
    ]

    autocomplete_fields = [
        'session',
    ]

    readonly_fields = [
    ]
    inlines = [
        StateLogInline,
    ]
    raw_id_fields = [
        # 'user',
    ]
    ordering = [
        'session',
        'kind',
        'last_name',
        'first_name',
    ]


@admin.register(Contest)
class ContestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'award_id',
        'name',
        'level',
        'kind',
        'age',
        'description',
        'district',
        'division',
        'gender',
        'is_novice',
        'scope',
        'scope_range',
        'season',
        'size',
        'size_range',
        'tree_sort',
        'session',

    ]

    list_display = (
        'name',
        # 'convention_name',
        'session',
        # 'group',
    )

    list_filter = [
        'status',
        # 'award__kind',
    ]

    save_on_top = True

    inlines = [
    ]

    fsm_field = [
        'status',
    ]

    readonly_fields = [
        'id',
        'tree_sort',
        # 'convention_name',
    ]

    autocomplete_fields = [
        # 'award',
        'session',
        # 'group',
    ]

    search_fields = [
        'name',
        'district',
    ]
    ordering = [
        # '-session__convention__year',
        # 'session__convention__season',
        # 'session__convention__district',
        # 'session__convention__name',
        'session',
        'name',
    ]


@admin.register(Entry)
class EntryAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = (
        'id',
        'status',
        'session',
        'representing',
        'chapters',
        ('is_evaluation', 'is_private', 'is_mt'),
        'draw',
        'base',
        'prelim',
        'seed',
        'image',
        'participants',
        'description',
        'notes',
        'owners',
        'contests',
        'group_charts',
    )

    list_display = (
        '__str__',
        # 'convention_name',
        'session',
        'status',
        # 'group',
    )

    list_select_related = [
        'session',
    ]

    list_filter = [
        # SessionConventionStatusListFilter,
        'status',
        'session',
        # 'session__convention__season',
        # 'session__convention__year',
    ]

    inlines = [
        # AppearanceInline,
        StateLogInline,
    ]

    search_fields = [
        'id',
        # 'session__convention__name',
        # 'group__name',
    ]

    autocomplete_fields = [
        'session',
        'contests',
        'owners',
    ]
    readonly_fields = (
        'id',
        # 'convention_name',
    )

    save_on_top = True

    ordering = [
        # '-session__convention__year',
        # 'session__convention__season',
        # 'session__convention__district',
        # 'session__convention__name',
        'session',
    ]


@admin.register(Repertory)
class RepertoryAdmin(VersionAdmin, FSMTransitionMixin):
    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'status',
        'title',
        'arrangers',
        'chart_id'
    ]

    list_display = [
        'id',
        'status',
        'title',
        'arrangers',
        'chart_id'
    ]

    save_on_top = True

    readonly_fields = [
        'id',
    ]

    autocomplete_fields = [
        # 'entry',
        # 'title',
        # 'chart',
    ]

    inlines = [
        StateLogInline,
    ]

    search_fields = [
        # 'group__name',
        # 'chart__title',
        'title',
    ]



@admin.register(Session)
class SessionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = [
        'id',
        'status',
        # 'convention',
        'kind',
        'convention_id',
        ('num_rounds', 'is_invitational',),
        'target',
        'legacy_report',
        'drcj_report',
        'owners',
        # 'contests',
        # 'footnotes',
        'description',
        'notes',

        'name',
        'representing',
        'divisions',
        ('year', 'season', ),
        'panel',
        ('open_date', 'close_date', ),
        ('start_date', 'end_date', ),
        'venue_name',
        'location',
        'timezone',
        'image',



    ]

    list_display = [
        'id',
        # 'convention',
        # 'convention__district',
        'kind',
        'num_rounds',
        'is_invitational',
        'status',
    ]

    list_filter = (
        # ConventionStatusListFilter,
        'status',
        'kind',
        'num_rounds',
        'is_invitational',
        # 'convention__season',
        # 'convention__district',
        # 'convention__year',
    )

    autocomplete_fields = [
        # 'convention',
        'target',
        'owners',
    ]

    readonly_fields = [
        'id',
        'legacy_report',
        'drcj_report',
    ]

    inlines = [
        # RoundInline,
        ContestInline,
        EntryInline,
        StateLogInline,
    ]

    list_select_related = [
        # 'convention',
    ]

    ordering = (
        # '-convention__year',
        # 'convention__season',
        # 'convention__group__tree_sort',
        'kind',
    )
    ordering = [
        # '-convention__year',
        # 'convention__season',
        # 'convention__district',
        # 'convention__name',
        'kind',
    ]

    search_fields = [
        # 'convention__name',
        'kind',
    ]

    # raw_id_fields = [
    #     'owners',
    # ]
