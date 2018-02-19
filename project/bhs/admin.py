# Django
# Third-Party
from django.contrib import admin

# Local
from .inlines import (
    MembershipInline,
    RoleInline,
    JoinInline,
    SubscriptionInline,
)
from .models import (
    Human,
    Membership,
    Role,
    Join,
    Status,
    Structure,
    Subscription,
)

admin.site.disable_action('delete_selected')


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)


@admin.register(Human)
class HumanAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        # 'is_deceased',
        'phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'birth_date',
        'sex',
        'primary_voice_part',
        'created_ts',
        'updated_ts',
    ]

    list_display = [
        '__str__',
        # 'first_name',
        # 'middle_name',
        # 'last_name',
        # 'nick_name',
        'email',
        # 'is_deceased',
        'phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'birth_date',
        'sex',
        'primary_voice_part',
        'created_ts',
        'updated_ts',
    ]

    readonly_fields = [
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        # 'is_deceased',
        'phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'birth_date',
        'sex',
        'primary_voice_part',
        'created_ts',
        'updated_ts',
    ]

    list_filter = [
        'sex',
        # 'is_deceased',
        'primary_voice_part',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'bhs_id',
        'email',
    ]

    inlines = [
        RoleInline,
        SubscriptionInline,
    ]

    ordering = (
        'last_name',
        'first_name',
    )


@admin.register(Structure)
class StructureAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'name',
        'kind',
        'bhs_id',
        'chapter_code',
        'chorus_name',
        'phone',
        'email',
        'website',
        'facebook',
        'twitter',
        'established_date',
        'status',
        'parent',
        'created_ts',
        'updated_ts',
    ]

    list_display = [
        '__str__',
        'name',
        'kind',
        'bhs_id',
        'chapter_code',
        'chorus_name',
        'phone',
        'email',
        'established_date',
        'status',
        'parent',
        'created_ts',
        'updated_ts',
    ]

    readonly_fields = [
        'id',
        'name',
        'kind',
        'bhs_id',
        'chapter_code',
        'chorus_name',
        'phone',
        'email',
        'website',
        'facebook',
        'twitter',
        'established_date',
        'status',
        'parent',
        'created_ts',
        'updated_ts',
    ]

    list_filter = [
        'kind',
        'status',
    ]
    search_fields = [
        'name',
        'chorus_name',
        'bhs_id',
        'chapter_code',
        'chorus_name',
    ]

    list_select_related = [
        'parent',
    ]

    ordering = (
        '-created_ts',
    )

    INLINES = {
        'organization': [
            RoleInline,
        ],
        'district': [
            RoleInline,
        ],
        'chapter': [
            RoleInline,
        ],
        'quartet': [
            RoleInline,
            JoinInline,
        ],
    }

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        inlines = self.INLINES[obj.kind]
        # try:
        #     inlines = self.INLINES[obj.kind]
        # except AttributeError:
        #     return inline_instances
        # except KeyError:
        #     # Defaults to Group
        #     inlines = self.INLINES['Group']

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            inline_instances.append(inline)
        return inline_instances

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)


@admin.register(Membership)
class MembershipAdmin(ReadOnlyAdmin):
    fields = [
        'structure',
        'code',
        'status',
        'created_ts',
        'updated_ts',
    ]

    list_display = [
        'structure',
        'code',
        'status',
        'created_ts',
        'updated_ts',
    ]

    list_select_related = [
        'structure',
    ]

    list_filter = [
        'structure__kind',
        'code',
        'status',
    ]

    readonly_fields = [
        'structure',
        'code',
        'status',
        'created_ts',
        'updated_ts',
    ]

    inlines = [
        JoinInline,
    ]

    ordering = (
        'structure__name',
        'code',
    )

    search_fields = [
        'structure__name',
    ]


# @admin.register(Status)
# class StatusAdmin(ReadOnlyAdmin):
#     fields = [
#         'id',
#         'name',
#     ]

#     list_display = [
#         'id',
#         'name',
#     ]

#     readonly_fields = [
#         'id',
#         'name',
#     ]


@admin.register(Subscription)
class SubscriptionAdmin(ReadOnlyAdmin):
    fields = [
        '__str__',
        'items_editable',
        'current_through',
        'status',
        'created_ts',
        'updated_ts',
    ]

    list_display = [
        '__str__',
        'items_editable',
        'current_through',
        'status',
        'created_ts',
        'updated_ts',
    ]

    readonly_fields = [
        '__str__',
        'items_editable',
        'current_through',
        'status',
        'created_ts',
        'updated_ts',
    ]

    list_filter = [
        'status',
    ]
    search_fields = (
        'human__last_name',
        'human__first_name',
        'human__bhs_id',
    )

    ordering = (
        'human__last_name',
    )

    inlines = [
        JoinInline,
    ]


@admin.register(Role)
class RoleAdmin(ReadOnlyAdmin):
    fields = [
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
        'abbv',
        'officer_roles_id',
    ]

    list_display = [
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
        'abbv',
        'officer_roles_id',
    ]

    list_select_related = [
        'structure',
        'human',
    ]
    list_filter = [
        'name',
    ]

    readonly_fields = [
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
        'abbv',
        'officer_roles_id',
    ]

    ordering = (
        'structure__name',
    )

    search_fields = [
        'structure__name',
        'human__name',
    ]


@admin.register(Join)
class JoinAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'status',
        'vocal_part',
        'subscription',
        'membership',
        'established_date',
        'inactive_date',
        'inactive_reason',
        'updated_ts',
    ]

    list_display = [
        'id',
        'status',
        'subscription',
        'membership',
        'vocal_part',
        'inactive_date',
        'inactive_reason',
        'established_date',
        'updated_ts',
    ]

    list_select_related = [
        'subscription',
        'membership',
    ]
    readonly_fields = [
        'id',
        'status',
        'subscription',
        'membership',
        'vocal_part',
        'inactive_date',
        'inactive_reason',
        'established_date',
        'updated_ts',
    ]

    list_display_links = [
        'id',
    ]

    list_filter = [
        'vocal_part',
        'structure__kind',
        'inactive_reason',
        'inactive_date',
    ]

    search_fields = [
        'subscription__human__last_name',
        'subscription__human__bhs_id',
        # 'membership__structure__name',
        # 'membership__structure__bhs_id',
    ]
