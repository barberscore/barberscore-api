from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from fsm_admin.mixins import FSMTransitionMixin

from .inlines import (
    AwardInline,
    CertificationInline,
    ContestInline,
    ContestantInline,
    SessionInline,
    PerformerInline,
    GroupInline,
    JudgeInline,
    MemberInline,
    PerformanceInline,
    ScoreInline,
    RoundInline,
    RoleInline,
    SongStackedInline,
    OrganizationInline,
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
    Submission,
    Song,
    User,
    Venue,
)

from super_inlines.admin import SuperModelAdmin


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = [
        'name',
        'status',
        'kind',
        'season',
        'size',
        'size_range',
        'scope',
        'scope_range',
        'is_improved',
        'is_novice',
        'idiom',
        'num_rounds',
        'stix_name',
    ]

    list_filter = [
        'status',
        'level',
        'kind',
        'season',
        'size',
        'scope',
        'organization',
        'is_primary',
        'is_novice',
        'is_improved',
    ]

    fields = [
        'name',
        'status',
        'organization',
        'level',
        'kind',
        'season',
        'size',
        'size_range',
        'scope',
        'scope_range',
        ('is_primary', 'is_improved', 'is_novice'),
        'idiom',
        'num_rounds',
        'cutoff',
        'minimum',
        # 'panel_size',
        'stix_num',
        'stix_name',
    ]

    readonly_fields = [
        'name',
        'level',
    ]


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    save_on_top = True


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
        'bhs_name',
        'bhs_group_name',
        'bhs_id',
        # 'location',
        # 'website',
        # 'facebook',
        # 'twitter',
        # 'email',
        # 'phone',
        # 'picture',
    )

    list_filter = (
        'organization',
        'status',
    )

    fields = (
        'name',
        'status',
        'organization',
        'bhs_name',
        'bhs_group_name',
        'bhs_id',
        'code',
    )

    inlines = [
        GroupInline,
        MemberInline,
    ]

    save_on_top = True


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_filter = [
        'status',
        'cycle',
        'award__is_primary',
        'award__organization__level',
        'award__kind',
        'is_qualifier',
    ]

    fields = [
        'name',
        'status',
        'award',
        'session',
        'cycle',
        'is_qualifier',
        'stix_num',
        'stix_name',
    ]

    save_on_top = True

    inlines = [
        ContestantInline,
    ]

    readonly_fields = [
        'name',
    ]


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    search_fields = [
        'name',
    ]
    fields = [
        'name',
        'status',
        'performer',
        'contest',
        'rank',
        'total_score',
    ]
    list_filter = (
        'status',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'performer',
        ]
    }
    readonly_fields = [
        'name',
        'rank',
        'total_score',
    ]

    raw_id_fields = [
        'performer',
    ]


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):

    fsm_field = [
        'status',
    ]

    change_list_template = "admin/change_list_filter_sidebar.html"
    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'status',
        'organization',
        'level',
        'division',
        'season',
        'date',
        'human_date',
        # 'location',
    )

    fields = (
        'name',
        'status',
        'venue',
        # 'dates',
        'date',
        'year',
        'organization',
        'level',
        'division',
        'season',
        'drcj',
        'stix_file',
    )

    list_filter = (
        'status',
        'organization',
        'year',
        'level',
        'division',
        'season',
    )

    inlines = [
        SessionInline,
        # OrganizationInline,
    ]

    readonly_fields = (
        'name',
        # 'year',
        'level',
        'human_date',
    )

    raw_id_fields = [
        'drcj',
    ]

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

    autocomplete_lookup_fields = {
        'fk': [
            'chapter',
        ]
    }

    save_on_top = True


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    fields = [
        'name',
        'status',
        'session',
        'person',
        'organization',
        ('category', 'slot',),
    ]

    list_display = [
        'name',
        'status',
        'person',
        'organization',
    ]

    list_filter = (
        'status',
    )

    list_select_related = [
        'organization',
        'session',
        'person',
    ]

    raw_id_fields = (
        'session',
        'person',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'session',
            'person',
        ]
    }

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
        OrganizationInline,
    ]


@admin.register(Performance)
class PerformanceAdmin(FSMTransitionMixin, SuperModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True
    change_list_template = "admin/change_list_filter_sidebar.html"

    inlines = [
        SongStackedInline,
        # RoundInline,
    ]
    list_display = [
        'name',
        'status',
        'slot',
        'total_score',
    ]
    list_filter = [
        'status',
        'round',
    ]

    fields = [
        'name',
        'status',
        'performer',
        ('slot', 'scheduled'),
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    ]

    readonly_fields = [
        'name',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points',
        'mus_score',
        'prs_score',
        'sng_score',
        'total_score',
    ]

    raw_id_fields = (
        'performer',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'performer',
        ]
    }

    search_fields = (
        'name',
    )


@admin.register(Performer)
class PerformerAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    change_list_template = "admin/change_list_filter_sidebar.html"

    inlines = [
        PerformanceInline,
        ContestantInline,
        SubmissionInline,
    ]

    list_display = (
        'name',
        'status',
        # 'mus_score',
        # 'prs_score',
        # 'sng_score',
        # 'total_score',
        'men',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'status',
    )

    raw_id_fields = (
        'session',
        'group',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'session',
            'group',
        ]
    }
    fields = (
        'name',
        'status',
        'session',
        ('group', 'organization',),
        ('men',),
        # ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        # ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    )

    readonly_fields = (
        'organization',
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

    save_on_top = True


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


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Round)
class RoundAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = [
        'name',
        'status',
    ]
    fields = [
        'name',
        'status',
        ('session', 'kind',),
    ]

    readonly_fields = [
        'name',
        'session',
        'kind',
    ]

    list_filter = (
        'status',
    )

    raw_id_fields = (
        'session',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'session',
        ]
    }

    inlines = [
        PerformanceInline,
    ]

    search_fields = [
        'name',
    ]


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
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

    autocomplete_lookup_fields = {
        'fk': [
            'song',
            'judge',
        ]
    }

    ordering = [
        'song',
        'judge',
    ]


@admin.register(Session)
class SessionAdmin(FSMTransitionMixin, SuperModelAdmin):
    fsm_field = [
        'status',
    ]

    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    fields = [
        'name',
        'status',
        'convention',
        'kind',
        'administrator',
        'entry_form',
        'song_list',
        # 'year',
        # # 'size',
        # 'num_rounds',
    ]

    list_display = [
        'name',
        'status',
        'convention',
        'kind',
        'administrator',
        'song_list',
        # 'size',
        # 'num_rounds',
    ]

    list_filter = (
        'status',
        'kind',
        'convention__year',
        'convention',
    )

    raw_id_fields = (
        'convention',
        'administrator',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'convention',
        ]
    }

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


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'status',
        'performer',
        'chart',
    ]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    list_display = (
        'name',
        # 'status',
        # 'title',
        'chart',
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
        'order',
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
        'order',
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
    )
    autocomplete_lookup_fields = {
        'fk': [
            'performance',
        ]
    }

    ordering = (
        'name',
        'order',
    )


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
        'timezone',
    )

    search_fields = (
        'name',
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    save_on_top = True
