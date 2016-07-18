# Third-Party
from fsm_admin.mixins import FSMTransitionMixin
from mptt.admin import MPTTModelAdmin

# Django
from django.contrib import admin

# Local
from .inlines import (
    AwardInline,
    CertificationInline,
    ContestantInline,
    ContestInline,
    ConventionInline,
    GroupInline,
    JudgeInline,
    MemberInline,
    PerformanceInline,
    PerformerInline,
    RoleInline,
    RoundInline,
    ScoreInline,
    SongInline,
    SessionInline,
    SubmissionInline,
)
from .models import (
    Award,
    Certification,
    Catalog,
    Chapter,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Member,
    Organization,
    Performance,
    Performer,
    Person,
    Role,
    Round,
    Score,
    Session,
    Slot,
    Song,
    Submission,
    User,
    Venue,
)


# from django_fsm_log.models import StateLog


# @admin.register(StateLog)
# class StateLogAdmin(admin.ModelAdmin):
#     pass


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'is_manual',
        'organization',
        'kind',
        'championship_season',
        'qualifier_season',
        'size',
        'size_range',
        'scope',
        'scope_range',
        'idiom',
        ('is_primary', 'is_improved', 'is_novice'),
        ('is_multi', 'is_qualification_required',),
        'championship_rounds',
        'qualifier_rounds',
        'threshold',
        'minimum',
        'advance',
    ]

    list_display = [
        'name',
        'status',
        'is_manual',
        'kind',
        'size',
        'size_range',
        'scope',
        'scope_range',
        'is_improved',
        'is_novice',
        'idiom',
        'championship_season',
        'qualifier_season',
    ]

    list_filter = [
        'status',
        'is_primary',
        'organization__level',
        'kind',
        'championship_season',
        'qualifier_season',
        'size',
        'scope',
        'is_manual',
        'is_novice',
        'is_improved',
        'organization',
    ]

    readonly_fields = [
        'name',
        'stix_num',
        'stix_name',
    ]

    search_fields = [
        'name',
    ]

    ordering = (
        'organization__level',
        'organization__name',
        'kind',
        '-is_primary',
        'is_improved',
        'size',
        'scope',
        'is_novice',
        'idiom',
    )


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'bhs_id',
        'title',
        'published',
        'arranger',
        'arranger_fee',
        'difficulty',
        'gender',
        'tempo',
        'is_medley',
        'is_learning',
        'voicing',
    ]

    list_display = [
        'name',
        'arranger',
        'status',
    ]

    list_filter = [
        'status',
    ]

    readonly_fields = [
        'name',
    ]

    search_fields = [
        'name',
    ]

    ordering = (
        'name',
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'category',
        'kind',
        'start_date',
        'end_date',
        'person',
    ]

    list_display = [
        'name',
        'category',
        'kind',
        'status',
    ]

    list_filter = [
        'status',
        'category',
        'kind',
    ]

    readonly_fields = [
        'name',
    ]

    raw_id_fields = [
        'person',
    ]

    search_fields = [
        'name',
    ]

    ordering = (
        'name',
    )


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    search_fields = (
        'nomen',
    )

    list_display = (
        'name',
        'code',
        'organization',
        'status',
    )

    list_filter = (
        'status',
        'organization',
    )

    fields = (
        'name',
        'status',
        'organization',
        'code',
        'bhs_id',
    )

    inlines = [
        GroupInline,
        MemberInline,
    ]

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'status',
        'award',
        'session',
        'champion',
        'cycle',
        'is_qualifier',
        'num_rounds',
    ]

    list_display = (
        'name',
        'session',
    )

    list_filter = [
        'status',
        'cycle',
        'award__is_primary',
        'award__organization__level',
        'award__organization',
        'award__kind',
        'is_qualifier',
    ]

    save_on_top = True

    inlines = [
        ContestantInline,
    ]

    readonly_fields = [
        'name',
        'cycle',
    ]

    raw_id_fields = [
        'award',
        'session',
        'champion',
    ]

    search_fields = [
        'name',
    ]


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'performer',
        'contest',
    ]

    list_filter = (
        'status',
    )

    readonly_fields = [
        'name',
    ]

    raw_id_fields = [
        'performer',
        'contest',
    ]

    search_fields = [
        'name',
    ]

    ordering = (
        'name',
    )


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):

    fields = (
        'name',
        'status',
        'kind',
        'level',
        'organization',
        'venue',
        'bhs_id',
        'is_prelims',
        'risers',
        'start_date',
        'end_date',
        'year',
        'season',
        'drcj',
    )

    list_display = (
        'name',
        'status',
        'start_date',
        'end_date',
        'venue',
    )

    list_filter = (
        'status',
        'level',
        'kind',
        'season',
        'organization',
        'year',
    )

    fsm_field = [
        'status',
    ]

    search_fields = (
        'name',
    )

    inlines = [
        SessionInline,
    ]

    readonly_fields = (
        'name',
    )

    raw_id_fields = [
        'drcj',
        'venue',
    ]

    ordering = (
        '-year',
        'level',
        'organization__name',
    )

    save_on_top = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = (
        'nomen',
    )

    fields = (
        'name',
        'status',
        'kind',
        ('age', 'is_novice',),
        'bhs_id',
        'start_date',
        'end_date',
        'chapter',
        'district',
        'division',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        'notes',
    )

    list_display = (
        'name',
        'status',
        'district',
        'division',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
    )

    list_filter = (
        'kind',
        'status',
    )

    inlines = [
        RoleInline,
        PerformerInline,
    ]

    raw_id_fields = [
        'chapter',
    ]

    save_on_top = True

    ordering = (
        'name',
    )


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'status',
        'category',
        'kind',
        'slot',
        'bhs_id',
        'session',
        'certification',
        'organization',
    ]

    list_display = [
        'name',
        'status',
        'kind',
        'category',
        'certification',
        'organization',
    ]

    list_filter = (
        'status',
        'category',
        'kind',
    )

    list_select_related = [
        'organization',
        'session',
        'certification',
    ]

    raw_id_fields = (
        'session',
        'certification',
    )

    readonly_fields = [
        'name',
    ]

    inlines = [
        ScoreInline,
    ]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'chapter',
        'person',
        'start_date',
        'end_date',
    ]

    list_display = [
        'name',
        'status',
        'start_date',
        'end_date',
    ]

    list_filter = [
        'status',
    ]

    raw_id_fields = [
        'chapter',
        'person',
    ]

    ordering = (
        'name',
    )

    search_fields = [
        'name',
    ]


