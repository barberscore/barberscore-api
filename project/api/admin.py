# Third-Party

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as AuthGroup


# Local
from .forms import UserChangeForm
from .forms import UserCreationForm

from .models import User


admin.site.site_header = 'Barberscore Admin Backend'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        'username',
        # 'person',
        # 'is_mc',
    ]
    # list_select_related = [
    #     'person',
    # ]
    # autocomplete_fields = [
    #     'person',
    # ]
    list_filter = (
        'is_staff',
    )

    fieldsets = (
        (None, {
            'fields': (
                # 'id',
                'username',
                # # 'person',
                # # 'is_mc',
                # 'is_staff',
                # 'created',
                # 'modified',
                # 'is_convention_manager',
                # 'is_session_manager',
                # 'is_round_manager',
                # 'is_scoring_manager',
                # 'is_group_manager',
                # 'is_person_manager',
                # 'is_award_manager',
                # 'is_officer_manager',
                # 'is_chart_manager',
                # 'is_assignment_manager',
            )
        }),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': (
    #             'person',
    #         )
    #     }),
    # )
    # search_fields = [
    #     'username',
    #     'person__first_name',
    #     'person__last_name',
    #     'person__bhs_id',
    #     'person__email',
    # ]
    # ordering = (
    #     'person__last_name',
    #     'person__first_name',
    # )
    filter_horizontal = ()
    # readonly_fields = [
    #     'id',
    #     'is_mc',
    #     'created',
    #     'modified',
    # ]

#     def is_mc(self, instance):
#         return instance.is_mc
#     is_mc.boolean = True
#     is_mc.short_description = 'Is Member Center'

# admin.site.unregister(AuthGroup)
