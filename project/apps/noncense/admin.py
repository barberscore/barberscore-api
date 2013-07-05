from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import MobileUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users."""

    class Meta:
        model = MobileUser
        fields = ('mobile', )


class UserChangeForm(forms.ModelForm):
    """A form for updating users."""

    class Meta:
        model = MobileUser
        fields = ['mobile', ]


class MobileUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('mobile', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('mobile', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', )}),
    )
    search_fields = ('mobile',)
    ordering = ('mobile',)
    filter_horizontal = ()

# # Now register the new UserAdmin...
admin.site.register(MobileUser, MobileUserAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
