# Django
# Third-Party
# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as AuthGroup

# Local
from .filters import BHSListFilter
from .filters import ConventionGroupListFilter
from .filters import DistrictListFilter
from .filters import DivisionListFilter
from .filters import GroupListFilter
from .filters import SessionGroupListFilter
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AppearanceInline
from .inlines import AssignmentInline
from .inlines import AwardInline
from .inlines import CompetitorInline
from .inlines import ContestantInline
from .inlines import ContestInline
from .inlines import ConventionInline
from .inlines import EntryInline
from .inlines import GrantorInline
from .inlines import GridInline
from .inlines import GroupInline
from .inlines import MemberInline
from .inlines import OfficerInline
from .inlines import PanelistInline
from .inlines import RepertoryInline
from .inlines import RoundInline
from .inlines import ScoreInline
from .inlines import SessionInline
from .inlines import SongInline
from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Chart
from .models import Competitor
from .models import Contest
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grantor
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User
from .models import Venue

admin.site.site_header = 'Barberscore Admin Backend'


@admin.register(Appearance)
class AppearanceAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'actual_start',
        'actual_finish',
        'competitor',
        'round',
        'num',
        'draw',
        'variance_report_link',
        ('mus_points', 'per_points', 'sng_points', 'tot_points',),
        ('mus_score', 'per_score', 'sng_score', 'tot_score',),
    ]
    list_display = [
        'nomen',
        'num',
        'draw',
        'status',
    ]
    list_filter = [
        'status',
        'round__session__kind',
        'round__session__convention__season',
        'round__session__convention__year',
    ]
    fsm_field = [
        'status',
    ]
    save_on_top = True
    readonly_fields = [
        'id',
        'nomen',
        'variance_report_link',
    ]
    autocomplete_fields = [
        'competitor',
        'round',
    ]
    search_fields = (
        'nomen',
    )
    inlines = [
        SongInline,
    ]


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'kind',
        'convention',
        'person',
        'category',
    ]

    list_display = [
        'nomen',
        'status',
        'kind',
        'category',
        'person',
        'convention',
    ]

    list_filter = (
        'status',
        'kind',
        'category',
    )

    list_select_related = [
        'convention',
        'person',
    ]

    search_fields = [
        'nomen',
    ]

    autocomplete_fields = [
        'convention',
        'person',
    ]

    readonly_fields = [
        'nomen',
    ]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'id',
        'name',
        'status',
        'group',
        'kind',
        'gender',
        'level',
        'season',
        'rounds',
        ('is_primary', 'is_invitational', 'is_manual'),
        'parent',
        ('threshold', 'minimum', 'advance',),
        'footnote',
        'description',
        'notes',
    ]

    list_display = [
        'nomen',
        'name',
        'group',
        'kind',
        'gender',
        'level',
        'season',
        'rounds',
        'is_primary', 'is_invitational', 'is_manual',
        'status',
    ]

    list_filter = [
        'status',
        'kind',
        'gender',
        'level',
        'season',
        'is_primary', 'is_invitational', 'is_manual',
        GroupListFilter,
    ]

    readonly_fields = [
        'id',
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    autocomplete_fields = [
        'group',
    ]

    ordering = (
        'group__tree_sort',
        'kind',
        'gender',
        'level',
    )


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):

    fields = [
        'nomen',
        'status',
        'title',
        'composers',
        'lyricists',
        'arrangers',
        'holders',
        'img',
        'description',
        'notes',
        # 'gender',
        # 'tempo',
        # 'is_medley',
        # 'is_learning',
        # 'voicing',
    ]

    list_display = [
        'nomen',
        'title',
        'arrangers',
        'composers',
        'lyricists',
        'status',
    ]

    list_editable = [
        'title',
        'arrangers',
        'composers',
        'lyricists',
        'status',
    ]

    list_filter = [
        'status',
    ]

    inlines = [
        RepertoryInline,
    ]

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
        'title',
    ]

    ordering = (
        'nomen',
    )


