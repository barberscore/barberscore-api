from django.contrib import admin

from .models import Flat
from .models import Complete
from .models import Selection
from .inlines import FlatInline

# Register your models here.
@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'complete',
        'selection',
        'score',
    ]
    list_display = [
        'id',
        'complete',
        'selection',
        'score',
    ]
    list_select_related = [
        'complete',
        'selection',
        'score',
    ]
    readonly_fields = [
        'id',
    ]
    autocomplete_fields = [
        'complete',
        'selection',
        'score',
    ]


@admin.register(Complete)
class CompleteAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'mark',
        'row',
        'year',
        'season_raw',
        'district_raw',
        'convention_raw',
        'session_raw',
        'round_raw',
        'category_raw',
        'season_kind',
        'convention_name',
        'session_kind',
        'round_kind',
        'category_kind',
        'panelist_name',
        'panelist_num',
        'points',
        'panelist',
    ]
    list_display = [
        'row',
        # 'mark',
        # 'convention_raw',
        # 'session_raw',
        # 'session_kind',
        # 'round_raw',
        # 'round_kind',
        # 'id',
        # 'category',
        # 'panelist_num',
        # 'panelist_name',
        # 'person',
        # 'num_appearances',
        # 'num_panelists',
        # 'points',
        # 'convention',
        # 'session',
        # 'round',
        'panelist',
    ]
    list_select_related = [
        'panelist',
    ]
    list_filter = [
        'year',
        'season_kind',
        'session_kind',
        'round_kind',
        'district_code',
    ]
    ordering = (
        'year',
        'district_code',
        'season_kind',
        'session_kind',
        'round_kind',
        'panelist_num',
    )
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'round',
    ]
    autocomplete_fields = [
        'panelist',
    ]
    inlines = [
        FlatInline,
    ]


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'row',
        'season_raw',
        'year',
        'district_raw',
        'event_raw',
        'session_raw',
        'season_kind',
        'convention_name',
        'session_kind',
        'round_kind',
        'group_name',
        'appearance_num',
        'song_num',
        'song_title',
        'totals',
        'points',
        'song',
    ]
    list_display = [
        'row',
        # 'season_raw',
        # 'district_raw',
        # 'event_raw',
        # 'session_raw',
        # 'district_code',
        # 'event_raw',
        # 'convention',
        # 'event_raw',
        # 'session_raw',
        # 'session_kind',
        # 'session',
        'song',
        'song_num',
        # 'round_kind',
        # 'appearance_num',
        # 'song_num',
        # 'group_name',
        # 'song_title',
        # 'convention',
        # 'session',
        # 'round',
        # 'appearance',
        # 'totals',
        # 'points',
        # 'song',
    ]
    list_filter = [
        'year',
        # 'season_raw',
        # 'district_raw',
        # 'event_raw',
        # 'session_raw',
        'season_kind',
        'district_code',
        'session_kind',
        'round_kind',
    ]
    list_select_related = [
        'song',
    ]
    list_editable = [
        # 'convention_name',
    ]

    ordering = (
        'row',
        'appearance_num',
        'song_num',
    )
    readonly_fields = [
        'id',
    ]
    autocomplete_fields = [
        'song',
    ]
    search_fields = [
        'song',
    ]
    inlines = [
        FlatInline,
    ]
