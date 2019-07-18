
# Django
from django.contrib import admin
from django.apps import apps

# Local
from .models import Appearance
from .models import Contender
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Song


class AppearanceInline(admin.TabularInline):
    model = Appearance
    fields = [
        # 'group',
        'status',
        'representing',
        'num',
        'base',
        # 'stats',
    ]
    readonly_fields = [
        # 'group',
        'status',
    ]
    ordering = (
        # 'draw',
        'num',
        # 'group__name',
    )
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class ContenderInline(admin.TabularInline):
    model = Contender
    fields = [
        'appearance',
        'outcome',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        'appearance',
        'outcome',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class OutcomeInline(admin.TabularInline):
    model = Outcome
    fields = [
        'num',
        'award',
        'round',
        'name',
    ]
    autocomplete_fields = [
        'award',
        'round',
    ]
    ordering = (
        'num',
    )
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'award':
    #         try:
    #             Award = apps.get_model('cmanager.award')
    #             parent_obj_id = request.resolver_match.kwargs['object_id']
    #             round = Round.objects.get(id=parent_obj_id)
    #             kwargs["queryset"] = Award.objects.filter(
    #                 kind=round.session.kind,
    #                 season=round.session.convention.season,
    #                 group=round.session.convention.group,
    #             )
    #         except IndexError:
    #             pass
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PanelistInline(admin.TabularInline):
    model = Panelist
    fields = [
        'status',
        'category',
        'kind',
        'num',
        # 'person',
        'representing',
        'round',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        # 'person',
        'round',
    ]
    ordering = (
        'num',
    )
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]


class ScoreInline(admin.TabularInline):
    model = Score
    fields = [
        'song',
        # 'panelist__person__common_name',
        'points',
    ]
    autocomplete_fields = [
        'song',
    ]
    readonly_fields = [
        'song',
        # 'panelist__person__common_name',
        'status',
    ]
    ordering = (
        'panelist__num',
    )
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    # def panelist__person__common_name(self, obj):
    #     return getattr(getattr(obj.panelist, 'person'), 'common_name', getattr(obj.panelist, 'legacy_name'))


class SongInline(admin.TabularInline):
    model = Song
    fields = [
        'num',
    ]
    ordering = (
        'num',
    )
    show_change_link = True
    extra = 0
    can_delete = False
    classes = [
        'collapse',
    ]
    readonly_fields = [
        'status',
    ]


class RoundInline(admin.TabularInline):
    model = Round
    fields = [
        'session',
        'kind',
        'status',
        'num',
    ]
    ordering = (
        'session',
        'kind',
    )
    readonly_fields = [
        'status',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
