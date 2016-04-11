from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from fsm_admin.mixins import FSMTransitionMixin
from grappelli_autocomplete_fk_edit_link import AutocompleteEditLinkAdminMixin

from .inlines import (
    AssistantInline,
    AwardInline,
    CertificationInline,
    ContestInline,
    ContestantInline,
    SessionInline,
    PerformerInline,
    GroupInline,
    JudgeInline,
    MemberInline,
    ParticipantInline,
    PerformanceInline,
    ScoreInline,
    RoundInline,
    RoleInline,
    SongStackedInline,
    OrganizationInline,
    SubmissionInline,
)

from .models import (
    Assistant,
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

# from django_fsm_log.models import StateLog


# @admin.register(StateLog)
# class StateLogAdmin(admin.ModelAdmin):
#     pass


@admin.register(Assistant)
class AssistantAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"

    fields = [
        'name',
        'status',
        'kind',
        'person',
        'session',
        'organization',
    ]

    list_display = [
        'name',
        'status',
        'person',
        'session',
        'organization',
    ]

    list_filter = [
        'status',
        'kind',
    ]

    readonly_fields = [
        'name',
    ]

    search_fields = [
        'name',
    ]

    raw_id_fields = [
        'session',
        'person',
    ]

    ordering = (
        'session',
        'person',
        'organization',
    )


@admin.register(Award)
class AwardAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"

    fields = [
        'name',
        'status',
        'is_manual',
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

    list_display = [
        'name',
        'status',
        'is_manual',
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
        'is_manual',
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

    readonly_fields = [
        'name',
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
class CertificationAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"

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

    autocomplete_lookup_fields = {
        'fk': [
            'person',
        ]
    }


@admin.register(Chart)
class ChartAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"

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
class ChapterAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
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
class ContestAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
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
        'champion',
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
        'cycle',
        'is_qualifier',
    ]

    raw_id_fields = [
        'award',
        'session',
    ]

    autocomplete_lookup_fields = {
        'fk': [
            'award',
            'session',
        ]
    }


@admin.register(Contestant)
class ContestantAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"

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
            'contest',
        ]
    }

    readonly_fields = [
        'name',
        'rank',
        'total_score',
    ]

    raw_id_fields = [
        'performer',
        'contest',
    ]

    search_fields = [
        'name',
    ]


@admin.register(Convention)
class ConventionAdmin(AutocompleteEditLinkAdminMixin, FSMTransitionMixin, admin.ModelAdmin):

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
        ParticipantInline,
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

    autocomplete_lookup_fields = {
        'fk': [
            'drcj',
            'venue',
        ]
    }

    ordering = (
        '-year',
        'level',
        'organization__name',
    )

    save_on_top = True


@admin.register(Group)
class GroupAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
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
class JudgeAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    fields = [
        'name',
        'status',
        'session',
        'person',
        'organization',
        ('category', 'kind',),
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
class MemberAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
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

    autocomplete_lookup_fields = {
        'fk': [
            'chapter',
            'person',
        ]
    }


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
class PerformanceAdmin(AutocompleteEditLinkAdminMixin, FSMTransitionMixin, SuperModelAdmin):
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
        ('slot', 'scheduled', 'actual'),
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
class PerformerAdmin(AutocompleteEditLinkAdminMixin, FSMTransitionMixin, admin.ModelAdmin):
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

    autocomplete_lookup_fields = {
        'fk': [
            'session',
            'group',
            'tenor',
            'lead',
            'baritone',
            'bass',
            'director',
            'codirector',
        ]
    }
    fields = (
        'name',
        'status',
        'session',
        ('group', 'organization',),
        ('tenor', 'lead', 'baritone', 'bass',),
        ('men', 'director', 'codirector',),
        # ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        # ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    )

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

    save_on_top = True

    ordering = (
        'name',
    )


@admin.register(Person)
class PersonAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
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
class RoleAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"

    fields = [
        'name',
        'status',
        'date',
        'group',
        'person',
    ]

    list_display = [
        'name',
        'status',
        'date',
        'group',
        'person',
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

    raw_id_fields = (
        'group',
        'person',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'group',
            'person',
        ]
    }


@admin.register(Round)
class RoundAdmin(AutocompleteEditLinkAdminMixin, FSMTransitionMixin, admin.ModelAdmin):
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
class ScoreAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
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
class SessionAdmin(AutocompleteEditLinkAdminMixin, FSMTransitionMixin, SuperModelAdmin):
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
        'date',
        'administrator',
        'aca',
        'cutoff',
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
        'convention__level',
        'convention__organization',
        'convention__season',
    )

    raw_id_fields = (
        'convention',
        'administrator',
        'aca',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'convention',
            'administrator',
            'aca',
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
        AssistantInline,
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
class SubmissionAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
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

    autocomplete_lookup_fields = {
        'fk': [
            'performer',
            'chart',
        ]
    }

    readonly_fields = [
        'name',
    ]


@admin.register(Song)
class SongAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
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
        'performance',
        'chart',
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
        'chart',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'performance',
            'chart',
        ]
    }

    ordering = (
        'name',
        'order',
    )


@admin.register(Venue)
class VenueAdmin(AutocompleteEditLinkAdminMixin, admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
        'location',
        'city',
        'state',
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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    save_on_top = True
