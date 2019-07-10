# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

# Django
from django.contrib import admin

# Local
from .filters import ConventionStatusListFilter
from .filters import SessionConventionStatusListFilter

from .inlines import ContestantInline
from .inlines import ContestInline
from .inlines import EntryInline

from .models import Contest
from .models import Contestant
from .models import Entry
from .models import Session

# from api.inlines import RoundInline

admin.site.site_header = 'Barberscore Admin Backend'


@admin.register(Contest)
class ContestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'award',
        'session',
        'result',
        'group',
    ]

    list_display = (
        'id',
        'award',
        'session',
        'result',
        'group',
    )

    list_filter = [
        'status',
        'award__kind',
    ]

    save_on_top = True

    inlines = [
        ContestantInline,
    ]

    fsm_field = [
        'status',
    ]

    readonly_fields = [
        'id',
    ]

    autocomplete_fields = [
        'award',
        'session',
        'group',
    ]

    search_fields = [
        'award__name',
    ]


@admin.register(Contestant)
class ContestantAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'status',
        'entry',
        'contest',
    ]

    list_filter = (
        'status',
    )

    readonly_fields = [
    ]

    autocomplete_fields = [
        'entry',
        'contest',
    ]

    search_fields = [
        'id',
    ]

    ordering = (
    )


@admin.register(Entry)
class EntryAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = (
        'id',
        'status',
        'session',
        'group',
        'representing',
        ('is_evaluation', 'is_private', 'is_mt'),
        'draw',
        'base',
        'prelim',
        'seed',
        'participants',
        'description',
        'notes',
    )

    list_display = (
        'status',
        'session',
        'group',
    )

    list_filter = [
        SessionConventionStatusListFilter,
        'status',
        'session__kind',
        'session__convention__season',
        'session__convention__year',
    ]

    inlines = [
        # AppearanceInline,
        ContestantInline,
        StateLogInline,
    ]

    search_fields = [
        'id',
        'session__convention__name',
        'group__name',
    ]

    autocomplete_fields = [
        'session',
        'group',
    ]
    readonly_fields = (
        'id',
    )

    save_on_top = True

    ordering = (
    )


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
        # 'footnotes',
        'description',
        'notes',
    ]

    list_display = [
        '__str__',
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
        'convention__group__tree_sort',
        'kind',
    )

    search_fields = [
        'convention__name',
        'kind',
    ]

    # raw_id_fields = [
    #     'owners',
    # ]