@admin.register(Contest)
class ContestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'status',
        'award',
        'session',
        'champion',
    ]

    list_display = (
        'nomen',
        'session',
    )

    list_filter = [
        'status',
        'award__kind',
        'award__is_primary',
    ]

    save_on_top = True

    inlines = [
        ContestantInline,
    ]

    fsm_field = [
        'status',
    ]

    readonly_fields = [
        'nomen',
    ]

    autocomplete_fields = [
        'award',
        'session',
    ]

    search_fields = [
        'nomen',
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
        'nomen',
    ]

    autocomplete_fields = [
        'entry',
        'contest',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'nomen',
    )


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = (
        'name',
        'status',
        'is_archived',
        'group',
        'year',
        'season',
        'panel',
        'venue',
        ('open_date', 'close_date',),
        ('start_date', 'end_date',),
        'description',
    )

    list_display = (
        'nomen',
        'group',
        'start_date',
        'end_date',
        'year',
        'season',
        'status',
    )

    list_filter = (
        'is_archived',
        'status',
        'season',
        ConventionGroupListFilter,
        'year',
    )

    fsm_field = [
        'status',
    ]

    search_fields = (
        'nomen',
    )

    inlines = [
        AssignmentInline,
        SessionInline,
        GrantorInline,
    ]

    readonly_fields = (
        'nomen',
    )

    autocomplete_fields = [
        'group',
        'venue',
    ]

    ordering = (
        '-year',
        '-season',
        'group__tree_sort',
    )

    save_on_top = True


@admin.register(Competitor)
class CompetitorAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = (
        'status',
        'is_archived',
        'session',
        'group',
        'img',
        'rank',
        ('is_ranked', 'is_multi',),
        'csa_report_link',
        ('tot_points', 'mus_points', 'per_points', 'sng_points',),
        ('tot_score', 'mus_score', 'per_score', 'sng_score',),
    )

    list_display = (
        'nomen',
        'status',
    )

    list_filter = [
        'is_archived',
        'status',
        'session__kind',
        'session__convention__season',
        'session__convention__year',
    ]

    inlines = [
        AppearanceInline,
        GridInline,
        # ContestantInline,
    ]

    search_fields = (
        'nomen',
    )

    autocomplete_fields = [
        'session',
        'group',
    ]

    readonly_fields = (
        'nomen',
        'csa_report_link',
    )

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(Entry)
class EntryAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = (
        'id',
        'status',
        'is_archived',
        'session',
        'group',
        'representing',
        ('is_evaluation', 'is_private',),
        'draw',
        'prelim',
        'seed',
        'directors',
        'rank',
        'description',
        'notes',
        ('mus_points', 'per_points', 'sng_points', 'tot_points',),
        ('mus_score', 'per_score', 'sng_score', 'tot_score',),
    )

    list_display = (
        'nomen',
        'status',
    )

    list_filter = [
        'is_archived',
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

    search_fields = (
        'nomen',
    )

    autocomplete_fields = [
        'session',
        'group',
    ]
    readonly_fields = (
        'id',
        'nomen',
    )

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(Grantor)
class GrantorAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'group',
        'convention',
    ]
    list_display = [
        'nomen',
        'group',
        'convention',
    ]

    readonly_fields = [
        'nomen',
    ]
    autocomplete_fields = [
        'group',
        'convention',
    ]


@admin.register(Grid)
class GridAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        # 'name',
        'status',
        'num',
        'onstage',
        'start',
        'round',
        'competitor',
        'renditions',
    ]
    list_display = [
        'nomen',
        'status',
        'onstage',
        'start',
    ]
    list_filter = (
        'status',
    )
    readonly_fields = [
        'nomen',
    ]
    autocomplete_fields = [
        'round',
        'competitor',
    ]
    ordering = [
        'num',
    ]


