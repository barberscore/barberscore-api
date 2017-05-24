# Django
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
    EntryInline,
    MemberInline,
    OfficerInline,
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
    Entity,
    Entry,
    Member,
    Office,
    Officer,
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
        'num',
        'slot',
    ]

    list_display = [
        'nomen',
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

    fields = [
        'name',
        'status',
        'is_manual',
        'kind',
        'age',
        'season',
        # 'size',
        # 'size_range',
        # 'scope',
        # 'scope_range',
        ('is_primary', 'is_improved', 'is_novice'),
        ('is_multi',),
        'rounds',
        'threshold',
        'minimum',
        'advance',
    ]

    list_display = [
        'nomen',
        'status',
        'is_primary',
        'is_manual',
        'kind',
        'age',
        # 'size',
        # 'size_range',
        # 'scope',
        # 'scope_range',
        'is_improved',
        'is_novice',
        'season',
    ]

    list_filter = [
        'status',
        'is_primary',
        'kind',
        'age',
        'season',
        # 'size',
        # 'scope',
        'is_manual',
        'is_novice',
        'is_improved',
    ]

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'kind',
        'age',
        '-is_primary',
        'is_improved',
        'size',
        'scope',
        'is_novice',
    )


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):

    fields = [
        'nomen',
        'status',
        'bhs_id',
        'title',
        'composers',
        'lyricists',
        'arrangers',
        'holders',
        'entity',
        'published',
        'difficulty',
        'gender',
        'tempo',
        'is_medley',
        'is_learning',
        'voicing',
    ]

    list_display = [
        'nomen',
        'status',
        'title',
        'composers',
        'lyricists',
        'arrangers',
        'holders',
    ]

    # list_editable = [
    #     'title',
    #     'composers',
    #     'arrangers',
    #     'holders',
    # ]

    list_filter = [
        'status',
    ]

    inlines = [
        RepertoryInline,
    ]

    raw_id_fields = [
        'entity',
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
class ContestAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'award',
        'session',
        'is_qualifier',
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
class ContestantAdmin(admin.ModelAdmin):

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
        'entity',
        'level',
        'venue',
        'risers',
        'open_date',
        'close_date',
        'start_date',
        'end_date',
        'panel',
        'year',
        'season',
    )

    list_display = (
        'nomen',
        'name',
        'panel',
        'season',
        # 'status',
        'open_date',
        'close_date',
        'start_date',
        'end_date',
        'level',
        # 'venue',
    )

    list_filter = (
        'status',
        'level',
        'season',
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
        'entity',
        'venue',
    ]

    ordering = (
        '-year',
        'level',
    )

    save_on_top = True


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'status',
        'parent',
        'kind',
        'code',
        'start_date',
        'end_date',
        'short_name',
        'long_name',
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
    ]

    list_display = [
        'nomen',
        'status',
        'start_date',
        'end_date',
        'code',
        'short_name',
        'long_name',
        'kind',
        'bhs_id',
    ]

    list_editable = [
        'bhs_id',
    ]

    inlines = [
        # AwardInline,
        RepertoryInline,
        OfficerInline,
        # EntryInline,
        MemberInline,
    ]

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'parent',
    ]

    ordering = [
        'kind',
        'name',
    ]

    # def get_inline_instances(self, request, obj=None):
    #     inlines = [
    #         AwardInline,
    #         MemberInline,
    #         RepertoryInline,
    #         OfficerInline,
    #     ]


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    fields = (
        # 'name',
        'status',
        'bhs_id',
        'image',
        'session',
        'entity',
        'representing',
        # 'district',
        # 'division',
        'risers',
        ('is_evaluation', 'is_private',),
        ('tenor', 'lead', 'baritone', 'bass',),
        ('director', 'codirector', 'men'),
        'prelim',
        'seed',
    )

    list_display = (
        'nomen',
        'status',
    )

    list_filter = [
        'status',
        'session__convention__level',
        'session__kind',
        'session__convention__season',
        'session__convention__year',
        'risers',
    ]

    fsm_field = [
        'status',
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
        'entity',
        'representing',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'director',
        'codirector',
    )

    readonly_fields = (
        'nomen',
    )

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'start_date',
        'end_date',
        'entity',
        'person',
        'part',
    ]
    list_display = [
        'status',
        'start_date',
        'end_date',
        'entity',
        'person',
        'part',
    ]
    raw_id_fields = [
        'person',
        'entity',
    ]
    search_fields = [
        'nomen',
    ]
    list_filter = [
        'status',
        'part',
        'entity__kind',
    ]


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'short_name',
        'kind',
        'is_cj',
    ]
    search_fields = [
        'nomen',
        'short_name',
    ]

    list_filter = [
        'status',
        'kind',
        'is_cj',
    ]

    inlines = [
        OfficerInline,
    ]


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'office',
        'person',
        'entity',
    ]
    list_display = [
        'person',
        'office',
        'entity',
        'start_date',
        'end_date',
        'status',
    ]
    list_filter = [
        'office__is_cj',
    ]
    search_fields = [
        'nomen',
    ]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    fields = [
        'status',
        'entry',
        'member',
        'part',
    ]

    list_display = [
        'status',
        'entry',
        'member',
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
        'member',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'nomen',
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = [
        'name',
        # 'common_name',
        'status',
        'kind',
        'representing',
        'birth_date',
        'start_date',
        'end_date',
        'dues_thru',
        'part',
        'mon',
        'spouse',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'bhs_id',
        'image',
        'description',
        'notes',
    ]

    list_display = [
        'nomen',
        'status',
        'bhs_id',
        'part',
        'representing',
        'location',
        'website',
        'facebook',
        'twitter',
    ]

    list_filter = [
        'status',
        'part',
    ]

    readonly_fields = [
        'nomen',
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

    raw_id_fields = [
        'representing',
    ]
    # readonly_fields = [
    #     'common_name',
    # ]


@admin.register(Repertory)
class RepertoryAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'entity',
        'chart',
    ]

    list_display = [
        'nomen',
        'status',
        'entity',
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
        'entity',
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
        ('session', 'kind',),
        'num_songs',
        # 'mt',
        'start_date',
        'end_date',
    ]

    list_display = [
        'nomen',
        'status',
    ]

    list_filter = [
        'status',
        'session__kind',
        'session__convention__level',
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
        # 'mt',
    )

    inlines = [
        AppearanceInline,
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
        'person',
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
        'person',
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
        'person',
    ]

    ordering = [
        'song',
        'person',
    ]
    save_on_top = True


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True
    fields = [
        # 'name',
        'status',
        'convention',
        'kind',
        'age',
        'num_rounds',
        'panel_size',
        # 'start_date',
        # 'end_date',
        'primary',
        'current',
        # 'cursor',
        # 'year',
        # # 'size',
        'scoresheet',
    ]

    list_display = [
        'nomen',
        'status',
        'kind',
        'age',
    ]

    list_filter = (
        'status',
        'kind',
        'age',
        'convention__entity__kind',
        'convention__season',
        'convention__year',
    )

    raw_id_fields = (
        'convention',
        'current',
        'primary',
    )

    readonly_fields = [
        'nomen',
    ]

    inlines = [
        RoundInline,
        EntryInline,
        ContestInline,
    ]

    list_select_related = [
        'convention',
    ]

    ordering = (
        '-convention__year',
        'convention__level',
        '-convention__season',
        'kind',
        'age',
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

    list_filter = (
        'status',
    )

    readonly_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'round',
    ]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        # 'status',
        'appearance',
        'chart',
        'num',

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

    inlines = [
        # ConventionInline,
    ]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
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
        (None, {'fields': ('email', 'auth0_id', 'is_active', 'is_staff', 'person', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('person', )}),
    )

    search_fields = [
        'email',
    ]
    ordering = ('email',)
    filter_horizontal = ()
    raw_id_fields = [
        'person',
    ]

    readonly_fields = [
        'email',
        'auth0_id',
    ]

admin.site.unregister(AuthGroup)
