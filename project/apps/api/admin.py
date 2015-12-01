from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from fsm_admin.mixins import FSMTransitionMixin

from .inlines import (
    ContestantInline,
    DirectorInline,
    PerformanceInline,
    ContestInline,
    # PlacementInline,
    PanelInline,
    PanelistInline,
    ScoreInline,
    SongStackedInline,
    # SongInline,
    SingerInline,
    SessionInline,
    RankingInline,
)

from .models import (
    Arranger,
    Catalog,
    Convention,
    Contest,
    Contestant,
    Group,
    Tune,
    Person,
    Song,
    Score,
    Panel,
    Panelist,
    Session,
    Performance,
    User,
    Organization,
    Ranking,
)

# from grappelli.forms import GrappelliSortableHiddenMixin
from super_inlines.admin import SuperModelAdmin


# class ArrangersInline(admin.TabularInline):
#     model = Arranger
#     fields = (
#         'song',
#         'person',
#         'part',
#         # 'is_practice',
#     )
#     ordering = (
#         'person',
#     )
#     extra = 0
#     raw_id_fields = (
#         'person',
#     )
#     autocomplete_lookup_fields = {
#         'fk': [
#             'person',
#         ]
#     }
#     can_delete = True
#     show_change_link = True
#     classes = ('grp-collapse grp-closed',)


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]
    autocomplete_lookup_fields = {
        'fk': [
            'contestant',
        ]
    }
    raw_id_fields = [
        'contestant',
    ]


@admin.register(Panel)
class PanelAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    fields = [
        'name',
        ('status', 'status_monitor',),
        'convention',
        'kind',
        'size',
        'rounds',
    ]

    list_display = [
        'name',
        'status',
        'convention',
        'kind',
        'size',
        'rounds',
    ]

    raw_id_fields = (
        'convention',
    )

    readonly_fields = [
        'name',
        'status_monitor',
    ]

    inlines = [
        SessionInline,
    ]


@admin.register(Arranger)
class ArrangerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'catalog',
        'person',
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


@admin.register(Contest)
class ContestAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    inlines = [
        RankingInline,
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
    )

    list_display = (
        'name',
        'status',
        'history',
        'goal',
        'rounds',
        'scoresheet_pdf',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        ('history', 'history_monitor',),
        'convention',
        'organization',
        'level',
        'kind',
        'goal',
        'year',
        'rounds',
        'scoresheet_pdf',
    )

    readonly_fields = (
        'name',
        'status_monitor',
        'history_monitor',
    )

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
class ContestantAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    change_list_template = "admin/change_list_filter_sidebar.html"

    inlines = [
        SingerInline,
        DirectorInline,
        PerformanceInline,
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
        'place',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'status',
    )

    raw_id_fields = (
        'convention',
        'group',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'convention',
            'group',
        ]
    }
    fields = (
        'name',
        ('status', 'status_monitor',),
        'convention',
        ('group', 'organization',),
        ('seed', 'prelim',),
        ('place', 'men',),
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


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'status',
        'status_monitor',
        'location',
        'dates',
        'kind',
        'year',
        'organization',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        ('location', 'timezone',),
        'dates',
        'organization',
        'kind',
        'year',
    )

    list_filter = (
        'status',
        'kind',
        'year',
        'organization',
    )

    inlines = [
        ContestInline,
        PanelInline,
        ContestantInline,
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
    )

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
        'chapter_name',
        'chapter_code',
        'picture',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        'kind',
        ('start_date', 'end_date',),
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        ('chapter_name', 'chapter_code',),
        'notes',
    )

    list_filter = (
        'kind',
    )

    readonly_fields = (
        'status_monitor',
    )
    save_on_top = True


@admin.register(Panelist)
class Panelist(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    fields = [
        'name',
        ('status', 'status_monitor',),
        'contest',
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
        'contest',
        'person',
    ]

    raw_id_fields = (
        'contest',
        'person',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'contest',
            'person',
        ]
    }

    readonly_fields = [
        'name',
    ]


@admin.register(Organization)
class Organization(MPTTModelAdmin):
    pass


@admin.register(Performance)
class Performance(FSMTransitionMixin, SuperModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True
    change_list_template = "admin/change_list_filter_sidebar.html"

    inlines = [
        SongStackedInline,
        # SessionInline,
    ]
    list_display = [
        'name',
        'status',
        'draw',
        'start_time',
        'total_score',
        'place',
    ]
    list_filter = [
        'status',
    ]

    fields = [
        'name',
        ('status', 'status_monitor',),
        'contestant',
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
        'contestant',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'contestant',
        ]
    }

    search_fields = (
        'name',
    )


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
        'judge',
        'organization',
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

    readonly_fields = (
        'status_monitor',
    )
    # inlines = [
    #     DirectorsInline,
    #     SingersInline,
    #     PanelistsInline,
    # ]


@admin.register(Score)
class Score(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    save_on_top = True
    fields = [
        'name',
        ('status', 'status_monitor',),
        'song',
        'panelist',
        'points',
    ]

    readonly_fields = [
        'name',
        'status_monitor',
        'song',
        'panelist',
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
        'panelist',
    ]

    autocomplete_lookup_fields = {
        'fk': [
            'song',
            'panelist',
        ]
    }

    ordering = [
        'panelist',
        'song',
    ]


@admin.register(Session)
class Session(FSMTransitionMixin, admin.ModelAdmin):
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
        ('panel', 'kind',),
        ('start_date', 'slots',),
    ]

    readonly_fields = [
        'name',
        'status_monitor',
        'panel',
        'kind',
    ]

    list_filter = (
        'status',
    )

    raw_id_fields = (
        'panel',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'panel',
        ]
    }

    inlines = [
        PerformanceInline,
        # PlacementInline,
    ]

    search_fields = [
        'name',
    ]


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
