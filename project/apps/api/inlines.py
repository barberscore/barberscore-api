from django.contrib import admin

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from super_inlines.admin import SuperInlineModelAdmin


from .models import (
    Arranger,
    Award,
    Certification,
    Competitor,
    Contest,
    Contestant,
    Director,
    Judge,
    Performance,
    Score,
    Session,
    Singer,
    Song,
)


class ArrangerInline(admin.TabularInline):
    model = Arranger
    fields = (
        'song',
        'person',
        'part',
        # 'is_practice',
    )
    ordering = (
        'person',
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


class AwardInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_award_change',
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
        'organization',
        'level',
        'kind',
        'goal',
        'year',
        'rounds',
        'qual_score',
    )
    show_change_link = True

    model = Award
    extra = 0
    raw_id_fields = (
        'contest',
    )
    readonly_fields = [
        'link',
        'name',
    ]

    can_delete = True
    classes = ('grp-collapse grp-closed',)


class CertificationInline(admin.TabularInline):
    fields = (
        'name',
        'person',
        'status',
        'category',
    )
    model = Certification
    extra = 0
    raw_id_fields = (
        'person',
    )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'person',
    #         'contestant',
    #     ]
    # }
    readonly_fields = [
        'name',
    ]
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class CompetitorInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_competitor_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'name',
        'award',
        'contestant',
        'total_score',
    )
    ordering = (
        'place',
    )

    show_change_link = True

    model = Competitor
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
        'status',
        'convention',
        'kind',
        'size',
        'rounds',
    )
    show_change_link = True

    model = Contest
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
        'group__kind',
        'group',
    )

    show_change_link = True

    model = Contestant
    extra = 0
    raw_id_fields = (
        'contest',
        'group',
    )
    readonly_fields = [
        'place',
        'total_score',
        'link',
    ]

    # autocomplete_lookup_fields = {
    #     'fk': [
    #         # 'contest',
    #         'group',
    #     ]
    # }
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
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'person',
    #         'contestant',
    #     ]
    # }
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class JudgeInline(admin.TabularInline):
    model = Judge
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


class ScoreInline(admin.TabularInline):
    model = Score
    fields = (
        'song',
        'judge',
        'category',
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
        'song',
        'category',
        'judge',
    ]

    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'song',
    #     ]
    # }
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-open',)


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
        'contest',
        'kind',
        'status',
        'start_date',
        'num',
        'slots',
    )
    ordering = (
        'contest',
        'kind',
    )

    model = Session
    extra = 0
    # raw_id_fields = (
    #     'award',
    # )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'award',
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
        'contestant',
    )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'person',
    #         # 'contestant',
    #     ]
    # }
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-closed',)


class SongStackedInline(SuperInlineModelAdmin, admin.StackedInline):
    fields = (
        'performance',
        'order',
        'status',
        'title',
        # 'tune',
        ('mus_points', 'prs_points', 'sng_points',),
    )
    ordering = (
        'performance',
        'order',
    )
    model = Song
    extra = 0
    raw_id_fields = (
        'tune',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'tune',
        ]
    }
    inlines = (
        ScoreInline,
    )
    readonly_fields = [
        'mus_points',
        'prs_points',
        'sng_points',
    ]
    show_change_link = True
    classes = ('grp-collapse grp-open',)
