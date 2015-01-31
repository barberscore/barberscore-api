from django.contrib import admin

from .models import (
    Profile,
    Note,
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
