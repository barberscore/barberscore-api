# Django
# Third-Party
from django.contrib import admin

from .models import (
    Human,
    Structure,
    Membership,
    Status,
    Subscription,
    SubscriptionMembershipJoin,
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
        'birth_date',
        'is_deceased',
        'phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'sex',
        'primary_voice_part',
    ]

    list_display = [
        '__str__',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        'birth_date',
        'is_deceased',
        'phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'sex',
        'primary_voice_part',
    ]

    readonly_fields = [
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        'birth_date',
        'is_deceased',
        'phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'sex',
        'primary_voice_part',
    ]

    list_filter = [
        'sex',
        'is_deceased',
        'primary_voice_part',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'bhs_id',
    ]

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
        'established_date',
        'status',
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
        'established_date',
        'status',
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


@admin.register(Membership)
class MembershipAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'structure',
        'status',
    ]

    list_display = [
        'id',
        'structure',
        'status',
    ]

    readonly_fields = [
        'id',
        'structure',
        'status',
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
        'id',
        'valid_through',
        'status',
    ]

    list_display = [
        'id',
        'valid_through',
        'status',
    ]

    readonly_fields = [
        'id',
        'valid_through',
        'status',
    ]

    list_filter = [
        'status',
    ]
#
#
# @admin.register(SubscriptionMembershipJoin)
# class SubscriptionMembershipJoinAdmin(ReadOnlyAdmin):
#     fields = [
#         'id',
#         'status',
#         'vocal_part',
#         'subscription',
#         'membership',
#     ]
#
#     list_display = [
#         'id',
#         'status',
#         'vocal_part',
#         'subscription',
#         'membership',
#     ]
#
#     readonly_fields = [
#         'id',
#         'status',
#         'vocal_part',
#         'subscription',
#         'membership',
#     ]
#
#     list_filter = [
#         'vocal_part',
#     ]
