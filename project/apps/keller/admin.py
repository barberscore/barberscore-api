from django.contrib import admin

from .models import CleanPanelist
from .models import CleanSong
from .models import CleanFlat
from .models import RawPanelist
from .models import RawSong

# from .models import Flat
# from .models import Complete
# from .models import Selection
# from .inlines import FlatInline

# @admin.register(CleanPanelist)
class CleanPanelistAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'district',
        'season',
        'year',
        'convention',
        'session',
        'round',
        'category',
        'num',
        'legacy_person',
        'scores',
        'panelist_id',
    ]
    list_display = [
        'id',
        'district',
        'season',
        'year',
        'convention',
        'session',
        'round',
        'category',
        'num',
        'legacy_person',
        'panelist_id',
    ]
    list_filter = [
        'district',
        'season',
        'year',
        'convention',
        'session',
        'round',
        'category',
        'num',
    ]
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'id',
        'convention',
    ]


# @admin.register(CleanSong)
class CleanSongAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'district',
        'season',
        'year',
        'convention',
        'session',
        'round',
        'appearance_num',
        'song_num',
        'legacy_group',
        'legacy_chart',
        'scores',
        'song_id',
    ]
    list_display = [
        'id',
        'district',
        'season',
        'year',
        'convention',
        'session',
        'round',
        'appearance_num',
        'song_num',
        'legacy_group',
        'legacy_chart',
        'scores',
        # 'song',
    ]
    list_filter = [
        'district',
        'season',
        'year',
        'session',
        'round',
    ]
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'id',
    ]
    raw_id_fields = [
        # 'song',
    ]


# @admin.register(CleanFlat)
class CleanFLatAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'cleanpanelist',
        'cleansong',
        'points',
        'score_id',
    ]
    list_display = [
        'id',
        'cleanpanelist',
        'cleansong',
        'points',
        'score_id',
    ]
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'id',
    ]
    raw_id_fields = [
        'cleanpanelist',
        'cleansong',
    ]


# @admin.register(RawPanelist)
class RawPanelistAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'year',
        'season',
        'district',
        'convention',
        'session',
        'round',
        'category',
        'num',
        'judge',
        'scores',
    ]
    list_display = [
        'id',
        'year',
        'season',
        'district',
        'convention',
        'session',
        'round',
        'category',
        'num',
        'judge',
    ]
    list_filter = [
        'year',
        'season',
        'district',
        'convention',
        'session',
        'round',
        'category',
        'num',
        # 'judge',
    ]
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'id',
        'convention',
    ]


# @admin.register(RawSong)
class RawSongAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'season',
        'year',
        'district',
        'event',
        'session',
        'group_name',
        'appearance_num',
        'song_num',
        'song_title',
        'totals',
        'scores',
    ]
    list_display = [
        'id',
        'season',
        'year',
        'district',
        'event',
        'session',
        'group_name',
        'appearance_num',
        'song_num',
        'song_title',
    ]
    list_filter = [
        'season',
        'year',
        'district',
        'event',
        'session',
        # 'group_name',
        # 'appearance_num',
        # 'song_num',
        # 'song_title',
    ]
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'id',
    ]


# @admin.register(Complete)
class CompleteAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'row_id',
        'points',
        'panelist_id',
    ]
    list_display = [
        'row_id',
        'panelist_id',
    ]
    readonly_fields = [
        'id',
    ]
    search_fields = [
        'row_id',
    ]



# @admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'row_id',
        'year',
        'season_kind',
        'convention_name',
        'session_kind',
        'round_kind',
        'group_name',
        'appearance_num',
        'song_num',
        'song_title',
        'points',
        'song_id',
    ]
    list_display = [
        'row_id',
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

    ordering = (
        'row_id',
        'appearance_num',
        'song_num',
    )
    readonly_fields = [
        'id',
    ]
    inlines = [
        # FlatInline,
    ]


# @admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'complete',
        'selection',
        'score_id',
    ]
    list_display = [
        'id',
        'complete',
        'selection',
        'score_id',
    ]
    list_select_related = [
        'complete',
        'selection',
    ]
    readonly_fields = [
        'id',
    ]
    autocomplete_fields = [
        'complete',
        'selection',
    ]
