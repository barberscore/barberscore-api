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
        'name',
        'contestant_type',
        ('website', 'facebook'),
        'phone',
        ('tenor', 'lead', 'baritone', 'bass'),
        'director',
        'district',
        'prelim',
        'picture',
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
        'stagetime',
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
        'song1_score',
        'song2',
        'song2_score',
        'appearance',
    )

    list_filter = (
        'contest',
        'contest_round',
    )