@admin.register(Group)
class GroupAdmin(FSMTransitionMixin, admin.ModelAdmin):
    save_on_top = True
    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'name',
        'status',
        'parent',
        'kind',
        'gender',
        'is_senior',
        ('bhs_id', 'bhs_pk',),
        ('international', 'district', 'division', 'chapter',),
        'location',
        'email',
        'phone',
        'website',
        'facebook',
        'twitter',
        'img',
        'description',
        'notes',
        ('created', 'modified',),
    ]

    list_filter = [
        'status',
        BHSListFilter,
        'kind',
        'gender',
        DistrictListFilter,
        DivisionListFilter,
    ]

    search_fields = [
        'nomen',
        'bhs_id',
    ]

    list_display = [
        'name',
        'kind',
        'gender',
        'parent',
        'bhs_id',
        'status',
        'created',
        'modified',
    ]
    list_select_related = [
    ]
    readonly_fields = [
        'id',
        'nomen',
        'international',
        'district',
        'division',
        'chapter',
        'created',
        'modified',
    ]

    # autocomplete_fields = [
    #     'parent',
    # ]
    raw_id_fields = [
        'parent',
    ]

    ordering = [
        'name',
    ]

    INLINES = {
        'International': [
            AwardInline,
            OfficerInline,
            ConventionInline,
        ],
        'District': [
            AwardInline,
            OfficerInline,
            ConventionInline,
        ],
        'Noncompetitive': [
            AwardInline,
            OfficerInline,
            ConventionInline,
        ],
        'Affiliate': [
            AwardInline,
            OfficerInline,
            ConventionInline,
        ],
        'Division': [
            AwardInline,
        ],
        'Chapter': [
            GroupInline,
        ],
        'Chorus': [
            OfficerInline,
            # MemberInline,
            RepertoryInline,
            EntryInline,
            CompetitorInline,
        ],
        'Quartet': [
            OfficerInline,
            MemberInline,
            RepertoryInline,
            EntryInline,
            CompetitorInline,
        ],
    }

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        try:
            inlines = self.INLINES[obj.KIND[obj.kind]]
        except AttributeError:
            return inline_instances

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            inline_instances.append(inline)
        return inline_instances

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    fields = [
        'status',
        # 'start_date',
        # 'end_date',
        'group',
        'person',
        'part',
        'bhs_pk',
        'sub_status',
        'mem_status',
        'mem_code',
        'inactive_date',
        'inactive_reason',
    ]
    list_display = [
        'status',
        # 'start_date',
        # 'end_date',
        'bhs_pk',
        'group',
        'person',
        'part',
        'sub_status',
        'mem_status',
        'mem_code',
        'inactive_date',
        'inactive_reason',
    ]
    autocomplete_fields = [
        'person',
        'group',
    ]
    search_fields = [
        'nomen',
    ]
    list_filter = [
        'status',
        BHSListFilter,
        'part',
        'group__kind',
        'sub_status',
        'mem_status',
        'mem_code',
        'inactive_reason',
    ]
    readonly_fields = [
        'sub_status',
        'mem_status',
        'mem_code',
        'inactive_date',
        'inactive_reason',
    ]


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'short_name',
        'kind',
        'is_convention_manager',
        'is_session_manager',
        'is_scoring_manager',
        'is_group_manager',
        'is_person_manager',
        'is_award_manager',
        'is_judge_manager',
        'is_chart_manager',
    ]
    search_fields = [
        'nomen',
        'short_name',
    ]

    list_filter = [
        'status',
        'kind',
        'is_convention_manager',
        'is_session_manager',
        'is_scoring_manager',
        'is_group_manager',
        'is_person_manager',
        'is_award_manager',
        'is_judge_manager',
        'is_chart_manager',
    ]

    # inlines = [
    #     OfficerInline,
    # ]


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'person',
        'office',
        'group',
        'start_date',
        'end_date',
        'bhs_pk'
    ]

    list_display = [
        'nomen',
        'start_date',
        'end_date',
        'status',
    ]
    list_filter = [
        'status',
        BHSListFilter,
        'office',
    ]
    search_fields = [
        'nomen',
    ]
    autocomplete_fields = [
        'office',
        'person',
        'group',
    ]


@admin.register(Panelist)
class PanelistAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'num',
        'kind',
        'round',
        'person',
        'category',
    ]

    list_display = [
        'nomen',
        'num',
        'status',
        'kind',
        'category',
        'person',
        'round',
    ]

    list_filter = (
        'status',
        'kind',
        'category',
    )

    list_select_related = [
        'round',
        'person',
    ]

    search_fields = [
        'nomen',
    ]

    autocomplete_fields = [
        'round',
        'person',
    ]

    readonly_fields = [
        'nomen',
    ]


@admin.register(Person)
class PersonAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        ('first_name', 'middle_name', 'last_name', 'nick_name',),
        'status',
        'user',
        'email',
        'is_deceased',
        'bhs_id',
        'bhs_pk',
        'current_through',
        'birth_date',
        'part',
        'gender',
        'spouse',
        'location',
        'website',
        'facebook',
        'twitter',
        'phone',
        'img',
        'description',
        'notes',
        ('created', 'modified',),
    ]

    list_display = [
        'nomen',
        'email',
        'bhs_id',
        'bhs_pk',
        'current_through',
        'part',
        'gender',
        'status',
        'created',
        'modified',
    ]

    list_filter = [
        'status',
        BHSListFilter,
        'gender',
        'part',
        'is_deceased',
    ]

    readonly_fields = [
        'id',
        'nomen',
        'current_through',
        'created',
        'modified',
    ]

    fsm_field = [
        'status',
    ]

    search_fields = (
        'nomen',
        'email',
    )

    autocomplete_fields = [
        'user',
    ]

    save_on_top = True

    inlines = [
        OfficerInline,
        MemberInline,
        AssignmentInline,
    ]

    # readonly_fields = [
    #     'common_name',
    # ]


