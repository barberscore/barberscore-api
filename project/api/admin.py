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
from .filters import AwardQualifierLevelFilter
from .filters import ConventionGroupListFilter
from .filters import ConventionStatusListFilter
from .filters import DistrictListFilter
from .filters import GroupListFilter
from .filters import MCListFilter
from .filters import MCUserListFilter
from .filters import RoundGroupListFilter
from .filters import SessionConventionStatusListFilter
from .filters import SessionGroupListFilter
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import ActiveChapterInline
from .inlines import ActiveChorusInline
from .inlines import ActiveQuartetInline
from .inlines import AppearanceInline
from .inlines import AssignmentInline
from .inlines import AwardInline
from .inlines import ContenderInline
from .inlines import ContestantInline
from .inlines import ContestInline
from .inlines import ConventionInline
from .inlines import EntryInline
from .inlines import FlatInline
from .inlines import GridInline
from .inlines import GroupInline
from .inlines import MemberInline
from .inlines import OfficerInline
from .inlines import OutcomeInline
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
from .models import Flat
from .models import Complete
from .models import Contest
from .models import Contender
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Outcome
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Selection
from .models import Session
from .models import Song
from .models import User
from .models import Venue

admin.site.site_header = 'Barberscore Admin Backend'


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'complete',
        'selection',
        'score',
    ]
    list_display = [
        'id',
        'complete',
        'selection',
        'score',
    ]
    readonly_fields = [
        'id',
    ]
    autocomplete_fields = [
        'complete',
        'selection',
        'score',
    ]


