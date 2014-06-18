from django.contrib import admin

from .models import (
    Profile,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    save_on_top = True
