from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from fsm_admin.mixins import FSMTransitionMixin

from .inlines import (
    ArrangerInline,
    ContestInline,
    CertificationInline,
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
    SingerInline,
    SongStackedInline,
)

from .models import (
    Arranger,
    Award,
    Contest,
    Catalog,
    Chapter,
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
        'get_long_name',
        'get_level',
        'kind',
        'long_name',
        'stix_name',
    ]

    list_filter = [
        'status',
        'kind',
        'organization',
        'is_championship',
    ]

    def get_long_name(self, obj):
        return obj.organization.long_name
    get_long_name.short_description = 'Org Name'
    get_long_name.admin_order_field = 'organization__long_name'

    def get_level(self, obj):
        return obj.organization.get_kind_display()
    get_level.short_description = 'Org Level'
    get_level.admin_order_field = 'organization__level'


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
    )

    list_display = (
        'name',
        # 'status',
        # 'status_monitor',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'code',
        'picture',
    )

    fields = (
        'name',
        # ('status', 'status_monitor',),
        ('start_date', 'end_date',),
        'organization',
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

    readonly_fields = (
        # 'status_monitor',
    )
    save_on_top = True


@admin.register(Contest)
class ContestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    inlines = [
        ContestantInline,
    ]

    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    search_fields = (
        'name',
    )

    list_filter = (
        'status',
        'history',
        'goal',
        'level',
        'kind',
        'year',
        'organization',
        'session',
        'award',
    )

    list_display = (
        'name',
        'status',
        'session',
        'award',
        'goal',
        # 'organization',
        # 'level',
        # 'kind',
        # 'year',
        # 'rounds',
        # 'qual_score',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        ('history', 'history_monitor',),
        'session',
        'award',
        'goal',
        'organization',
        'level',
        'kind',
        'year',
        'rounds',
        'qual_score',
    )

    readonly_fields = (
        'name',
        'status_monitor',
        'history_monitor',
    )

    # ordering = (
    #     '-year',
    #     '-tree_id',
    #     'level',
    #     'kind',
    #     'goal',
    # )

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "convention":
    #         try:
    #             parent_obj_id = request.resolver_match.args[0]
    #             obj = Contest.objects.get(pk=parent_obj_id)
    #             kwargs["queryset"] = Convention.objects.filter(year=obj.year)
    #         except IndexError:
    #             pass
    #     return super(ContestAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    search_fields = [
        'name',
    ]
    fields = [
        'name',
        ('status', 'status_monitor',),
        'performer',
        'contest',
        'place',
    ]
    list_filter = (
        'status',
        'contest__session__convention',
        'contest__session__convention__year',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'performer',
            'contest',
        ]
    }
    readonly_fields = [
        'name',
        'status_monitor',
        'place',
    ]

    raw_id_fields = [
        'performer',
        'contest',
    ]


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):

    def human_range(self, obj):
        try:
            dates = "{0} - {1}".format(
                arrow.get(obj.dates2.lower).format('MMMM D'),
                arrow.get(obj.dates2.upper).format('MMMM D, YYYY'),
            )
        except AttributeError:
            dates = obj.dates2
        return dates
    human_range.short_description = "Dates22"

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
        'human_range',
        'location',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        'stix_name',
        'stix_div',
        ('location', 'timezone',),
        'dates',
        'organization',
        'kind',
        'year',
        'stix_file',
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
        # ContestInline,
        SessionInline,
        # PerformerInline,
    ]

    readonly_fields = (
        'name',
        'status_monitor',
    )
    save_on_top = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'chapter__name',
    )

    list_display = (
        'name',
        'chapter',
        'status',
        'status_monitor',
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
        ('status', 'status_monitor',),
        'kind',
        ('start_date', 'end_date',),
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
    )

    inlines = [
        PerformerInline,
    ]

    readonly_fields = (
        'status_monitor',
    )

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
        ('status', 'status_monitor',),
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
        ('status', 'status_monitor',),
        'parent',
        'kind',
        'short_name',
        'long_name',
        ('start_date', 'end_date',),
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

    readonly_fields = [
        'status_monitor',
    ]

    list_display = [
        'name',
        'short_name',
        'long_name',
        'status',
        'kind',
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
        'start_time',
        'total_score',
    ]
    list_filter = [
        'status',
        'round',
    ]

    fields = [
        'name',
        ('status', 'status_monitor',),
        'performer',
        ('draw', 'start_time',),
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    ]

    readonly_fields = [
        'name',
        'status_monitor',
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
        'mus_score',
        'prs_score',
        'sng_score',
        'total_score',
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
        ('status', 'status_monitor',),
        'session',
        ('group', 'organization',),
        ('seed', 'prelim',),
        ('men',),
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    )

    readonly_fields = (
        'name',
        'status_monitor',
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
        'status_monitor',
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
        ('status', 'status_monitor',),
        'kind',
        ('start_date', 'end_date',),
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
        'notes',
    )

    list_filter = [
        'status',
    ]

    readonly_fields = (
        'status_monitor',
    )
    inlines = [
        DirectorInline,
        SingerInline,
        ArrangerInline,
        CertificationInline,
    ]


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    fields = [
        'name',
        ('status', 'status_monitor',),
        'song',
        'judge',
        'points',
    ]

    readonly_fields = [
        'name',
        'status_monitor',
        'song',
        'judge',
    ]

    list_display = [
        'name',
        'status',
        'points',
    ]

    list_filter = [
        'status',
    ]

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
        'judge',
        'song',
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
        ('status', 'status_monitor',),
        ('history', 'history_monitor',),
        'convention',
        'organization',
        'year',
        'kind',
        'size',
        'num_rounds',
    ]

    list_display = [
        'name',
        'status',
        'convention',
        'kind',
        'size',
        'num_rounds',
    ]

    list_filter = (
        'status',
        'history',
        'kind',
        'year',
        'organization',
    )

    raw_id_fields = (
        'convention',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'convention',
        ]
    }

    readonly_fields = [
        'name',
        'status_monitor',
        'history_monitor',
        'organization',
        'year',
    ]

    inlines = [
        RoundInline,
        JudgeInline,
        ContestInline,
        PerformerStackedInline,
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
        'start_date',
        'slots',
    ]
    fields = [
        'name',
        ('status', 'status_monitor',),
        ('session', 'kind',),
        ('start_date', 'slots',),
    ]

    readonly_fields = [
        'name',
        'status_monitor',
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
        # PlacementInline,
    ]

    search_fields = [
        'name',
    ]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    list_display = (
        'name',
        'status',
        'tune',
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
        ('status', 'status_monitor',),
        'order',
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
        'tune',
        'catalog',
    ]

    inlines = [
        # ArrangersInline,
        ScoreInline,
    ]

    list_filter = (
        'status',
    )

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
        'status_monitor',
    )
    raw_id_fields = (
        'performance',
        'tune',
        'catalog',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'performance',
            'tune',
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
