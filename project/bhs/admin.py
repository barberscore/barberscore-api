# Django
# Third-Party
from django.contrib import admin

# Local
from .inlines import (
    MembershipInline,
    # RoleInline,
    SMJoinInline,
    SubscriptionInline,
)
from .models import (
    Human,
    Membership,
    Role,
    SMJoin,
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
    inlines = [
        # MembershipInline,
        SMJoinInline,
    ]
    ordering = (
        '-created_ts',
    )


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

    list_filter = [
        'structure__kind',
    ]

    readonly_fields = [
        'structure',
        'code',
        'status',
        'created_ts',
        'updated_ts',
    ]

    inlines = [
        SMJoinInline,
    ]

    ordering = (
        'structure__name',
        'code',
    )

    search_fields = [
        'structure__name',
    ]


@admin.register(Status)
class StatusAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'name',
    ]

    list_display = [
        'id',
        'name',
    ]

    readonly_fields = [
        'id',
        'name',
    ]


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
        SMJoinInline,
    ]


@admin.register(Role)
class RoleAdmin(ReadOnlyAdmin):
    fields = [
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
    ]

    list_display = [
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
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
    ]

    ordering = (
        'structure__name',
    )

    search_fields = [
        'structure__name',
        'human__name',
    ]


@admin.register(SMJoin)
class SMJoinAdmin(ReadOnlyAdmin):
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
        'vocal_part',
        'subscription',
        'membership',
        'established_date',
        'inactive_date',
        'inactive_reason',
        'updated_ts',
    ]

    readonly_fields = [
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

    list_filter = [
        'vocal_part',
    ]

    # search_fields = [
    #     'subscription',
    # ]
