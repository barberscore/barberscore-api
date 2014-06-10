from django.contrib import admin

from .models import (
    Contest,
    Contestant,
    Performance,
)


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = (
        'name',
    )
    list_display = (
        '__unicode__',
        'contestant_type',
        'slug',
        'prelim',
    )
    list_filter = (
        'contestant_type',
    )


@admin.register(Performance)
class PerforamnceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        '__unicode__',
        'appearance',
    )
    list_filter = (
        'contest',
    )
