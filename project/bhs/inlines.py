# Django
from django.contrib import admin

# Local
from .models import (
    Human,
    Membership,
    Role,
    SMJoin,
    Status,
    Structure,
    Subscription,
)


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fields = [
        'items_editable',
        'current_through',
        'status',
        'human',
    ]
    readonly_fields = [
        'items_editable',
        'current_through',
        'status',
        'human',
    ]
    show_change_link = True
    extra = 0
    # classes = [
    #     'collapse',
    # ]
    max_num = 0
    can_delete = False


class SMJoinInline(admin.TabularInline):
    model = SMJoin
    fields = [
        '__str__',
        'membership',
        'structure',
        # 'human',
        'vocal_part',
        'status',
    ]
    readonly_fields = [
        '__str__',
        'membership',
        'structure',
        # 'human',
        'vocal_part',
        'status',
    ]
    show_change_link = True
    extra = 0
    # classes = [
    #     'collapse',
    # ]
    max_num = 0
    can_delete = False


class MembershipInline(admin.TabularInline):
    model = Membership
    fields = [
        '__str__',
        'status',
    ]
    readonly_fields = [
        '__str__',
        'status',
    ]
    show_change_link = True
    extra = 0
    # classes = [
    #     'collapse',
    # ]
    max_num = 0
    can_delete = False


class RoleInline(admin.TabularInline):
    model = Role
    fields = [
        '__str__',
        'start_date',
        'end_date',
    ]
    readonly_fields = [
        '__str__',
        'start_date',
        'end_date',
    ]
    show_change_link = True
    extra = 0
    # classes = [
    #     'collapse',
    # ]
    max_num = 0
    can_delete = False
