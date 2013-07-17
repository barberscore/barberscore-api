from django.contrib import admin

from .models import (
    Profile,
)


class ProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['first_name', 'last_name']

admin.site.register(Profile, ProfileAdmin)
