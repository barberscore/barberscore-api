from django.contrib import admin

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from super_inlines.admin import SuperInlineModelAdmin


from .models import (
    Contestant,
    Song,
    Contest,
    Score,
    Judge,
    Singer,
    Panel,
    Director,
    Session,
    Performance,
    Ranking,
)


# class PerformancesInline(GrappelliSortableHiddenMixin, admin.TabularInline):
class PerformanceInline(admin.TabularInline):
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
        'status',
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
        'draw',
        # 'start',
        'link',
    )
    classes = ('grp-collapse grp-closed',)


class PlacementInline(admin.TabularInline):
    fields = (
        'contestant',
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


class PanelInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_panel_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'name',
        'status',
        'convention',
        'kind',
        'size',
        'rounds',
    )
    show_change_link = True

    model = Panel
    extra = 0
    raw_id_fields = (
        'convention',
    )
    readonly_fields = [
        'link',
        'name',
    ]

    can_delete = True
    classes = ('grp-collapse grp-closed',)


class ContestInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_contest_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'name',
        'panel',
        'organization',
        'level',
        'kind',
        'goal',
        'year',
        'rounds',
        'qual_score',
    )
    show_change_link = True

    model = Contest
    extra = 0
    raw_id_fields = (
        'panel',
    )
    readonly_fields = [
        'link',
        'name',
    ]

    can_delete = True
    classes = ('grp-collapse grp-closed',)


class ContestantInline(admin.TabularInline):
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
        # 'convention',
        # 'panel',
        'group',
        'organization',
        'seed',
        'prelim',
        'place',
        'total_score',
        'men',
    )
    ordering = (
        # 'convention',
        'group__kind',
        'group',
    )

    show_change_link = True

    model = Contestant
    extra = 0
    raw_id_fields = (
        # 'convention',
        # 'panel',
        'group',
    )
    readonly_fields = [
        'place',
        'total_score',
        'link',
    ]

    autocomplete_lookup_fields = {
        'fk': [
            # 'panel',
            'group',
        ]
    }
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class RankingInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_ranking_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'name',
        'contest',
        'contestant',
        'place',
        'total_score',
    )
    ordering = (
        'place',
    )

    show_change_link = True

    model = Ranking
    extra = 0
    raw_id_fields = (
        'contestant',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'contestant',
        ]
    }
    readonly_fields = [
        'link',
        'name',
        'total_score',
    ]
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class DirectorInline(admin.TabularInline):
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


class JudgeInline(admin.TabularInline):
    model = Judge
    fields = (
        'panel',
        'person',
        'organization',
        'kind',
        'slot',
        # 'is_practice',
    )
    ordering = (
        'kind',
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


class ScoreInline(admin.TabularInline):
    model = Score
    fields = (
        'song',
        'judge',
        'kind',
        'points',
        'status',
    )
    ordering = (
        'judge',
    )
    extra = 0
    raw_id_fields = (
        'song',
    )
    readonly_fields = [
        'kind',
    ]

    autocomplete_lookup_fields = {
        'fk': [
            'song',
        ]
    }
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-open',)


class SongStackedInline(SuperInlineModelAdmin, admin.StackedInline):
    fields = (
        'performance',
        'order',
        'status',
        'title',
        # 'tune',
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
        ScoreInline,
    )
    show_change_link = True
    classes = ('grp-collapse grp-open',)


class PerformanceStackedInline(SuperInlineModelAdmin, admin.StackedInline):
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
        SongStackedInline,
    )
    classes = ('grp-collapse grp-closed',)


class SessionInline(admin.TabularInline):
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
        'panel',
        'kind',
        'status',
        'start_date',
        'num',
        'slots',
    )
    ordering = (
        'panel',
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


class SingerInline(admin.TabularInline):
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


# class SongInline(admin.TabularInline):
#     def link(self, obj):
#         return mark_safe(
#             "<a href={0}>link</a>".format(
#                 reverse(
#                     'admin:api_song_change',
#                     args=(
#                         obj.id.hex,
#                     )
#                 )
#             )
#         )

#     fields = (
#         'link',
#         'performance',
#         'order',
#         'tune',
#         'mus_points',
#         'prs_points',
#         'sng_points',
#     )
#     ordering = (
#         'performance',
#         'order',
#     )
#     model = Song
#     extra = 0
#     raw_id_fields = (
#         # 'performance',
#         'tune',
#     )
#     autocomplete_lookup_fields = {
#         'fk': [
#             # 'performance',
#             'tune',
#         ]
#     }

#     readonly_fields = [
#         'link',
#     ]
#     can_delete = True
#     show_change_link = True