@admin.register(Repertory)
class RepertoryAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'group',
        'chart',
    ]

    list_display = [
        'nomen',
        'status',
        'group',
        'chart',
    ]

    fsm_field = [
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'nomen',
        # 'session',
        # 'kind',
    ]

    autocomplete_fields = [
        'group',
        'chart',
    ]

    # inlines = [
    #     AppearanceInline,
    # ]

    search_fields = [
        'nomen',
    ]


@admin.register(Round)
class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        # 'name',
        'status',
        'is_archived',
        ('session', 'kind', 'num'),
        'ors_report_link',

    ]

    list_display = [
        'nomen',
        'status',
    ]

    list_filter = [
        'is_archived',
        'status',
        'session__kind',
        'session__convention__season',
        'session__convention__year',
    ]

    fsm_field = [
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'nomen',
        'ors_report_link',
        # 'session',
        # 'kind',
    ]

    autocomplete_fields = [
        'session',
    ]

    inlines = [
        AppearanceInline,
        PanelistInline,
        GridInline,
    ]

    search_fields = [
        'nomen',
    ]


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        # 'status',
        'song',
        'panelist',
        'category',
        'kind',
        'original',
        'violation',
        'penalty',
        'points',
    ]

    readonly_fields = [
        'nomen',
        'song',
        'panelist',
    ]

    list_display = [
        'nomen',
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
    save_on_top = True


@admin.register(Session)
class SessionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = [
        'id',
        'status',
        'is_archived',
        'convention',
        'kind',
        'gender',
        'num_rounds',
        'is_invitational',
        'description',
        'notes',
        'bbscores_report_link',
        'drcj_report_link',
        'admins_report_link',
        'sa_report_link',
    ]

    list_display = [
        'nomen',
        'status',
        'kind',
        'gender',
        'num_rounds',
        'is_invitational',
        'status',
    ]

    list_filter = (
        'is_archived',
        'status',
        'kind',
        'gender',
        'num_rounds',
        'is_invitational',
        SessionGroupListFilter,
        'convention__season',
        'convention__year',
    )

    autocomplete_fields = [
        'convention',
    ]

    readonly_fields = [
        'id',
        'nomen',
        'sa_report_link',
        'bbscores_report_link',
        'drcj_report_link',
        'admins_report_link',
    ]

    inlines = [
        ContestInline,
        EntryInline,
        CompetitorInline,
        RoundInline,
        StateLogInline,
    ]

    list_select_related = [
        'convention',
    ]

    ordering = (
        '-convention__year',
        '-convention__season',
        'convention__group__tree_sort',
        'kind',
    )

    search_fields = [
        'nomen',
    ]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        # 'status',
        'appearance',
        'chart',
        'num',
        'tot_points',

        # 'title',
    ]

    list_display = (
        'nomen',
        # 'status',
        # 'title',
        'appearance',
        'num',
    )

    # list_filter = (
    #     'status',
    # )

    search_fields = (
        'nomen',
    )

    inlines = [
        ScoreInline,
    ]
    save_on_top = True

    readonly_fields = (
        'nomen',
    )

    autocomplete_fields = [
        'appearance',
        'chart',
    ]

    ordering = (
        'nomen',
        'num',
    )


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
        'status',
        'city',
        'state',
        'airport',
        'timezone',
    )

    list_display = [
        'nomen',
        'name',
        'city',
        'state',
        'timezone',
    ]

    list_filter = (
        'status',
    )

    search_fields = (
        'nomen',
    )

    readonly_fields = [
        'nomen',
    ]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fsm_field = [
        'status',
    ]
    list_display = [
        'email',
        'name',
        'person',
        'is_staff',
        'account_id',
        'status',
    ]

    # list_editable = [
    #     'account_id',
    # ]

    list_display_links = [
        'email',
        'person',
    ]

    list_filter = (
        'status',
        'is_staff',
    )

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'name',
                'status',
                'email',
                'account_id',
                'is_staff',
                'is_group_manager',
                'is_session_manager',
                'is_scoring_manager',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name',
                'status',
                'email',
                'account_id',
                'is_staff',
            )
        }),
    )
    search_fields = [
        'email',
        'name',
    ]
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = [
        'id',
        # 'email',
        # 'account_id',
        'is_group_manager',
        'is_session_manager',
        'is_scoring_manager',
    ]


admin.site.unregister(AuthGroup)
