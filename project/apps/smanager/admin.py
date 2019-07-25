# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

# Django
from django.contrib import admin

# Local
from .filters import ConventionStatusListFilter
from .filters import SessionConventionStatusListFilter
from .filters import ActiveConventionListFilter
from .inlines import AssignmentInline
# from .inlines import ConventionInline
from .inlines import ContestInline
from .inlines import EntryInline
from .inlines import SessionInline

from .models import Assignment
from .models import Convention
from .models import Contest
from .models import Entry
from .models import Session

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
        'convention',
        'person_id',
        'user',
        'category',
    ]

    list_display = [
        'common_name',
        'bhs_id',
        'convention',
        'category',
        'kind',
        'status',
    ]

    list_filter = (
        'status',
        'kind',
        'category',
        ActiveConventionListFilter,
    )

    list_select_related = [
        'convention',
    ]

    search_fields = [
        'id',
    ]

    autocomplete_fields = [
        'convention',
    ]

    readonly_fields = [
    ]
    inlines = [
        StateLogInline,
    ]
    raw_id_fields = [
        'user',
    ]
    ordering = [
        '-convention__start_date',
        'category',
        'kind',
        'last_name',
        'first_name',
    ]


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = (
        'id',
        # 'legacy_selection',
        # 'legacy_complete',
        'status',
        'name',
        ('group_id', 'divisions', ),
        ('year', 'season', ),
        ('panel', 'kinds', ),
        ('open_date', 'close_date', ),
        ('start_date', 'end_date', ),
        'owners',
        'venue_name',
        'location',
        'timezone',
        'image',
        'description',
        'district',
    )

    list_display = (
        '__str__',
        'year',
        'season',
        'district',
        'name',
        # 'location',
        # 'timezone',
        # 'start_date',
        # 'end_date',
        # 'status',
    )

    list_editable = [
        'name',
        # 'location',
        # 'start_date',
        # 'end_date',
    ]

    list_filter = (
        'status',
        'season',
        'district',
        'year',
    )

    fsm_field = [
        'status',
    ]

    search_fields = [
        'name',
    ]

    inlines = [
        AssignmentInline,
        SessionInline,
    ]

    readonly_fields = (
        'id',
    )

    autocomplete_fields = [
        # 'group',
        'owners',
    ]

    ordering = (
        '-year',
        'season',
        # 'group__tree_sort',
    )
    list_select_related = [
        # 'group',
    ]

    save_on_top = True


@admin.register(Contest)
class ContestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'award_id',
        'award_age',
        'award_description',
        'award_district',
        'award_division',
        'award_gender',
        'award_is_novice',
        'award_kind',
        'award_level',
        'award_name',
        'award_scope',
        'award_scope_range',
        'award_season',
        'award_size',
        'award_size_range',
        'award_tree_sort',

        'session',
        # 'group',
    ]

    list_display = (
        'id',
        # 'award_id',
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
        'award_tree_sort',
    ]

    autocomplete_fields = [
        # 'award',
        'session',
        # 'group',
    ]

    search_fields = [
        'award_name',
        'award_district',
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
        'session',
        'status',
        # 'group',
    )

    list_select_related = [
        'session',
    ]

    list_filter = [
        SessionConventionStatusListFilter,
        'status',
        'session__kind',
        'session__convention__season',
        'session__convention__year',
    ]

    inlines = [
        # AppearanceInline,
        StateLogInline,
    ]

    search_fields = [
        'id',
        'session__convention__name',
        # 'group__name',
    ]

    autocomplete_fields = [
        'session',
        'contests',
        'owners',
    ]
    readonly_fields = (
        'id',
    )

    save_on_top = True

    ordering = (
    )
    class Media:
        css = {
            'all': ('css/admin.css',),
        }


@admin.register(Session)
class SessionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = [
        'id',
        'status',
        'convention',
        'kind',
        ('num_rounds', 'is_invitational',),
        'target',
        'legacy_report',
        'drcj_report',
        'owners',
        # 'contests',
        # 'footnotes',
        'description',
        'notes',
    ]

    list_display = [
        '__str__',
        'convention',
        # 'convention__district',
        'kind',
        'num_rounds',
        'is_invitational',
        'status',
    ]

    list_filter = (
        ConventionStatusListFilter,
        'status',
        'kind',
        'num_rounds',
        'is_invitational',
        'convention__season',
        'convention__district',
        'convention__year',
    )

    autocomplete_fields = [
        'convention',
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
        'convention',
    ]

    ordering = (
        '-convention__year',
        'convention__season',
        # 'convention__group__tree_sort',
        'kind',
    )

    search_fields = [
        'convention__name',
        'kind',
    ]

    # raw_id_fields = [
    #     'owners',
    # ]
