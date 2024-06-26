# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin
from django.utils.html import format_html
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.contrib import messages
from django.apps import apps
from django.conf import settings
# Local
# from .filters import AppearanceConventionStatusListFilter
# from .filters import ConventionStatusListFilter
# from .filters import MCListFilter
# from .filters import MCUserListFilter
# from .filters import SessionConventionStatusListFilter

from .inlines import AppearanceInline
from .inlines import OutcomeInline
from .inlines import PanelistInline
from .inlines import RoundInline
from .inlines import ScoreInline
from .inlines import SongInline

from .models import Appearance
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Song

admin.site.site_header = 'Barberscore Admin Backend'


@admin.register(Appearance)
class AppearanceAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'name',
        'status',
        'onstage',
        'actual_start',
        'actual_finish',
        'owners',
        'area',
        'group_id',
        'round',
        'num',
        'draw',
        'base',
        'is_single',
        'is_private',
        'participants',
        'district',
        'pos',
        'stats',
        'csa_report',
        'variance_report',
        'outcomes',
    ]
    list_display = [
        'status',
        'round',
        'get_group',
        'num',
        'draw',
    ]

    list_display_links = [
        'status',
        'get_group',
    ]

    list_select_related = [
        # 'round__session',
        # 'round__session__convention',
    ]
    list_filter = [
        # AppearanceConventionStatusListFilter,
        'status',
        # 'round__session__kind',
        # 'round__session__convention__season',
        # 'round__session__convention__year',
    ]
    fsm_field = [
        'status',
    ]
    save_on_top = True
    autocomplete_fields = [
        'round',
        'owners',
        'outcomes',
    ]
    readonly_fields = [
        'id',
        'name',
        'stats',
        # 'csa',
        # 'variance_report',
    ]
    search_fields = [
        # 'round__session__convention__name',
        'id',
        'name',
    ]
    inlines = [
        SongInline,
    ]

    # Adds group name to admin list view
    def get_group(self, obj):
        Group = apps.get_model('bhs.group')
        group = Group.objects.get(id=obj.group_id)
        return group.name
    get_group.short_description = 'Group'
    get_group.admin_order_field = 'appearance__group'

@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'id',
        'status',
        'name',
        'round',
        # 'award_id',
        'num',
        'level',
        'printed',
        'print_on_finals_oss',
        # 'appearances',
    ]

    list_display = [
        'status',
        'round',
        # 'award_id',
        'num',
        'name',
        # 'legacy_name',
    ]

    list_filter = (
        'status',
    )

    list_select_related = [
        'round',
        # 'award',
    ]

    autocomplete_fields = [
        'round',
    ]

    readonly_fields = [
        'id',
    ]
    search_fields = [
        'id',
    ]

    inlines = [
    ]


@admin.register(Panelist)
class PanelistAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'id',
        'status',
        'num',
        'kind',
        'round',
        'person_id',
        # 'user',
        'category',
        'psa_report',
    ]

    list_display = [
        'num',
        'kind',
        'category',
        'name',
        'round',
    ]

    list_filter = (
        # AppearanceConventionStatusListFilter,
        'status',
        'kind',
        'category',
    )

    list_select_related = [
        'round',
    ]

    search_fields = [
        'id',
        'name',
    ]

    autocomplete_fields = [
        'round',
        # 'user',
    ]
    readonly_fields = [
        'id',
    ]


@admin.register(Round)
class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'status',
                'oss_report',
                'sa_report',
                'owners',
                # 'legacy_oss',
                ('kind', 'num', 'spots',),
                # 'footnotes',
                '__str__',
                'session_nomen',
            )
        }),
        ('Revision', {
            'fields': ('revision_number', ('revision_date', 'revision_reason')),
        }),
    )

    list_display = [
        '__str__',
        'status',
        'session_id',
        'legacy_oss',
    ]


    list_filter = [
        # SessionConventionStatusListFilter,
        'status',
        'kind',
        'session_kind',
        'district',
    ]

    fsm_field = [
        'status',
    ]

    ordering = (
        # '-session__convention__year',
        # 'session__convention__name',
        # '-session__kind',
        '-date',
        'kind',
    )

    save_on_top = True

    readonly_fields = [
        'id',
        '__str__',
        # 'sa',
        # 'session__kind',
    ]

    autocomplete_fields = [
        # 'session',
        'owners',
    ]

    inlines = [
        OutcomeInline,
        PanelistInline,
        AppearanceInline,
        StateLogInline,
    ]

    search_fields = [
        'id',
        # 'session__convention__name',
    ]


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        # 'status',
        'song',
        'panelist',
        'points',
    ]

    readonly_fields = [
        'song',
        'panelist',
    ]

    list_display = [
        # 'status',
        'points',
    ]

    # list_filter = [
    #     'status',
    # ]

    autocomplete_fields = [
        'song',
        'panelist',
    ]

    ordering = [
        'song',
        'panelist',
    ]
    search_fields = [
        'id',
    ]

    save_on_top = True


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = [
        'id',
        # 'name',
        'stats',
        'appearance',
        'chart_id',
        # 'legacy_chart',
        'num',
        'penalties',
        # 'title',
    ]

    list_display = (
        'id',
        'appearance',
        'num',
    )

    # list_filter = (
    #     'status',
    # )

    search_fields = [
        'id',
    ]

    inlines = [
        ScoreInline,
    ]
    save_on_top = True

    readonly_fields = (
        'id',
        'stats',
    )

    autocomplete_fields = [
        'appearance',
        # 'chart',
    ]

    ordering = (
        'num',
    )
