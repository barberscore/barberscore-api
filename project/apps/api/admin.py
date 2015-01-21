from django.contrib import admin

from .models import (
    Singer,
    Chorus,
)


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Chorus)
class ChorusAdmin(admin.ModelAdmin):
    save_on_top = True
