# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin
from django.utils.html import format_html
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as AuthGroup
from django.utils import timezone
from django.contrib import messages
from django.apps import apps
from django.conf import settings
# Local
from .filters import AppearanceConventionStatusListFilter
from .filters import ConventionStatusListFilter
from .filters import MCListFilter
from .filters import MCUserListFilter
from .filters import SessionConventionStatusListFilter
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AppearanceInline
from .inlines import ContenderInline
from .inlines import OutcomeInline
from .inlines import PanelistInline
from .inlines import RoundInline
from .inlines import ScoreInline
from .inlines import SongInline
from .models import Appearance
from .models import Contender
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Song
from .models import User

from apps.stage.inlines import GridInline

admin.site.site_header = 'Barberscore Admin Backend'


@admin.register(Appearance)
class AppearanceAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'actual_start',
        'actual_finish',
        'group',
        'round',
        'num',
        'draw',
        'base',
        'is_single',
        'is_private',
        'participants',
        'representing',
        'pos',
        'stats',
        'csa',
        'variance_report',
    ]
    list_display = [
        'status',
        'group',
        'round',
        'num',
        'draw',
        'status',
    ]
    list_select_related = [
        'group',
        'round__session',
        'round__session__convention',
    ]
    list_filter = [
        AppearanceConventionStatusListFilter,
        'status',
        'round__session__kind',
        'round__session__convention__season',
        'round__session__convention__year',
    ]
    fsm_field = [
        'status',
    ]
    save_on_top = True
    autocomplete_fields = [
        'group',
        'round',
    ]
    readonly_fields = [
        'id',
        'stats',
        # 'csa',
        'variance_report',
    ]
    search_fields = [
        'group__name',
        'round__session__convention__name',
    ]
    inlines = [
        SongInline,
    ]
    ordering = (
        'group__name',
    )


@admin.register(Contender)
class ContenderAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'status',
        # 'appearance',
        # 'outcome',
    ]

    list_display = [
        'id',
    ]


    list_filter = (
        'status',
    )

    readonly_fields = [
    ]

    # autocomplete_fields = [
    #     'appearance',
    #     'outcome',
    # ]

    search_fields = [
        'id',
    ]

    ordering = (
    )


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'id',
        'status',
        'round',
        'award',
        'num',
        'name',
        'legacy_name',
    ]

    list_display = [
        'status',
        'round',
        'award',
        'num',
        'name',
        'legacy_name',
    ]

    list_filter = (
        'status',
    )

    list_select_related = [
        'round',
        'award',
    ]

    autocomplete_fields = [
        'round',
        'award',
    ]

    readonly_fields = [
        'id',
    ]
    search_fields = [
        'id',
    ]

    inlines = [
        ContenderInline,
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
        'person',
        'category',
        'psa',
    ]

    list_display = [
        'num',
        'kind',
        'category',
        'person',
        'round',
        'psa',
    ]

    list_editable = [
        'person',
    ]
    list_filter = (
        AppearanceConventionStatusListFilter,
        'status',
        'kind',
        'category',
    )

    list_select_related = [
        'round',
        'person',
    ]

    search_fields = [
        'id',
    ]

    autocomplete_fields = [
        'round',
        'person',
    ]
    readonly_fields = [
        'id',
    ]


@admin.register(Round)
class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'oss',
        # 'sa',
        # 'legacy_oss',
        ('session', 'kind', 'num', 'spots',),
        # 'footnotes',
        '__str__',
        # 'session__kind',
        ('date', 'is_reviewed'),
    ]

    list_display = [
        '__str__',
        'status',
        'legacy_oss',
    ]


    list_filter = [
        SessionConventionStatusListFilter,
        'status',
        'kind',
        'session__kind',
        'session__convention__season',
        'session__convention__district',
        'session__convention__year',
        # 'is_reviewed',
    ]

    fsm_field = [
        'status',
    ]

    ordering = (
        '-session__convention__year',
        'session__convention__name',
        '-session__kind',
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
        'session',
    ]

    inlines = [
        OutcomeInline,
        PanelistInline,
        AppearanceInline,
        GridInline,
        StateLogInline,
    ]

    search_fields = [
        'session__convention__name',
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
        'chart',
        'legacy_chart',
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
        'chart',
    ]

    ordering = (
        'num',
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        'username',
        'person',
        'is_mc',
    ]
    list_select_related = [
        'person',
    ]
    autocomplete_fields = [
        'person',
    ]
    list_filter = (
        'is_staff',
        MCUserListFilter,
    )

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'username',
                'person',
                'is_mc',
                'is_staff',
                'created',
                'modified',
                'is_convention_manager',
                'is_session_manager',
                'is_round_manager',
                'is_scoring_manager',
                'is_group_manager',
                'is_person_manager',
                'is_award_manager',
                'is_officer_manager',
                'is_chart_manager',
                'is_assignment_manager',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'person',
            )
        }),
    )
    search_fields = [
        'username',
        'person__first_name',
        'person__last_name',
        'person__bhs_id',
        'person__email',
    ]
    ordering = (
        'person__last_name',
        'person__first_name',
    )
    filter_horizontal = ()
    readonly_fields = [
        'id',
        'is_mc',
        'created',
        'modified',
    ]

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'

admin.site.unregister(AuthGroup)
