from django.contrib import admin

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from mptt.admin import MPTTModelAdmin
from fsm_admin.mixins import FSMTransitionMixin

from django_object_actions import (
    DjangoObjectActions,
    takes_instance_or_queryset,
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
    Panelist,
    Singer,
    Director,
    Session,
    Award,
    Performance,
    User,
    Organization,
)

# from grappelli.forms import GrappelliSortableHiddenMixin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin


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


# class PerformancesInline(GrappelliSortableHiddenMixin, admin.TabularInline):
class PerformancesInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_performance_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'contestant',
        'session',
        'position',
        'draw',
        # 'start',
    )
    sortable_field_name = "position"

    model = Performance
    extra = 0
    # raw_id_fields = (
    #     'contestant',
    # )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'contestant',
    #     ]
    # }
    readonly_fields = (
        'contestant',
        'session',
        'draw',
        # 'start',
        'link',
    )
    classes = ('grp-collapse grp-close',)


class PlacementInline(admin.TabularInline):
    fields = (
        'contestant',
        'session',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points',
        'place',
    )
    extra = 0
    model = Performance
    readonly_fields = (
        'contestant',
        'session',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points',
        'place',
    )
    ordering = (
        'place',
        'sng_points',
        'mus_points',
    )
    classes = ('grp-collapse grp-open',)


class ContestantsInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_contestant_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'contest',
        'group',
        'organization',
        'seed',
        'prelim',
        'place',
        'total_score',
        'men',
    )
    ordering = (
        'place',
        'seed',
        'group',
    )

    show_change_link = True

    model = Contestant
    extra = 0
    raw_id_fields = (
        # 'contest',
        'group',
    )
    readonly_fields = [
        'place',
        'total_score',
        'link',
    ]

    autocomplete_lookup_fields = {
        'fk': [
            # 'contest',
            'group',
        ]
    }
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class DirectorsInline(admin.TabularInline):
    fields = (
        'contestant',
        'person',
        'part',
    )
    ordering = (
        'part',
        'contestant',
    )
    model = Director
    extra = 0
    raw_id_fields = (
        'person',
        'contestant',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'person',
            'contestant',
        ]
    }
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class PanelistsInline(admin.TabularInline):
    model = Panelist
    fields = (
        'contest',
        'person',
        'organization',
        'category',
        'slot',
        # 'is_practice',
    )
    ordering = (
        'category',
        'slot',
    )
    extra = 0
    raw_id_fields = (
        'person',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'person',
        ]
    }
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-closed',)


class SongsInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_song_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'performance',
        'order',
        'tune',
        'mus_points',
        'prs_points',
        'sng_points',
    )
    ordering = (
        'performance',
        'order',
    )
    model = Song
    extra = 0
    raw_id_fields = (
        # 'performance',
        'tune',
    )
    autocomplete_lookup_fields = {
        'fk': [
            # 'performance',
            'tune',
        ]
    }

    readonly_fields = [
        'link',
    ]
    can_delete = True
    show_change_link = True


class ScoresInline(admin.TabularInline):
    model = Score
    fields = (
        'song',
        'panelist',
        'category',
        'points',
        'status',
    )
    ordering = (
        'panelist',
    )
    extra = 0
    raw_id_fields = (
        'panelist',
    )
    readonly_fields = [
        'category',
        'panelist',
    ]

    autocomplete_lookup_fields = {
        'fk': [
            'panelist',
        ]
    }
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-open',)


class SongsStackedInline(SuperInlineModelAdmin, admin.StackedInline):
    fields = (
        'performance',
        'order',
        'status',
        'tune',
        # 'mus_points',
        # 'prs_points',
        # 'sng_points',
    )
    ordering = (
        'performance',
        'order',
    )
    model = Song
    extra = 0
    raw_id_fields = (
        # 'performance',
        'tune',
    )
    autocomplete_lookup_fields = {
        'fk': [
            # 'performance',
            'tune',
        ]
    }
    inlines = (
        ScoresInline,
    )
    show_change_link = True
    classes = ('grp-collapse grp-open',)


class PerformancesStackedInline(SuperInlineModelAdmin, admin.StackedInline):
    fields = (
        'contestant',
        'session',
    )
    model = Performance
    extra = 0
    # raw_id_fields = (
    #     'contestant',
    # )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'contestant',
    #     ]
    # }
    readonly_fields = (
        'contestant',
        'session',
        # 'start',
    )
    inlines = (
        SongsStackedInline,
    )
    classes = ('grp-collapse grp-closed',)


class SessionsInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_session_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'contest',
        'kind',
        'start',
        'slots',
    )
    ordering = (
        'contest',
        'kind',
    )

    model = Session
    extra = 0
    # raw_id_fields = (
    #     'contest',
    # )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'contest',
    #     ]
    # }
    classes = ('grp-collapse grp-closed',)
    readonly_fields = [
        'link',
    ]


