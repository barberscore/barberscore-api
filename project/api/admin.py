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
from .filters import AppearanceConventionStatusListFilter
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
from .models import Subscription
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
        ('mus_points', 'per_points', 'sng_points', 'tot_points',),
        ('mus_score', 'per_score', 'sng_score', 'tot_score',),
        'variance_report',
    ]
    list_display = [
        '__str__',
        'num',
        # 'draw',
        'tot_score',
        'status',
    ]
    list_select_related = [
        'competitor',
        'competitor__group',
        'competitor__session',
        'competitor__session__convention',
        'round__session',
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
        'competitor',
        'round',
    ]
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'competitor__group__name',
    ]
    inlines = [
        SongInline,
    ]
    ordering = (
        'competitor',
    )


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
        'person',
        'convention',
        'kind',
        'category',
        'status',
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
        'id',
    ]

    autocomplete_fields = [
        'convention',
        'person',
    ]

    readonly_fields = [
    ]
    inlines = [
        StateLogInline,
    ]


@admin.register(Award)
class AwardAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = [
        'id',
        'name',
        'status',
        'group',
        'kind',
        'age',
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
        'name',
        # 'size',
        # 'scope',
        'group',
        'kind',
        'age',
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
        'level',
        'age',
        'gender',
        'season',
        'is_primary', 'is_invitational', 'is_manual',
        GroupListFilter,
    ]

    readonly_fields = [
        'id',
    ]

    search_fields = [
        'name',
    ]

    autocomplete_fields = [
        'group',
        'parent',
    ]

    ordering = (
        'tree_sort',
    )


@admin.register(Chart)
class ChartAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'status',
        'title',
        'composers',
        'lyricists',
        'arrangers',
        'holders',
        'image',
        'description',
        'notes',
        'created',
        'modified',
        # 'gender',
        # 'tempo',
        # 'is_medley',
        # 'is_learning',
        # 'voicing',
    ]

    list_display = [
        'status',
        'title',
        'arrangers',
        'composers',
        'lyricists',
    ]

    list_editable = [
        'title',
        'arrangers',
        'composers',
        'lyricists',
    ]

    list_filter = [
        'status',
    ]

    inlines = [
        RepertoryInline,
        StateLogInline,
    ]

    readonly_fields = [
        'created',
        'modified',
    ]

    search_fields = [
        'title',
        'arrangers',
    ]

    ordering = (
        'title',
        'arrangers',
    )


