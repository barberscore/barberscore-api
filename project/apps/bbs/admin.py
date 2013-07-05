from django.contrib import admin

from .models import (
    Contest,
    Contestant,
    Performance,
    Singer,
    Song
)


class ContestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("year", "level", "contest_type", "contest_round")}


class SingerAdmin(admin.ModelAdmin):
    save_on_top = True


class ContestantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug', 'district', 'location', 'website', 'facebook']
    list_filter = ['district', 'contestant_type']
    search_fields = ['name']


class PerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = [
        (None, {'fields': ['contest', 'contestant', 'slot', 'stage_time']}),
        ('Scores', {'fields': [('song_one', 'score_one'), ('song_two', 'score_two')]}),
        ('Detail', {'fields': [('mus_one', 'prs_one', 'sng_one'), ('mus_two', 'prs_two', 'sng_two')], 'classes':['collapse']})
    ]
    list_display = ['__unicode__', 'slug', 'stage_time']
    list_filter = ['contest']
    raw_id_fields = ['song_one', 'song_two']


class SongAdmin(admin.ModelAdmin):
    save_on_top = True


admin.site.register(Contest, ContestAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Singer, SingerAdmin)
admin.site.register(Song, SongAdmin)
