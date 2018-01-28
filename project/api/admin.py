# Django
# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as AuthGroup

# Local
from .forms import (
    UserChangeForm,
    UserCreationForm,
)
from .inlines import (
    AppearanceInline,
    AssignmentInline,
    AwardInline,
    ContestantInline,
    ContestInline,
    ConventionInline,
    CompetitorInline,
    EnrollmentInline,
    EntryInline,
    GrantorInline,
    GridInline,
    GroupInline,
    MemberInline,
    OfficerInline,
    PanelistInline,
    ParticipantInline,
    RepertoryInline,
    RoundInline,
    ScoreInline,
    SessionInline,
    SongInline,
)
from .models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Competitor,
    Enrollment,
    Entry,
    Grantor,
    Grid,
    Group,
    Member,
    Office,
    Officer,
    Organization,
    Panelist,
    Participant,
    Person,
    Repertory,
    Round,
    Score,
    Session,
    Song,
    User,
    Venue,
)
from .filters import (
    OrganizationListFilter,
    ParentOrganizationListFilter,
    SessionOrganizationListFilter,
    ConventionOrganizationListFilter,
    DistrictListFilter,
    DivisionListFilter,
)


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
    raw_id_fields = (
        'competitor',
        'round',
    )
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

    raw_id_fields = (
        'convention',
        'person',
    )

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
        'organization',
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
        'organization',
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
        OrganizationListFilter,
    ]

    readonly_fields = [
        'id',
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'organization',
    ]

    ordering = (
        'organization__org_sort',
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

    raw_id_fields = [
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

    raw_id_fields = [
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
        'organization',
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
        'organization',
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
        ConventionOrganizationListFilter,
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

    raw_id_fields = [
        'organization',
        'venue',
    ]

    ordering = (
        '-year',
        '-season',
        'organization__org_sort',
        # 'organization__short_name',
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
        # ParticipantInline,
    ]

    search_fields = (
        'nomen',
    )

    raw_id_fields = (
        'session',
        'group',
    )

    readonly_fields = (
        'nomen',
    )

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'status',
        # 'start_date',
        # 'end_date',
        'organization',
        'person',
        'bhs_pk',
        'sub_status',
        'mem_status',
        'mem_code',
    ]
    list_display = [
        'nomen',
        # 'start_date',
        # 'end_date',
        'organization',
        'person',
        'sub_status',
        'mem_status',
        'mem_code',
        'status',
    ]
    raw_id_fields = [
        'person',
        'organization',
    ]
    search_fields = [
        'nomen',
    ]
    list_filter = [
        'status',
        # 'organization',
        'sub_status',
        'mem_status',
        'mem_code',
    ]
    readonly_fields = [
        'id',
        'sub_status',
        'mem_status',
        'mem_code',
    ]


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
        ParticipantInline,
        StateLogInline,
    ]

    search_fields = (
        'nomen',
    )

    raw_id_fields = (
        'session',
        'group',
    )

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
        'organization',
        'convention',
    ]
    list_display = [
        'nomen',
        'organization',
        'convention',
    ]

    readonly_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'organization',
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
    raw_id_fields = [
        'round',
        'competitor',
    ]
    ordering = [
        'num',
    ]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'id',
        'name',
        'status',
        'kind',
        'gender',
        'is_senior',
        ('bhs_id', 'bhs_pk',),
        'organization',
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
        'kind',
        'gender',
        DistrictListFilter,
        DivisionListFilter,
    ]

    search_fields = [
        'nomen',
    ]

    list_display = [
        'nomen',
        'kind',
        'gender',
        'organization',
        'location',
        'bhs_id',
        'bhs_pk',
        'status',
        'created',
        'modified',
    ]
    list_select_related = [
        'organization',
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

    raw_id_fields = [
        'organization',
    ]

    ordering = [
        'name',
    ]

    INLINES = {
        'Quartet': [
            MemberInline,
            RepertoryInline,
            EntryInline,
            CompetitorInline,
        ],
        'Chorus': [
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
        'is_admin',
        'sub_status',
        'mem_status',
        'mem_code',
    ]
    list_display = [
        'status',
        # 'start_date',
        # 'end_date',
        'group',
        'person',
        'part',
        'is_admin',
        'sub_status',
        'mem_status',
        'mem_code',
    ]
    raw_id_fields = [
        'person',
        'group',
    ]
    search_fields = [
        'nomen',
    ]
    list_filter = [
        'status',
        'part',
        'group__kind',
        'is_admin',
        'sub_status',
        'mem_status',
        'mem_code',
    ]
    readonly_fields = [
        'sub_status',
        'mem_status',
        'mem_code',
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
        'is_organization_manager',
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
        'is_organization_manager',
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
        'organization',
        'start_date',
        'end_date',
    ]

    list_display = [
        'nomen',
        'start_date',
        'end_date',
        'status',
    ]
    list_filter = [
        'status',
        'office',
        'organization',
    ]
    search_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'office',
        'person',
        'organization',
    ]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'name',
        'status',
        'kind',
        'parent',
        'code',
        'start_date',
        'end_date',
        'location',
        'mem_status',
        'bhs_id',
        'bhs_pk',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'img',
        'description',
        'notes',
    ]

    list_filter = [
        'status',
        'kind',
        'mem_status',
        ParentOrganizationListFilter,
    ]

    search_fields = [
        'nomen',
        'bhs_id',
        'code',
    ]

    list_display = [
        'nomen',
        'kind',
        'code',
        'bhs_id',
        'bhs_pk',
        'mem_status',
        'status',
    ]

    readonly_fields = [
        'id',
        'nomen',
        'mem_status',
    ]

    raw_id_fields = [
        'parent',
    ]

    ordering = (
        'org_sort',
        'name',
    )

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
        'Division': [
            AwardInline,
        ],
        'Chapter': [
            GroupInline,
            EnrollmentInline,
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

    raw_id_fields = (
        'round',
        'person',
    )

    readonly_fields = [
        'nomen',
    ]


@admin.register(Participant)
class ParticipantAdmin(FSMTransitionMixin, admin.ModelAdmin):

    fields = [
        'status',
        'entry',
        'person',
        'part',
    ]

    list_display = [
        'status',
        'entry',
        'person',
        'part',
    ]

    list_filter = (
        'status',
        'part',
    )

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'entry',
        'person',
    ]

    fsm_field = [
        'status',
    ]
    search_fields = [
        'nomen',
    ]

    ordering = (
        'nomen',
    )


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

    raw_id_fields = [
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

    raw_id_fields = (
        'group',
        'chart',
    )

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
        'oss_report_link',

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
        'oss_report_link',
        # 'session',
        # 'kind',
    ]

    raw_id_fields = (
        'session',
    )

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

    raw_id_fields = [
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
        # 'bbscores_report',
        # 'drcj_report',
        # 'admins_report',
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
        SessionOrganizationListFilter,
        'convention__season',
        'convention__year',
    )

    raw_id_fields = (
        'convention',
    )

    readonly_fields = [
        'id',
        'nomen',
        # 'bbscores_report',
        # 'drcj_report',
        # 'admins_report',
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
        'convention__organization__org_sort',
        # 'convention__organization__short_name',
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

    raw_id_fields = (
        'appearance',
        'chart',
    )

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
        'is_active',
        'is_staff',
        'status',
        'auth0_id',
    ]

    # list_editable = [
    #     'auth0_id',
    # ]

    list_display_links = [
        'person',
    ]

    list_filter = (
        'status',
        'is_active',
        'is_staff',
    )

    fieldsets = (
        (None, {
            'fields': (
                'status',
                'name',
                'email',
                'auth0_id',
                'is_active',
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
                'status',
                'name',
                'email',
                'auth0_id',
                'is_active',
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
        # 'name',
        # 'email',
        # 'auth0_id',
        'is_group_manager',
        'is_session_manager',
        'is_scoring_manager',
    ]


admin.site.unregister(AuthGroup)
