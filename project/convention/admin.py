from django.contrib import admin

from .models import (
    Contest,
    Contestant,
    Performance,
    Profile,
    Note,
)


class PerformanceInline(admin.TabularInline):
    model = Performance

    fields = (
        'contestant',
        'contest_round',
        'session',
        'appearance',
    )

    extra = 10


class ScoreInline(admin.TabularInline):
    model = Performance

    fields = (
        'contestant',
        'contest_round',
        'mus1',
        'prs1',
        'sng1',
        'mus2',
        'prs2',
        'sng2',
    )

    max_num = 0


class SongInline(admin.TabularInline):
    model = Performance

    fields = (
        'contestant',
        'contest_round',
        'song1',
        'song2',
    )

    max_num = 0


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contest", {
            'fields': (
                'year',
                'contest_level',
                'contest_type',
            ),
        }),
    )

    list_filter = (
        'year',
        'contest_level',
        'contest_type',
    )

    inlines = (
        PerformanceInline,
        # ScoreInline,
    )

    save_on_top = True


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'contestant_type',
            ),
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': (
                ('website', 'facebook', 'twitter'),
                ('phone', 'email'),
                ('tenor', 'lead', 'baritone', 'bass', 'director',),
                ('district', 'location'),
                ('prelim', 'rank'),
                'picture',
                'blurb',
            ),
        }),
    )

    inlines = (
        SongInline,
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
        ('contestant', 'contest'),
        ('contest_round', 'session'),
        ('appearance', 'stagetime'),
        ('song1', 'song2'),
        ('mus1', 'prs1', 'sng1'),
        ('mus2', 'prs2', 'sng2'),
        ('place', 'men_on_stage'),
    )

    list_display = (
        '__unicode__',
        # 'stagetime',
        'song1',
        'mus1',
        'prs1',
        'sng1',
        'song2',
        'mus2',
        'prs2',
        'sng2',
        'place',
    )

    list_filter = (
        'contest',
        'contest_round',
    )

    search_fields = (
        'contestant__name',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'timezone',
    )

    save_on_top = True


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        '__unicode__',
        'note',
    )
    search_fields = (
        'note',
    )
    list_filter = (
        'contestant',
    )
