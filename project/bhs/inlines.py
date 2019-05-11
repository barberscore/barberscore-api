
# Django
from django.contrib import admin

# Local
from .models import Human
from .models import Join
from .models import Membership
from .models import Role
from .models import Status
from .models import Structure
from .models import Subscription

from .models import Repertory

class StructureInline(admin.TabularInline):
    model = Structure
    fields = [
        'name',
        'kind',
        'gender',
        'bhs_id',
    ]
    readonly_fields = [
        'name',
        'kind',
        'gender',
        'bhs_id',
    ]
    show_change_link = True
    extra = 0
    # classes = [
    #     'collapse',
    # ]
    max_num = 0
    can_delete = False


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


class JoinInline(admin.TabularInline):
    model = Join
    fields = [
        '__str__',
        'subscription',
        'membership',
        'structure',
        # 'human',
        'part',
        'inactive_date',
        'status',
        'paid',
    ]
    readonly_fields = [
        '__str__',
        'subscription',
        'membership',
        'structure',
        # 'human',
        'part',
        'inactive_date',
        'status',
        'paid',
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


class RepertoryInline(admin.TabularInline):
    model = Repertory
    fields = [
        'chart',
        'group',
        'status',
    ]
    autocomplete_fields = [
        'chart',
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    readonly_fields = [
        'status',
    ]
    ordering = [
        'chart__title',
    ]


