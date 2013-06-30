from django.contrib import admin

from .models import (
    Convention,
    Contestant,
    Performance,
    Score
)


class ConventionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("year","level", "contest_type")}


class ContestAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ContestantAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'slug', 'district']
    list_filter = ['district']


class PerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = [
        (None, {'fields': ['convention', 'contest_round', 'contestant', 'slot']}),
        ('Scores', {'fields': [('song_one', 'score_one'), ('song_two', 'score_two')]}),
        ('Detail', {'fields': [('mus_one', 'prs_one', 'sng_one'), ('mus_two', 'prs_two', 'sng_two')], 'classes':['collapse']})
    ]

admin.site.register(Convention, ConventionAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Score)
