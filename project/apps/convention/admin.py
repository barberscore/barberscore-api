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

    fields = (
        'name', (
            'website',
            'facebook',
        ),
        'phone', (
            'tenor',
            'lead',
            'baritone',
            'bass',
        ),
        'director',
        'district',
        'prelim',
        'picture',
    )

    readonly_fields = (
        'name',
        'district',
        'prelim',
    )

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'website',
        'facebook',
        'phone',
        'prelim',
    )

    list_filter = (
        'contestant_type',
    )

    ordering = (
        'name',
    )


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    save_on_top = True

    fields = (
        'contestant',
        'contest',
        'contest_round',
        'appearance',
        'song1', (
            'mus1',
            'prs1',
            'sng1',
        ),
        'song2', (
            'mus2',
            'prs2',
            'sng2',
        ),
    )

    readonly_fields = (
        'contestant',
        'contest',
        'contest_round',
        'appearance',
    )

    list_display = (
        '__unicode__',
        'song1',
        'score1',
        'song2',
        'score2',
        'appearance',
    )

    list_filter = (
        'contest',
        'contest_round',
    )
