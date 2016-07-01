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
    SessionInline,
    SubmissionInline,
)
from .models import (
    Award,
    Certification,
    Chapter,
    Chart,
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
        'level',
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
        'stix_num',
        'stix_name',
    ]

    list_display = [
        'name',
        'status',
        'is_manual',
        'kind',
        'championship_season',
        'qualifier_season',
        'size',
        'size_range',
        'scope',
        'scope_range',
        'is_improved',
        'is_novice',
        'idiom',
        'championship_rounds',
        'stix_name',
    ]

    list_filter = [
        'status',
        'is_manual',
        'level',
        'kind',
        'championship_season',
        'qualifier_season',
        'size',
        'scope',
        'organization',
        'is_primary',
        'is_novice',
        'is_improved',
    ]

    readonly_fields = [
        # 'name',
        'level',
    ]

    search_fields = [
        'name',
    ]

    ordering = (
        'level',
        'organization__name',
        'kind',
        '-is_primary',
        'is_improved',
        'size',
        'scope',
        'is_novice',
        'idiom',
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'category',
        'date',
        'person',
    ]

    list_display = [
        'name',
        'status',
        'category',
        'date',
        'person',
    ]

    list_filter = [
        'status',
        'category',
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


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'title',
        'arranger',
        'composer',
        'lyricist',
        'bhs_id',
        ('is_medley', 'is_generic',),
    ]

    list_display = [
        'name',
        'status',
        'title',
        'arranger',
        'bhs_id',
    ]

    list_filter = [
        'status',
    ]

    readonly_fields = [
        'name',
    ]

    search_fields = [
        'title',
    ]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'code',
    )

    list_display = (
        'name',
        'organization',
        'code',
        'status',
        'bhs_id',
    )

    list_filter = (
        'organization',
        'status',
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
        'code',
        'name',
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
        'stix_num',
        'stix_name',
    ]

    list_display = (
        'name',
        'session',
        # 'location',
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
        'champion',
    ]

    raw_id_fields = [
        'award',
        'session',
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


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):

    fsm_field = [
        'status',
    ]

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'bhs_id',
        'status',
        'kind',
        'level',
        'season',
        'date',
        # 'location',
    )

    fields = (
        'name',
        'status',
        'venue',
        'kind',
        'organization',
        'bhs_id',
        'is_prelims',
        'risers',
        'date',
        'year',
        'level',
        'season',
        'drcj',
        'stix_file',
    )

    list_filter = (
        'status',
        'organization',
        'year',
        'level',
        'season',
    )

    inlines = [
        SessionInline,
    ]

    readonly_fields = (
        'name',
        # 'year',
        'level',
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
        'name',
        'chapter__name',
        'bhs_id',
    )

    list_display = (
        'name',
        'chapter',
        'bhs_id',
        'status',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
    )

    fields = (
        'name',
        'status',
        'kind',
        ('age', 'is_novice',),
        'organization',
        'bhs_id',
        'chapter',
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


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'status',
        'session',
        'certification',
        'organization',
        ('category', 'kind',),
    ]

    list_display = [
        'name',
        'status',
        'certification',
        'organization',
    ]

    list_filter = (
        'status',
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
    list_display = [
        'name',
        'chapter',
        'person',
        'status',
    ]

    raw_id_fields = [
        'chapter',
        'person',
    ]


@admin.register(Organization)
class OrganizationAdmin(MPTTModelAdmin):
    fields = [
        'name',
        'status',
        'parent',
        'kind',
        'code',
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
        'short_name',
        'long_name',
        'status',
        'kind',
    ]

    inlines = [
        AwardInline,
        # OrganizationInline,
    ]

    raw_id_fields = [
        'representative',
    ]


@admin.register(Performance)
class PerformanceAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True

    list_display = [
        'name',
        'status',
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

    fields = [
        'name',
        'status',
        'performer',
        'num',
    ]

    readonly_fields = [
        'name',
    ]

    raw_id_fields = (
        'performer',
    )

    search_fields = (
        'name',
    )


@admin.register(Performer)
class PerformerAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    inlines = [
        PerformanceInline,
        ContestantInline,
        SubmissionInline,
    ]

    list_display = (
        'name',
        'status',
        'prelim',
        'men',
    )

    list_filter = [
        'status',
        'session__convention__year',
        'session__convention__organization',
        'session__convention__season',
        'session__kind',
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

    fields = (
        'name',
        'status',
        'bhs_id',
        'session',
        'group',
        'representing',
        ('is_evaluation', 'is_private',),
        ('tenor', 'lead', 'baritone', 'bass',),
        ('director', 'codirector', 'men'),
        'prelim',
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
    search_fields = (
        'name',
    )

    save_on_top = True
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
        # 'bhs_id',
        'bhs_name',
        'bhs_city',
        'bhs_state',
        'bhs_phone',
        'bhs_email',
    )

    fields = (
        'name',
        'common_name',
        'status',
        'organization',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'bhs_id',
        'picture',
        'description',
        'bhs_city',
        'notes',
    )

    list_filter = [
        'status',
    ]

    inlines = [
        RoleInline,
        MemberInline,
        CertificationInline,
    ]
    readonly_fields = [
        'common_name',
    ]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'date',
        'group',
        'person',
        'part',
        'bhs_file',
    ]

    list_display = [
        'name',
        'status',
        'date',
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
    fsm_field = [
        'status',
    ]

    save_on_top = True
    list_display = [
        'name',
        'status',
    ]
    fields = [
        'name',
        'status',
        ('session', 'kind',),
        'mt',
        'date',
    ]

    readonly_fields = [
        'name',
        'session',
        'kind',
    ]

    list_filter = [
        'status',
        'session__convention__year',
        'session__convention__organization',
        'session__convention__season',
        'session__kind',
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
    save_on_top = True
    fields = [
        'name',
        # 'status',
        'song',
        'judge',
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
        'date',
        'primary',
        'current',
        'cursor',
        'entry_form',
        'song_list',
        # 'year',
        # # 'size',
        'scoresheet_pdf',
    ]

    list_display = [
        'name',
        'status',
        'convention',
        'kind',
        'song_list',
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


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'status',
        'performer',
        'chart',
    ]

    list_display = [
        'name',
        'status',
        'performer',
        'chart',
    ]

    list_filter = (
        'status',
    )

    raw_id_fields = (
        'performer',
        'chart',
    )

    readonly_fields = [
        'name',
    ]


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


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'name',
        # 'status',
        # 'title',
        'submission',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points'
    )

    search_fields = (
        'name',
    )

    fields = [
        'name',
        # 'status',
        'performance',
        'submission',
        'num',
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
        # 'title',
    ]

    inlines = [
        ScoreInline,
    ]

    # list_filter = (
    #     'status',
    # )

    readonly_fields = (
        'name',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points',
        'mus_score',
        'prs_score',
        'sng_score',
        'total_score',
    )
    raw_id_fields = (
        'performance',
        'submission',
    )

    ordering = (
        'name',
        'num',
    )


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
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