@admin.register(Contest)
class ContestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'award',
        'session',
        'group',
    ]

    list_display = (
        'id',
        'award',
        'session',
        'group',
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


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = (
        'id',
        'name',
        'status',
        'group',
        'year',
        'season',
        'panel',
        'image',
        'venue',
        ('open_date', 'close_date',),
        ('start_date', 'end_date',),
        'description',
    )

    list_display = (
        'name',
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

    search_fields = [
        'name',
    ]

    inlines = [
        AssignmentInline,
        SessionInline,
        GrantorInline,
    ]

    readonly_fields = (
        'id',
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
        'draw',
        ('is_ranked', 'is_multi',),
        ('tot_points', 'mus_points', 'per_points', 'sng_points',),
        ('tot_score', 'mus_score', 'per_score', 'sng_score',),
    )

    list_display = (
        'status',
        'tot_score',
        'tot_points',
        'is_ranked',
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
        # GridInline,
        # ContestantInline,
    ]

    search_fields = [
        'session__convention__name',
        'group__name',
    ]

    autocomplete_fields = [
        'session',
        'group',
    ]

    readonly_fields = (
    )

    save_on_top = True

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

    search_fields = [
        'id',
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


@admin.register(Grantor)
class GrantorAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'group',
        'convention',
    ]
    list_display = [
        'group',
        'convention',
    ]

    readonly_fields = [
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
        'period',
        'num',
        'onstage',
        'start',
        'round',
        'renditions',
    ]
    list_display = [
        'status',
        'onstage',
        'start',
    ]
    list_filter = (
        'status',
        'period',
    )
    readonly_fields = [
    ]
    autocomplete_fields = [
        'round',
    ]
    ordering = [
        'round',
        'period',
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
        'name',
        'bhs_id',
        'code',
    ]

    list_display = [
        'name',
        'kind',
        'gender',
        'parent',
        'bhs_id',
        'is_mc',
        'status',
    ]
    list_select_related = [
        'parent',
    ]
    readonly_fields = [
        'id',
        'is_mc',
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
            MemberInline,
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

    def get_queryset(self, request):
        return super().get_queryset(
            request
        ).prefetch_related('members')

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
        'status',
        'person',
        'group',
        'part',
        'is_mc',
        'mc_pk',
        'current_through',
        'established_date',
        'inactive_date',
        'inactive_reason',
        'sub_status',
        'mem_code',
        'mem_status',
        'created',
        'modified',
    ]
    list_display = [
        'person',
        'group',
        'part',
        'is_mc',
        'status',
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
        'modified',
    ]

    autocomplete_fields = [
        'person',
        'group',
    ]
    search_fields = [
        'person__first_name',
        'person__last_name',
        'group__name',
        'person__bhs_id',
        'group__bhs_id',
    ]
    list_filter = [
        'status',
        MCListFilter,
        'subscription',
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
        'code',
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
        'code',
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
        'name',
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

    # inlines = [
    #     OfficerInline,
    # ]

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'


@admin.register(Officer)
class OfficerAdmin(FSMTransitionMixin, admin.ModelAdmin):
    def office__code(self, obj):
        return "{0}".format(obj.office.code)

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
        'person',
        'office__code',
        'group',
        'is_mc',
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
        'group__kind',
        'office__code',
    ]
    inlines = [
        StateLogInline,
    ]
    search_fields = [
        'person__last_name',
        'group__name',
    ]
    autocomplete_fields = [
        'office',
        'person',
        'group',
    ]
    ordering = [
        'office__code',
        'person__last_name',
        'person__first_name',
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
        'id',
    ]

    autocomplete_fields = [
        'round',
        'person',
    ]

    readonly_fields = [
    ]


@admin.register(Person)
class PersonAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        ('first_name', 'middle_name', 'last_name', 'nick_name',),
        'email',
        'is_deceased',
        'is_mc',
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
        'email',
        'phone',
        # 'mc_pk',
        # 'current_through',
        'part',
        'gender',
        'is_mc',
        'status',
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
        # 'current_through',
        'created',
        'modified',
    ]

    fsm_field = [
        'status',
    ]

    search_fields = [
        'last_name',
        'first_name',
        'bhs_id',
        'email',
    ]

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
class RepertoryAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'status',
        'group',
        'chart',
    ]

    list_display = [
        'group',
        'chart',
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'id',
    ]

    autocomplete_fields = [
        'group',
        'chart',
    ]

    inlines = [
        StateLogInline,
    ]

    search_fields = [
        'group__name',
        'chart__title',
    ]


@admin.register(Round)
class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        # 'name',
        'id',
        'status',
        ('session', 'kind', 'num', 'spots',),
        'date',
        'footnotes',
    ]

    list_display = [
        'status',
        'session',
        'kind',
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
        'id',
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
        'session__convention__name',
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
        'footnotes',
        'description',
        'notes',
    ]

    list_display = [
        '__str__',
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
        'convention__name',
        'kind',
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
        'id',
        'appearance',
        'num',
        'tot_points',
        'tot_score',
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
    )

    autocomplete_fields = [
        'appearance',
        'chart',
    ]

    ordering = (
        'num',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'status',
        'code',
    ]

    list_display = (
        'name',
        'status',
        'code',
    )

    list_filter = (
        'status',
    )

    search_fields = [
        'name',
    ]

    save_on_top = True

    readonly_fields = (
    )

    ordering = (
        'name',
    )


@admin.register(Venue)
class VenueAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = (
        'id',
        'name',
        'status',
        'city',
        'state',
        'airport',
        'timezone',
    )

    list_display = [
        'name',
        'city',
        'state',
        'airport',
        'timezone',
    ]

    list_filter = (
        'status',
    )

    search_fields = [
        'name',
        'city',
        'state',
    ]

    readonly_fields = [
        'id',
    ]


@admin.register(User)
class UserAdmin(FSMTransitionMixin, BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fsm_field = [
        'status',
    ]
    list_display = [
        'username',
        # 'name',
        'person',
        'status',
        'is_mc',
    ]
    list_select_related = [
        'person',
    ]

    autocomplete_fields = [
        'person',
    ]

    list_filter = (
        'status',
        'is_staff',
        MCUserListFilter,
    )

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'username',
                # 'name',
                'status',
                # 'email',
                'person',
                'is_mc',
                'is_staff',
                'created',
                'modified',
            )
        }),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': (
    #             'person',
    #         )
    #     }),
    # )
    search_fields = [
        'username',
        # 'name',
    ]
    inlines = [
        StateLogInline,
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