@admin.register(Organization)
class OrganizationAdmin(MPTTModelAdmin):
    fields = [
        'name',
        'status',
        'parent',
        'level',
        'kind',
        'code',
        'start_date',
        'end_date',
        'short_name',
        'long_name',
        'location',
        'representative',
        'spots',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        'notes',
    ]

    list_filter = [
        'status',
        'level',
        'kind',
    ]

    list_display = [
        'name',
        'status',
        'code',
        'short_name',
        'long_name',
        'level',
        'kind',
    ]

    inlines = [
        AwardInline,
        # OrganizationInline,
    ]

    raw_id_fields = [
        'representative',
    ]

    readonly_fields = [
        'level',
    ]


@admin.register(Performance)
class PerformanceAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'name',
        'status',
        'actual_start',
        'actual_finish',
        'performer',
        'round',
        'num',
        'slot',
    ]

    list_display = [
        'name',
        'status',
        'performer',
        'round',
        'num',
    ]

    list_filter = [
        'status',
        'round__session__convention__year',
        'round__session__convention__organization',
        'round__session__convention__season',
        'round__session__kind',
        'round',
    ]

    fsm_field = [
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'name',
    ]

    raw_id_fields = (
        'performer',
    )

    search_fields = (
        'name',
    )

    inlines = [
        SongInline,
    ]


@admin.register(Performer)
class PerformerAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = (
        'name',
        'status',
        'bhs_id',
        'picture',
        'csa_pdf',
        'session',
        'group',
        'district',
        'division',
        'risers',
        ('is_evaluation', 'is_private',),
        ('tenor', 'lead', 'baritone', 'bass',),
        ('director', 'codirector', 'men'),
        'prelim',
        'seed',
    )

    list_display = (
        'name',
        'status',
        'prelim',
        'men',
        'risers',
    )

    list_filter = [
        'status',
        'risers',
        'session__convention__year',
        'session__convention__organization',
        'session__convention__season',
        'session__kind',
    ]

    fsm_field = [
        'status',
    ]

    inlines = [
        PerformanceInline,
        ContestantInline,
        SubmissionInline,
    ]

    search_fields = (
        'name',
    )

    raw_id_fields = (
        'session',
        'group',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'director',
        'codirector',
    )

    readonly_fields = (
        'name',
    )

    save_on_top = True

    ordering = (
        'name',
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'common_name',
        'status',
        'kind',
        'birth_date',
        'start_date',
        'end_date',
        'dues_thru',
        'mon',
        'spouse',
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'postal_code',
        # 'organization',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'bhs_id',
        'picture',
        'description',
        'notes',
    )

    list_display = (
        'name',
        'status',
        'bhs_id',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
    )

    list_filter = [
        'status',
    ]

    inlines = [
        RoleInline,
        MemberInline,
        CertificationInline,
    ]

    search_fields = (
        'nomen',
    )

    save_on_top = True

    readonly_fields = [
        'common_name',
    ]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'start_date',
        'end_date',
        'group',
        'person',
        'part',
    ]

    list_display = [
        'name',
        'status',
        'start_date',
        'end_date',
        'group',
        'person',
        'part',
    ]

    list_filter = [
        'status',
        'group__kind',
    ]

    readonly_fields = [
        'name',
    ]

    search_fields = [
        'name',
    ]

    raw_id_fields = (
        'group',
        'person',
    )


