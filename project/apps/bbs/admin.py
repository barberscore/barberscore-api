from django.contrib import admin

from .models import (
    Contest,
    Contestant,
    Score,
)


class ContestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("year", "contest_level", "contest_type", )}


class ContestantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug', 'district', 'location', 'website', 'facebook']
    list_filter = ['district', 'contestant_type']
    search_fields = ['name']


class ScoreAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['__unicode__', 'song1', 'mus1', 'prs1', 'sng1', 'song2', 'mus2', 'prs2', 'sng2']


admin.site.register(Contest, ContestAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Score, ScoreAdmin)
