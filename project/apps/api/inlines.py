from django.contrib import admin

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from super_inlines.admin import SuperInlineModelAdmin


from .models import (
    Arranger,
    Contest,
    Certification,
    Contestant,
    Session,
    Performer,
    Director,
    Judge,
    Performance,
    Score,
    Round,
    Singer,
    Song,
)


class ArrangerInline(admin.TabularInline):
    model = Arranger
    fields = (
        # 'song',
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
        'session',
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
        'session',
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
    #         'performer',
    #     ]
    # }
    readonly_fields = [
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
        'name',
        'contest',
        'performer',
        'total_score',
    )
    ordering = (
        'place',
    )

    show_change_link = True

    model = Contestant
    extra = 0
    raw_id_fields = (
        'performer',
    )
    autocomplete_lookup_fields = {
        'fk': [
            'performer',
        ]
    }
    readonly_fields = [
        'link',
        'name',
        'total_score',
    ]
    can_delete = True
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
        'name',
        'status',
        'convention',
        'kind',
        'size',
        'rounds',
    )
    show_change_link = True

    model = Session
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


class PerformerInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_performer_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'session',
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

    model = Performer
    extra = 0
    raw_id_fields = (
        'session',
        'group',
    )
    readonly_fields = [
        'place',
        'total_score',
        'link',
    ]

    # autocomplete_lookup_fields = {
    #     'fk': [
    #         # 'session',
    #         'group',
    #     ]
    # }
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class DirectorInline(admin.TabularInline):
    fields = (
        'performer',
        'person',
        'part',
    )
    ordering = (
        'part',
        'performer',
    )
    model = Director
    extra = 0
    raw_id_fields = (
        'person',
        'performer',
    )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'person',
    #         'performer',
    #     ]
    # }
    can_delete = True
    classes = ('grp-collapse grp-closed',)


class JudgeInline(admin.TabularInline):
    model = Judge
    fields = (
        'session',
        'person',
        # 'organization',
        'category',
        'slot',
        'kind',
    )
    ordering = (
        'kind',
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
        'performer',
        'status',
        'position',
        'draw',
        # 'start',
    )
    sortable_field_name = "position"

    model = Performance
    extra = 0
    # raw_id_fields = (
    #     'performer',
    # )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'performer',
    #     ]
    # }
    readonly_fields = (
        'performer',
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


class RoundInline(admin.TabularInline):
    def link(self, obj):
        return mark_safe(
            "<a href={0}>link</a>".format(
                reverse(
                    'admin:api_round_change',
                    args=(
                        obj.id.hex,
                    )
                )
            )
        )

    fields = (
        'link',
        'session',
        'kind',
        'status',
        'start_date',
        'num',
        'slots',
    )
    ordering = (
        'session',
        'kind',
    )

    model = Round
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
        'performer',
        'person',
        'part',
    )
    ordering = (
        'part',
        'performer',
    )
    extra = 0
    raw_id_fields = (
        'person',
        'performer',
    )
    # autocomplete_lookup_fields = {
    #     'fk': [
    #         'person',
    #         # 'performer',
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