@admin.register(Round)
class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'name',
        'status',
        ('session', 'kind',),
        'num_songs',
        'mt',
        'start_date',
        'end_date',
        'ann_pdf',
    ]

    list_display = [
        'name',
        'status',
    ]

    list_filter = [
        'status',
        'session__convention__year',
        'session__convention__organization',
        'session__convention__season',
        'session__kind',
    ]

    fsm_field = [
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'name',
        'session',
        'kind',
    ]

    raw_id_fields = (
        'session',
        'mt',
    )

    inlines = [
        PerformanceInline,
    ]

    search_fields = [
        'name',
    ]


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    fields = [
        'name',
        # 'status',
        'song',
        'judge',
        'category',
        'kind',
        'original',
        'violation',
        'penalty',
        'points',
    ]

    readonly_fields = [
        'name',
        'song',
        'judge',
    ]

    list_display = [
        'name',
        # 'status',
        'points',
    ]

    # list_filter = [
    #     'status',
    # ]

    raw_id_fields = [
        'song',
        'judge',
    ]

    ordering = [
        'song',
        'judge',
    ]
    save_on_top = True


@admin.register(Session)
class SessionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True
    fields = [
        'name',
        'status',
        'convention',
        'kind',
        'num_rounds',
        'start_date',
        'end_date',
        'primary',
        'current',
        # 'cursor',
        # 'year',
        # # 'size',
        'scoresheet_pdf',
    ]

    list_display = [
        'name',
        'status',
        'convention',
        'kind',
        # 'size',
        # 'championship_rounds',
    ]

    list_filter = (
        'status',
        'kind',
        'convention__year',
        'convention__level',
        'convention__organization',
        'convention__season',
    )

    raw_id_fields = (
        'convention',
        'current',
        'primary',
    )

    readonly_fields = [
        'name',
    ]

    inlines = [
        RoundInline,
        PerformerInline,
        JudgeInline,
        ContestInline,
    ]

    list_select_related = [
        'convention',
    ]

    ordering = (
        '-convention__year',
        'convention__level',
        'convention__organization__name',
        '-convention__season',
        'kind',
    )


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'status',
        'num',
        'onstage',
        'round',
    ]
    readonly_fields = [
        'name',
    ]
    raw_id_fields = [
        'round',
    ]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = [
        'name',
        # 'status',
        'performance',
        'submission',
        'num',

        # 'title',
    ]

    list_display = (
        'name',
        # 'status',
        # 'title',
        'submission',
        'num',
    )

    # list_filter = (
    #     'status',
    # )

    search_fields = (
        'name',
    )

    inlines = [
        ScoreInline,
    ]
    save_on_top = True

    readonly_fields = (
        'name',
    )

    raw_id_fields = (
        'performance',
        'submission',
    )

    ordering = (
        'name',
        'num',
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'status',
        'performer',
        'title',
        'arranger',
        'source',
        'is_medley',
        'is_parody',
    ]

    list_display = [
        'name',
        'status',
        'title',
        'arranger',
        'performer',
    ]

    list_filter = (
        'status',
        'performer',
    )

    raw_id_fields = (
        'performer',
    )

    readonly_fields = [
        'name',
    ]


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
        'status',
        'location',
        'city',
        'state',
        'airport',
        'timezone',
    )

    list_display = [
        'name',
        'location',
        'city',
        'state',
        'timezone',
    ]

    list_filter = (
        'status',
    )

    search_fields = (
        'name',
    )

    readonly_fields = [
        'name',
    ]

    inlines = [
        ConventionInline,
    ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    save_on_top = True
