# Django
# Third-Party
# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as AuthGroup

# Local
from .filters import OrphanListFilter
from .filters import MCListFilter
from .filters import MCUserListFilter
from .filters import ConventionStatusListFilter
from .filters import SessionConventionStatusListFilter
from .filters import AccountListFilter
from .filters import OfficeListFilter
from .filters import ConventionGroupListFilter
from .filters import DistrictListFilter
from .filters import DivisionListFilter
from .filters import GroupListFilter
from .filters import SessionGroupListFilter
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import ActiveQuartetInline
from .inlines import ActiveChapterInline
from .inlines import ActiveChorusInline
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
        'variance_report_new',
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
class AssignmentAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
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
    inlines = [
        StateLogInline,
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
class ChartAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'nomen',
        'status',
        'title',
        'composers',
        'lyricists',
        'arrangers',
        'holders',
        'image',
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
        StateLogInline,
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
    list_select_related = [
        'group',
    ]

    save_on_top = True


@admin.register(Competitor)
class CompetitorAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = (
        'status',
        'session',
        'group',
        'rank',
        ('is_ranked', 'is_multi',),
        'csa_report_new',
        ('tot_points', 'mus_points', 'per_points', 'sng_points',),
        ('tot_score', 'mus_score', 'per_score', 'sng_score',),
    )

    list_display = (
        'nomen',
        'status',
    )

    list_filter = [
        SessionConventionStatusListFilter,
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
        'csa_report_new',
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
        'is_mc',
        'name',
        'status',
        'kind',
        'gender',
        'is_senior',
        ('bhs_id', 'mc_pk', 'code',),
        'parent',
        ('international', 'district', 'division', 'chapter',),
        'location',
        'email',
        'phone',
        'website',
        'facebook',
        'twitter',
        'image',
        'description',
        'notes',
        ('created', 'modified',),
    ]

    list_filter = [
        'status',
        OrphanListFilter,
        MCListFilter,
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
        'is_mc',
        'kind',
        'gender',
        'parent',
        'bhs_id',
        'status',
        'created',
        'modified',
    ]
    list_select_related = [
        'parent',
    ]
    readonly_fields = [
        'id',
        'is_mc',
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
        'tree_sort',
    ]

    INLINES = {
        'International': [
            AwardInline,
            OfficerInline,
            ConventionInline,
            StateLogInline,
        ],
        'District': [
            AwardInline,
            OfficerInline,
            ConventionInline,
            ActiveChapterInline,
            ActiveQuartetInline,
            StateLogInline,
        ],
        'Noncompetitive': [
            OfficerInline,
            GroupInline,
            StateLogInline,
        ],
        'Affiliate': [
            OfficerInline,
            GroupInline,
            StateLogInline,
        ],
        'Division': [
            AwardInline,
            ActiveChapterInline,
            ActiveQuartetInline,
            StateLogInline,
        ],
        'Chapter': [
            ActiveChorusInline,
            StateLogInline,
        ],
        'Chorus': [
            OfficerInline,
            # MemberInline,
            RepertoryInline,
            EntryInline,
            CompetitorInline,
            StateLogInline,
        ],
        'Quartet': [
            OfficerInline,
            MemberInline,
            RepertoryInline,
            EntryInline,
            CompetitorInline,
            StateLogInline,
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

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'


@admin.register(Member)
class MemberAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'is_mc',
        'status',
        'group',
        'person',
        'part',
        'mc_pk',
        'inactive_date',
        'inactive_reason',
        'sub_status',
        'current_through',
        'established_date',
        'mem_code',
        'mem_status',
        'created',
    ]
    list_display = [
        'status',
        'is_mc',
        'person',
        'group',
        'part',
        'created',
    ]
    readonly_fields = [
        'id',
        'is_mc',
        'part',
        'inactive_date',
        'inactive_reason',
        'sub_status',
        'current_through',
        'established_date',
        'mem_code',
        'mem_status',
        'created',
    ]

    autocomplete_fields = [
        'person',
        'group',
    ]
    search_fields = [
        'person',
        'group',
    ]
    list_filter = [
        'status',
        MCListFilter,
        'group__kind',
        'group__status',
        'part',
        'inactive_date',
        'inactive_reason',
        'sub_status',
        'current_through',
        'established_date',
        'mem_code',
        'mem_status',
        'created',
    ]
    list_select_related = [
        'person',
        'group',
    ]
    inlines = [
        StateLogInline,
    ]

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'name',
        'is_mc',
        'short_name',
        'kind',
        'mc_pk',
        'is_convention_manager',
        'is_session_manager',
        'is_scoring_manager',
        'is_group_manager',
        'is_person_manager',
        'is_award_manager',
        'is_judge_manager',
        'is_chart_manager',
    ]

    list_display = [
        'name',
        'is_mc',
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

    readonly_fields = [
        'id',
        'is_mc',
    ]

    list_filter = [
        'status',
        'kind',
        MCListFilter,
        'is_convention_manager',
        'is_session_manager',
        'is_scoring_manager',
        'is_group_manager',
        'is_person_manager',
        'is_award_manager',
        'is_judge_manager',
        'is_chart_manager',
    ]

    inlines = [
        OfficerInline,
    ]

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'


@admin.register(Officer)
class OfficerAdmin(FSMTransitionMixin, admin.ModelAdmin):
    def office__code(self, obj):
        return "{0}".format(obj.office.short_name)

    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'is_mc',
        'status',
        'person',
        'office',
        'group',
        'start_date',
        'end_date',
        'mc_pk'
    ]

    list_display = [
        'is_mc',
        'person',
        'office',
        'office__code',
        'group',
        'start_date',
        'end_date',
        'status',
    ]
    readonly_fields = [
        'id',
        'is_mc',
        office__code,
    ]
    list_select_related = [
        'person',
        'group',
        'office',
    ]
    list_filter = [
        'status',
        MCListFilter,
        OfficeListFilter,
        'group__kind',
    ]
    inlines = [
        StateLogInline,
    ]
    search_fields = [
        'nomen',
    ]
    autocomplete_fields = [
        'office',
        'person',
        'group',
    ]
    ordering = [
        'group__tree_sort',
    ]

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'


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
        'is_mc',
        'email',
        'is_deceased',
        'bhs_id',
        'mc_pk',
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
        'image',
        'description',
        'notes',
        ('created', 'modified',),
    ]

    list_display = [
        'nomen',
        'is_mc',
        'email',
        'bhs_id',
        # 'mc_pk',
        'current_through',
        'part',
        'gender',
        'status',
        'created',
        'modified',
    ]

    list_filter = [
        'status',
        MCListFilter,
        'gender',
        'part',
        'is_deceased',
    ]

    readonly_fields = [
        'id',
        'is_mc',
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

    # autocomplete_fields = [
    #     'user',
    # ]

    save_on_top = True

    inlines = [
        OfficerInline,
        MemberInline,
        AssignmentInline,
        StateLogInline,
    ]

    # readonly_fields = [
    #     'common_name',
    # ]
    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'


@admin.register(Repertory)
class RepertoryAdmin(admin.ModelAdmin):
    # fsm_field = [
    #     'status',
    # ]

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
    #     StateLogInline,
    # ]

    search_fields = [
        'nomen',
    ]


@admin.register(Round)
class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        # 'name',
        'status',
        ('session', 'kind', 'num'),
        'ors_report_new',

    ]

    list_display = [
        'nomen',
        'status',
    ]

    list_filter = [
        SessionConventionStatusListFilter,
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
        'ors_report_new',
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
        'convention',
        'kind',
        'gender',
        'num_rounds',
        'is_invitational',
        'description',
        'notes',
        'bbscores_report_new',
        'drcj_report_new',
        'admins_report_new',
        'sa_report_new',
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
        ConventionStatusListFilter,
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
class UserAdmin(FSMTransitionMixin, BaseUserAdmin):
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
        'is_mc',
    ]

    # list_editable = [
    #     'account_id',
    # ]
    list_select_related = [
        'person',
    ]

    # list_display_links = [
    #     'email',
    #     'person',
    # ]

    autocomplete_fields = [
        'person',
    ]

    list_filter = (
        'status',
        'is_staff',
        MCUserListFilter,
        AccountListFilter,
    )

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'name',
                'status',
                'email',
                'person',
                'account_id',
                'is_mc',
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
                'person',
            )
        }),
    )
    search_fields = [
        'email',
        'name',
    ]
    inlines = [
        StateLogInline,
    ]
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = [
        'id',
        # 'email',
        # 'account_id',
        'is_mc',
        'is_group_manager',
        'is_session_manager',
        'is_scoring_manager',
    ]

    def is_mc(self, instance):
        return instance.person.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'




admin.site.unregister(AuthGroup)
