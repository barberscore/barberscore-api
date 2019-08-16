# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

# Django
from django.contrib import admin
from reversion.admin import VersionAdmin

# Local
# from .filters import ConventionStatusListFilter
# from .filters import SessionConventionStatusListFilter
# from .filters import ActiveConventionListFilter
# from .inlines import ConventionInline
from .inlines import ContestInline
from .inlines import EntryInline

from .models import Assignment
from .models import Contest
from .models import Entry
from .models import Session
from .models import Repertory



admin.site.site_header = 'Barberscore Admin Backend'



@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'kind',
        'session',
        'person_id',
        'category',
    ]

    list_display = [
        'name',
        'bhs_id',
        'session',
        'category',
        'kind',
    ]

    list_filter = (
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
class ContestAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'award_id',
        'name',
        'level',
        'kind',
        'age',
        'description',
        'district',
        'division',
        'gender',
        'is_single',
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
        # 'award__kind',
    ]

    save_on_top = True

    inlines = [
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
class EntryAdmin(VersionAdmin, FSMTransitionMixin):
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
        # 'group_charts',
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
        'kind',
        'district',
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
        'name',
        # 'session__convention__season',
        # 'session__convention__district',
        # 'session__convention__name',
        'session',
    ]


@admin.register(Repertory)
class RepertoryAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'title',
        'arrangers',
        'chart_id'
    ]

    list_display = [
        'id',
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
    ]

    search_fields = [
        # 'group__name',
        # 'chart__title',
        'title',
    ]


@admin.register(Session)
class SessionAdmin(VersionAdmin, FSMTransitionMixin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = [
        'id',
        'status',
        'name',
        'district',
        'kind',
        'convention_id',
        ('num_rounds', 'is_invitational',),
        'target',
        'legacy_report',
        'drcj_report',
        'owners',
        'group_emails',
        # 'contests',
        # 'footnotes',
        'description',
        'notes',

        # 'name',
        # 'representing',
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
        'district',
        'name',
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
        'season',
        'district',
        'year',
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