class SingersInline(admin.TabularInline):
    model = Singer
    fields = (
        'contestant',
        'person',
        'part',
    )
    ordering = (
        'part',
        'contestant',
    )
    extra = 0
    raw_id_fields = (
        'person',
        # 'contestant',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'person',
            # 'contestant',
        ]
    }
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-closed',)


@admin.register(Arranger)
class ArrangerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'catalog',
        'person',
    ]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    pass


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
    # class ContestAdmin(DjangoObjectActions, admin.MoadelAdmin):
    # @takes_instance_or_queryset
    # def build_contest(self, request, queryset):
    #     for obj in queryset:
    #         obj.build_contest()
    # build_contest.label = 'Build Contest'

    # @takes_instance_or_queryset
    # def draw_contest(self, request, queryset):
    #     for obj in queryset:
    #         obj.draw_contest()
    # draw_contest.label = 'Draw Contest'

    # @takes_instance_or_queryset
    # def start_contest(self, request, queryset):
    #     for obj in queryset:
    #         obj.start_contest()
    # start_contest.label = 'Start Contest'

    # @takes_instance_or_queryset
    # def end_contest(self, request, queryset):
    #     for obj in queryset:
    #         obj.end_contest()
    # end_contest.label = 'End Contest'

    # objectactions = [
    #     'build_contest',
    #     'draw_contest',
    #     'start_contest',
    #     'end_contest',
    # ]
    fsm_field = [
        'state',
    ]

    inlines = [
        ContestantsInline,
        SessionsInline,
        PanelistsInline,
    ]

    change_list_template = "admin/change_list_filter_sidebar.html"
    # change_list_filter_template = "admin/filter_listing.html"
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
        'panel',
        'scoresheet_pdf',
    )

    fields = (
        'name',
        'state',
        ('status', 'status_monitor',),
        ('history', 'history_monitor',),
        'convention',
        'organization',
        'level',
        'kind',
        'goal',
        'year',
        ('rounds', 'panel',),
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
class ContestantAdmin(DjangoObjectActions, admin.ModelAdmin):
    @takes_instance_or_queryset
    def update_contestants(self, request, queryset):
        for obj in queryset:
            obj.denorm()
    update_contestants.label = 'Update Contestants'

    change_list_template = "admin/change_list_filter_sidebar.html"

    objectactions = [
        'update_contestants',
    ]

    inlines = [
        SingersInline,
        DirectorsInline,
        PerformancesInline,
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
        'contest__level',
        'contest__kind',
        'contest__year',
    )

    raw_id_fields = (
        'contest',
        'group',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'contest',
            'group',
        ]
    }
    fields = (
        'name',
        ('status', 'status_monitor',),
        'contest',
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
        ('start', 'end',),
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
        'contest__level',
        'contest__kind',
        'contest__year',
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
class Performance(SuperModelAdmin):
    save_on_top = True
    change_list_template = "admin/change_list_filter_sidebar.html"

    inlines = [
        SongsStackedInline,
    ]
    list_display = [
        'name',
        'status',
        'draw',
        'start',
        'total_score',
        'place',
    ]
    list_filter = [
        'status',
        'session',
        'contestant__contest__level',
        'contestant__contest__kind',
        'contestant__contest__year',
    ]

    fields = [
        'name',
        ('status', 'status_monitor',),
        'session',
        'contestant',
        ('draw', 'start',),
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    ]

    readonly_fields = [
        'name',
        'status_monitor',
        'session',
        'contestant',
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
        'session',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'contestant',
            'session',
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
        ScoresInline,
    ]

    list_filter = (
        'status',
        'performance__contestant__contest__level',
        'performance__contestant__contest__kind',
        'performance__contestant__contest__year',
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
        ('start', 'end',),
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
        'song__performance__session__contest__level',
        'song__performance__session__contest__kind',
        'song__performance__session__contest__year',
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
class Session(DjangoObjectActions, admin.ModelAdmin):
    @takes_instance_or_queryset
    def end_session(self, request, queryset):
        for obj in queryset:
            obj.end_session()
    end_session.label = 'End Session'

    objectactions = [
        'end_session',
    ]

    save_on_top = True
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = [
        'name',
        'status',
        'start',
        'slots',
    ]
    fields = [
        'name',
        ('status', 'status_monitor',),
        ('contest', 'kind',),
        ('start', 'slots',),
    ]

    readonly_fields = [
        'name',
        'status_monitor',
        'contest',
        'kind',
    ]

    list_filter = (
        'status',
        'contest__level',
        'contest__kind',
        'contest__year',
    )

    raw_id_fields = (
        'contest',
    )

    autocomplete_lookup_fields = {
        'fk': [
            'contest',
        ]
    }

    inlines = [
        PerformancesInline,
        PlacementInline,
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
