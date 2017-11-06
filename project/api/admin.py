# Django
# Third-Party
from django_fsm_log.models import StateLog
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
    EntryInline,
    GrantorInline,
    GroupInline,
    MemberInline,
    OfficerInline,
    PanelistInline,
    ParticipantInline,
    RepertoryInline,
    RoundInline,
    ScoreInline,
    SessionInline,
    SlotInline,
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
    Entry,
    Grantor,
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
    Slot,
    Song,
    User,
    Venue,
)


@admin.register(Appearance)
class AppearanceAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        'status',
        'actual_start',
        'actual_finish',
        'entry',
        'round',
        'var_pdf',
        'num',
        'draw',
        'slot',
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
        'nomen',
    ]

    raw_id_fields = (
        'entry',
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
        'name',
        'status',
        'organization',
        'kind',
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
        'level',
        'season',
        'rounds',
        'is_primary', 'is_invitational', 'is_manual',
        'status',
    ]

    list_editable = [
        'name',
        'organization',
        'kind',
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
        'season',
        'is_primary', 'is_invitational', 'is_manual',
        'organization',
    ]

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'organization__org_sort',
        'kind',
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
        'is_qualifier',
        'is_primary',
        'kind',
    ]

    list_display = (
        'nomen',
        'session',
    )

    list_filter = [
        'status',
        'kind',
        'award__kind',
        'award__is_primary',
        'is_qualifier',
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
class ConventionAdmin(admin.ModelAdmin):

    fields = (
        'name',
        'status',
        'organization',
        'year',
        'season',
        'panel',
        'venue',
        'open_date',
        'close_date',
        'start_date',
        'end_date',
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
        'status',
        'season',
        'organization',
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
        'organization__short_name',
    )

    save_on_top = True


@admin.register(Entry)
class EntryAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = (
        'status',
        'is_archived',
        'session',
        'group',
        'image',
        'csa_pdf',
        ('tot_points', 'mus_points', 'per_points', 'sng_points',),
        ('tot_score', 'mus_score', 'per_score', 'sng_score',),
        ('is_evaluation', 'is_private',),
        'draw',
        'prelim',
        'seed',
        'directors',
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
        ContestantInline,
        ParticipantInline,
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


@admin.register(Grantor)
class GrantorAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'organization',
        'session',
    ]
    list_display = [
        'nomen',
        'organization',
        'session',
    ]

    readonly_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'organization',
        'session',
    ]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'status',
        'kind',
        ('is_bhs', 'bhs_id', 'bhs_pk',),
        'organization',
        'code',
        # 'start_date',
        # 'end_date',
        'short_name',
        'location',
        'email',
        'phone',
        # 'spots',
        'website',
        'facebook',
        'twitter',
        'image',
        'description',
        'notes',
    ]

    list_filter = [
        'status',
        'is_bhs',
        'kind',
        'organization',
    ]

    search_fields = [
        'nomen',
        'short_name',
    ]

    list_display = [
        'nomen',
        # 'start_date',
        # 'end_date',
        # 'code',
        # 'short_name',
        'kind',
        'organization',
        'location',
        'is_bhs',
        'bhs_id',
        'bhs_pk',
        'status',
    ]

    list_editable = [
        'bhs_id',
        'bhs_pk',
        'organization',
        'kind',
        'location',
        'status',
    ]

    inlines = [
        MemberInline,
        RepertoryInline,
        EntryInline,
    ]
    # quartet_inlines = [
    #     # AwardInline,
    #     RepertoryInline,
    #     OfficerInline,
    #     # EntryInline,
    #     MemberInline,
    # ]
    # other_inlines = [
    #     AwardInline,
    #     RepertoryInline,
    #     OfficerInline,
    #     # EntryInline,
    #     # MemberInline,
    # ]

    readonly_fields = [
        'nomen',
    ]

    # raw_id_fields = [
    #     'organization',
    # ]

    ordering = [
        'name',
    ]

    # def get_inline_instances(self, request, obj=None):
    #     inline_instances = []
    #
    #     if obj.kind == obj.KIND.quartet:
    #         inlines = self.quartet_inlines
    #     else:
    #         inlines = self.other_inlines
    #
    #     for inline_class in inlines:
    #         inline = inline_class(self.model, self.admin_site)
    #         inline_instances.append(inline)
    #     return inline_instances
    #
    # def get_formsets(self, request, obj=None):
    #     for inline in self.get_inline_instances(request, obj):
    #         yield inline.get_formset(request, obj)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    fields = [
        'status',
        # 'start_date',
        # 'end_date',
        'group',
        'person',
        'part',
        'is_admin',
    ]
    list_display = [
        'status',
        # 'start_date',
        # 'end_date',
        'group',
        'person',
        'part',
        'is_admin',
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
        'name',
        'status',
        'parent',
        'kind',
        'code',
        'start_date',
        'end_date',
        'short_name',
        'location',
        'bhs_id',
        # 'spots',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'image',
        'description',
        'notes',
    ]

    list_filter = [
        'status',
        'kind',
    ]

    search_fields = [
        'nomen',
        'short_name',
    ]

    list_display = [
        'nomen',
        'kind',
        # 'start_date',
        # 'end_date',
        'code',
        'short_name',
        'bhs_id',
        'status',
    ]

    list_editable = [
        'bhs_id',
    ]
    inlines = [
        OfficerInline,
        AwardInline,
        GroupInline,
        ConventionInline,
    ]

    # quartet_inlines = [
    #     # AwardInline,
    #     RepertoryInline,
    #     OfficerInline,
    #     # EntryInline,
    #     MemberInline,
    # ]
    # other_inlines = [
    #     AwardInline,
    #     RepertoryInline,
    #     OfficerInline,
    #     # EntryInline,
    #     # MemberInline,
    # ]

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'parent',
    ]

    ordering = (
        'org_sort',
        'name',
    )

    # def get_inline_instances(self, request, obj=None):
    #     inline_instances = []
    #
    #     if obj.kind == obj.KIND.quartet:
    #         inlines = self.quartet_inlines
    #     else:
    #         inlines = self.other_inlines
    #
    #     for inline_class in inlines:
    #         inline = inline_class(self.model, self.admin_site)
    #         inline_instances.append(inline)
    #     return inline_instances
    #
    # def get_formsets(self, request, obj=None):
    #     for inline in self.get_inline_instances(request, obj):
    #         yield inline.get_formset(request, obj)


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
        'name',
        'status',
        'email',
        'is_deceased',
        'is_bhs',
        'bhs_id',
        'bhs_pk',
        'is_current',
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
    ]

    list_display = [
        'nomen',
        'email',
        'is_bhs',
        'bhs_id',
        'bhs_pk',
        'current_through',
        'part',
        'gender',
        'status',
    ]

    list_filter = [
        'status',
        'is_bhs',
        'is_current',
        'gender',
        'part',
        'is_deceased',
    ]

    readonly_fields = [
        'nomen',
        'email',
        'is_current',
        'current_through',
    ]

    fsm_field = [
        'status',
    ]

    search_fields = (
        'nomen',
        'email',
    )

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
class RoundAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        'status',
        ('session', 'kind', 'num'),
        'ann_pdf',

    ]

    list_display = [
        'nomen',
        'status',
    ]

    list_filter = [
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
        # 'session',
        # 'kind',
    ]

    raw_id_fields = (
        'session',
    )

    inlines = [
        AppearanceInline,
        PanelistInline,
        SlotInline,
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
        'status',
        'is_archived',
        'convention',
        'kind',
        'is_invitational',
        ('open_date', 'close_date'),
        ('start_date', 'end_date'),
        'scoresheet',
        'bbscores',
        'drcj_report',
        'admin_emails',
    ]

    list_display = [
        'nomen',
        'open_date',
        'close_date',
        'start_date',
        'end_date',
        'status',
        'kind',
        'is_invitational',
        'status',
    ]

    list_filter = (
        'is_archived',
        'status',
        'kind',
        'is_invitational',
        'convention__organization',
        'convention__season',
        'convention__year',
    )

    raw_id_fields = (
        'convention',
    )

    readonly_fields = [
        'nomen',
        'open_date',
        'close_date',
        'start_date',
        'end_date',
    ]

    inlines = [
        RoundInline,
        EntryInline,
        ContestInline,
        GrantorInline,
    ]

    list_select_related = [
        'convention',
    ]

    ordering = (
        '-convention__year',
        '-convention__season',
        'convention__organization__org_sort',
        'convention__organization__short_name',
        'kind',
    )

    search_fields = [
        'nomen',
    ]


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        # 'name',
        'status',
        'num',
        'onstage',
        'round',
    ]
    list_display = [
        'nomen',
        'status',
        'onstage',
    ]

    # list_editable = [
    #     'onstage',
    # ]

    list_filter = (
        'status',
    )

    readonly_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'round',
    ]

    ordering = [
        'num',
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
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        'name',
        'email',
        'person',
        'is_active',
        'is_staff',
    ]

    list_filter = (
        'is_active',
        'is_staff',
    )

    fieldsets = (
        (None, {'fields': ('name', 'email', 'auth0_id', 'is_active', 'is_staff', 'person', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('person', )}),
    )

    search_fields = [
        'email',
        'name',
    ]
    ordering = ('email',)
    filter_horizontal = ()
    raw_id_fields = [
        'person',
    ]

    readonly_fields = [
        'name',
        'email',
        'auth0_id',
    ]


@admin.register(StateLog)
class StateLogAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'by',
    ]
    fields = [
        'timestamp',
        'content_type',
        'content_object',
        'transition',
        'by',
        'object_id',
    ]
    readonly_fields = [
        'content_object',
        'timestamp',
        'by',
        'state',
        'transition',
        'content_type',
        'object_id',
    ]


admin.site.unregister(AuthGroup)
