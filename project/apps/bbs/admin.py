from django.contrib import admin

from .models import (
    Contest,
    Contestant,
    Score,
)

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'slug',
    )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    save_on_top = True
