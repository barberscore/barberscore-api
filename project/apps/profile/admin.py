from django.contrib import admin

from .models import (
    UserProfile,
)


class UserProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['first_name', 'last_name']

admin.site.register(UserProfile, UserProfileAdmin)