@admin.register(Complete)
class CompleteAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'mark',
        'row',
        'year',
        'season_raw',
        'district_raw',
        'convention_raw',
        'session_raw',
        'round_raw',
        'category_raw',
        'season_kind',
        'convention_name',
        'session_kind',
        'round_kind',
        'category_kind',
        'panelist_name',
        'panelist_num',
        'points',
        'panelist',
    ]
    list_display = [
        'row',
        # 'mark',
        # 'convention_raw',
        'session_raw',
        'session_kind',
        # 'round_raw',
        # 'round_kind',
        # 'id',
        # 'category',
        # 'panelist_num',
        # 'panelist_name',
        # 'person',
        # 'num_appearances',
        # 'num_panelists',
        # 'points',
        # 'convention',
        # 'session',
        # 'round',
        # 'panelist',
    ]
    list_filter = [
        'year',
        'season_kind',
        'session_kind',
        'round_kind',
        'district_code',
    ]
    ordering = (
        'year',
        'district_code',
        'season_kind',
        'session_kind',
        'round_kind',
        'panelist_num',
    )
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'round',
    ]
    autocomplete_fields = [
        'panelist',
    ]
    inlines = [
        # FlatInline,
    ]


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'row',
        'season_raw',
        'year',
        'district_raw',
        'event_raw',
        'session_raw',
        'season_kind',
        'convention_name',
        'session_kind',
        'round_kind',
        'group_name',
        'appearance_num',
        'song_num',
        'song_title',
        'totals',
        'points',
        'song',
    ]
    list_display = [
        'row',
        # 'season_raw',
        # 'district_raw',
        # 'event_raw',
        # 'session_raw',
        # 'district_code',
        # 'event_raw',
        # 'convention',
        # 'event_raw',
        # 'session_raw',
        # 'session_kind',
        # 'session',
        'song',
        'song_num',
        # 'round_kind',
        # 'appearance_num',
        # 'song_num',
        # 'group_name',
        # 'song_title',
        # 'convention',
        # 'session',
        # 'round',
        # 'appearance',
        # 'totals',
        # 'points',
        # 'song',
    ]
    list_filter = [
        'year',
        # 'season_raw',
        # 'district_raw',
        # 'event_raw',
        # 'session_raw',
        'season_kind',
        'district_code',
        'session_kind',
        'round_kind',
    ]
    list_select_related = [
        'song',
    ]
    list_editable = [
        # 'convention_name',
    ]

    ordering = (
        'row',
        'appearance_num',
        'song_num',
    )
    readonly_fields = [
        'id',
    ]
    autocomplete_fields = [
        'song',
    ]
    search_fields = [
        'song',
    ]
    inlines = [
        # FlatInline,
    ]


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
        'gender',
        'division',
        'age',
        'level',
        'season',
        'is_single',
        'parent',
        ('threshold', 'minimum', 'advance', 'spots',),
        'description',
        'notes',
    ]

    list_display = [
        'name',
        # 'size',
        # 'scope',
        'group',
        'division',
        'kind',
        'age',
        'gender',
        'level',
        # 'size',
        # 'scope',
        # 'season',
        # 'rounds',
        # 'threshold',
        # 'advance',
        # 'minimum',
        'status',
    ]

    # list_editable = [
    #     'threshold',
    #     'advance',
    #     'minimum',
    # ]
    list_filter = [
        'status',
        'kind',
        'level',
        AwardQualifierLevelFilter,
        'division',
        'age',
        'gender',
        'season',
        'is_single',
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


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = (
        'id',
        'name',
        'legacy_name',
        'legacy_selection',
        'legacy_complete',
        'status',
        ('group', 'divisions'),
        'year',
        'season',
        'panel',
        'image',
        'location',
        'timezone',
        'venue',
        ('open_date', 'close_date',),
        ('start_date', 'end_date',),
        'description',
    )

    list_display = (
        'name',
        'location',
        'timezone',
        'start_date',
        'end_date',
        'year',
        'season',
        'status',
    )

    list_editable = [
        'location',
        'start_date',
        'end_date',
    ]

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
        'season',
        'group__tree_sort',
    )
    list_select_related = [
        'group',
    ]

    save_on_top = True


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
        'venue',
        'round',
        # 'appearance',
        'renditions',
    ]
    list_display = [
        'status',
        'onstage',
        'start',
    ]
    list_filter = (
        'status',
        'onstage',
        'period',
    )
    readonly_fields = [
    ]
    autocomplete_fields = [
        'round',
        'venue',
        # 'appearance',
    ]
    ordering = [
        'round',
        'period',
        'num',
    ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        try:
            timezone.activate(obj.venue.timezone)
        except AttributeError:
            pass
        return super().change_view(request, object_id, form_url, extra_context)


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
        'division',
        ('is_senior', 'is_youth',),
        ('bhs_id', 'mc_pk', 'code',),
        'parent',
        ('international', 'district', 'chapter',),
        'location',
        'email',
        'phone',
        'website',
        'facebook',
        'twitter',
        'image',
        'description',
        'participants',
        'notes',
        ('created', 'modified',),
    ]

    list_filter = [
        'status',
        MCListFilter,
        'kind',
        'gender',
        'is_senior',
        'is_youth',
        'division',
        DistrictListFilter,
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
        'is_senior',
        'is_youth',
        'division',
        'parent',
        'bhs_id',
        'code',
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

    actions = [
        # 'update_from_mc',
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
        'Chapter': [
            ActiveChorusInline,
            OfficerInline,
            StateLogInline,
        ],
        'Chorus': [
            OfficerInline,
            # MemberInline,
            RepertoryInline,
            # EntryInline,
            StateLogInline,
        ],
        'Quartet': [
            OfficerInline,
            MemberInline,
            RepertoryInline,
            EntryInline,
            StateLogInline,
        ],
        'VLQ': [
            OfficerInline,
            MemberInline,
            RepertoryInline,
            EntryInline,
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

    # def update_from_mc(self, request, queryset):
    #     Structure = apps.get_model('bhs.structure')
    #     i = 0
    #     for obj in queryset:
    #         try:
    #             structure = Structure.objects.get(
    #                 id=obj.mc_pk
    #             )
    #         except Structure.DoesNotExist:
    #             self.message_user(
    #                 request,
    #                 "{0} is not registered with Member Center".format(
    #                     obj.name,
    #                 ),
    #                 level=messages.ERROR,
    #             )
    #             continue
    #         structure.update_bs()
    #         i += 1
    #     if i == 1:
    #         message = "{0} group was updated.".format(i)
    #     elif i > 1:
    #         message = "{0} groups were updated.".format(i)
    #     elif i == 0:
    #         return
    #     self.message_user(
    #         request,
    #         message,
    #     )
    # update_from_mc.short_description = "Update from Member Center"


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
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
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
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
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
        'group__kind',
        'group__status',
        'part',
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
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
        'is_round_manager',
        'is_scoring_manager',
        'is_group_manager',
        'is_person_manager',
        'is_award_manager',
        'is_officer_manager',
        'is_chart_manager',
        'is_assignment_manager',
    ]

    list_display = [
        'name',
        'is_mc',
        'code',
        'kind',
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
        'is_round_manager',
        'is_scoring_manager',
        'is_group_manager',
        'is_person_manager',
        'is_award_manager',
        'is_officer_manager',
        'is_chart_manager',
        'is_assignment_manager',
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
    def office__code(self, instance):
        return "{0}".format(instance.office.code)

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
        'office',
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


@admin.register(Person)
class PersonAdmin(FSMTransitionMixin, admin.ModelAdmin):
    # Disable for use with MC
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    fields = [
        'id',
        'status',
        ('first_name', 'middle_name', 'last_name', 'nick_name',),
        'email',
        'is_deceased',
        'is_mc',
        'bhs_id',
        'mc_pk',
        'birth_date',
        'part',
        'gender',
        'spouse',
        'location',
        'district',
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
        'common_name',
        'email',
        'phone',
        # 'mc_pk',
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
        'common_name',
        'created',
        'modified',
    ]

    fsm_field = [
        'status',
    ]

    search_fields = [
        'last_name',
        'first_name',
        'nick_name',
        'bhs_id',
        'email',
    ]

    # autocomplete_fields = [
    #     'user',
    # ]

    save_on_top = True

    inlines = [
        MemberInline,
        OfficerInline,
        AssignmentInline,
        PanelistInline,
        StateLogInline,
    ]

    ordering = [
        'last_name',
        'first_name',
    ]
    # readonly_fields = [
    #     'common_name',
    # ]
    actions = [
        # 'update_from_mc',
    ]

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'

    # def update_from_mc(self, request, queryset):
    #     Human = apps.get_model('bhs.human')
    #     i = 0
    #     for obj in queryset:
    #         try:
    #             human = Human.objects.get(
    #                 id=obj.mc_pk
    #             )
    #         except Human.DoesNotExist:
    #             self.message_user(
    #                 request,
    #                 "{0} is not registered with Member Center".format(
    #                     obj.common_name,
    #                 ),
    #                 level=messages.ERROR,
    #             )
    #             continue
    #         human.update_bs()
    #         i += 1
    #     if i == 1:
    #         message = "{0} person was updated.".format(i)
    #     elif i > 1:
    #         message = "{0} persons were updated.".format(i)
    #     elif i == 0:
    #         return
    #     self.message_user(
    #         request,
    #         message,
    #     )
    # update_from_mc.short_description = "Update from Member Center"


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
        'id',
        'status',
        'oss',
        'sa',
        ('session', 'kind', 'num', 'spots',),
        'date',
        'footnotes',
    ]

    list_display = [
        '__str__',
        'status',
        'oss',
        'sa',
    ]


    list_filter = [
        SessionConventionStatusListFilter,
        'status',
        'kind',
        'session__kind',
        'session__convention__season',
        RoundGroupListFilter,
        'session__convention__year',
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
        # 'oss',
        # 'sa',
    ]

    autocomplete_fields = [
        'session',
    ]

    inlines = [
        PanelistInline,
        AppearanceInline,
        GridInline,
        OutcomeInline,
        StateLogInline,
    ]

    search_fields = [
        'session__convention__name',
    ]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide MyInline in the add view
            if isinstance(inline, GridInline):
                try:
                    timezone.activate(obj.session.convention.timezone)
                except AttributeError:
                    pass
            yield inline.get_formset(request, obj), inline


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
        'legacy_report',
        'drcj_report',
        'num_rounds',
        'is_invitational',
        'footnotes',
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
        SessionGroupListFilter,
        'convention__season',
        'convention__year',
    )

    autocomplete_fields = [
        'convention',
    ]

    readonly_fields = [
        'id',
        'legacy_report',
        'drcj_report',
    ]

    inlines = [
        ContestInline,
        EntryInline,
        RoundInline,
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
        'selection',
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
        'selection',
    )

    autocomplete_fields = [
        'appearance',
        'chart',
    ]

    ordering = (
        'num',
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
    ]

    def is_mc(self, instance):
        return instance.is_mc
    is_mc.boolean = True
    is_mc.short_description = 'Is Member Center'

admin.site.unregister(AuthGroup)
