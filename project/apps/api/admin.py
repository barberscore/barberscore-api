from django.contrib import admin

import datetime

from mptt.admin import MPTTModelAdmin
from fsm_admin.mixins import FSMTransitionMixin

from .inlines import (
    ArrangerInline,
    AwardInline,
    CertificationInline,
    ContestInline,
    ContestantInline,
    SessionInline,
    PerformerInline,
    PerformerStackedInline,
    DirectorInline,
    GroupInline,
    JudgeInline,
    PerformanceInline,
    ScoreInline,
    RoundInline,
    RankingInline,
    SingerInline,
    SongStackedInline,
    OrganizationInline,
)

from .models import (
    Arranger,
    Award,
    Catalog,
    Chapter,
    Contest,
    Contestant,
    Session,
    Performer,
    Convention,
    Group,
    Judge,
    Organization,
    Performance,
    Person,
    Score,
    Round,
    Song,
    Tune,
    User,
)

import arrow

# from grappelli.forms import GrappelliSortableHiddenMixin
from super_inlines.admin import SuperModelAdmin


@admin.register(Arranger)
class ArrangerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'catalog',
        'person',
    ]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = [
        'name',
        'organization',
        'kind',
        'size',
        'is_improved',
        'idiom',
        'num_rounds',
        'season',
        'stix_name',
    ]

    list_filter = [
        'status',
        'kind',
        'organization',
    ]


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = [
        'song_name',
        'tune',
        'bhs_id',
        'bhs_songname',
        'bhs_arranger',
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
        'bhs_name',
        'bhs_group_name',
        'bhs_group_id',
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
        'bhs_group_id',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        'code',
        'notes',
    )

    inlines = [
        GroupInline,
    ]

    save_on_top = True


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_filter = [
        'status',
        'cycle',
        'award__kind',
        'award__season',
    ]

    save_on_top = True

    inlines = [
        ContestantInline,
    ]

    readonly_fields = [
        'is_qualifier',
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
        'award',
        'place',
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
        'place',
        'total_score',
    ]

    raw_id_fields = [
        'performer',
    ]


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):

    def human_range(self, obj):
        if obj.date:
            if obj.date.upper - obj.date.lower == datetime.timedelta(1):
                dates = "{0}".format(
                    arrow.get(obj.date.lower).format('MMMM D, YYYY'),
                )
            else:
                dates = "{0} - {1}".format(
                    arrow.get(obj.date.lower).format('MMMM D'),
                    arrow.get(obj.date.upper).format('MMMM D, YYYY'),
                )
        else:
            dates = obj.date
        return dates
    human_range.short_description = "Dates22"

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
        'kind',
        'division',
        # 'date',
        'human_range',
        # 'location',
    )

    fields = (
        'name',
        'status',
        # 'stix_name',
        # 'stix_div',
        ('location', 'timezone',),
        # 'dates',
        'date',
        'year',
        'organization',
        'drcj',
        'kind',
        # 'stix_file',
        'division',
    )

    list_filter = (
        'status',
        'kind',
        'year',
        'organization__level',
        'division',
        'organization',
    )

    inlines = [
        SessionInline,
        # OrganizationInline,
    ]

    readonly_fields = (
        'name',
        'year',
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
        'group_id',
    )

    list_display = (
        'name',
        'chapter',
        'group_id',
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
        'organization',
        (
            'is_quartet',
            'is_chorus',
            'is_collegiate',
            'is_senior',
            'is_youth',
            'is_novice',
        ),
        'group_id',
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


    # ordering = [
    #     'tree_id',
    # ]


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
        'draw',
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
        ('draw', 'scheduled'),
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
        'draw',
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
        SingerInline,
        DirectorInline,
        PerformanceInline,
        ContestantInline,
    ]

    list_display = (
        'name',
        'status',
        'seed',
        'prelim',
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
        ('seed', 'prelim',),
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
        'member',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'bhs_member_id',
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
        'member',
        'picture',
        'description',
        'bhs_city',
        'notes',
    )

    list_filter = [
        'status',
    ]

    inlines = [
        DirectorInline,
        SingerInline,
        ArrangerInline,
        CertificationInline,
    ]


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
        ('history', 'history_monitor',),
        'convention',
        'kind',
        'administrator',
        # 'organization',
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
        # 'size',
        # 'num_rounds',
    ]

    list_filter = (
        'status',
        'history',
        'kind',
        'convention__year',
        'organization',
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
        'history_monitor',
        'organization',
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


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    list_display = (
        'name',
        # 'status',
        # 'title',
        'tune',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points'
    )

    search_fields = (
        'name',
        'tune__name',
    )

    fields = [
        'name',
        # 'status',
        'order',
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
        # 'title',
        'tune',
        # 'catalog',
    ]

    inlines = [
        # ArrangersInline,
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
        # 'tune',
        # 'catalog',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'performance',
            # 'tune',
        ]
    }

    ordering = (
        'name',
        'order',
    )


@admin.register(Tune)
class TuneAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    save_on_top = True
