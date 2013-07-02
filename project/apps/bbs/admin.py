from django.contrib import admin

from .models import (
    Contest,
    Contestant,
    Performance,
    Rating,
)


class ContestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("year", "level", "contest_type")}


class ContestantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug', 'district', 'seed']
    list_filter = ['district', 'contestant_type']


class PerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = [
        (None, {'fields': ['contest', 'contest_round', 'contestant', 'slot', 'stage_time']}),
        ('Scores', {'fields': [('song_one', 'score_one'), ('song_two', 'score_two')]}),
        ('Detail', {'fields': [('mus_one', 'prs_one', 'sng_one'), ('mus_two', 'prs_two', 'sng_two')], 'classes':['collapse']})
    ]
    list_display = ['__unicode__', 'stage_time']
    list_filter = ['contest']


class RatingAdmin(admin.ModelAdmin):
    save_on_top = True
    raw_id_fields = ['performance']
    list_display = ['user', 'performance']

admin.site.register(Contest, ContestAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Rating, RatingAdmin)
