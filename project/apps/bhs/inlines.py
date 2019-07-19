
# Django
from django.contrib import admin

# Local
# from .models import Human
# from .models import Join
# from .models import Membership
# from .models import Role
# from .models import Status
# from .models import Structure
# from .models import Subscription

from .models import Award
from .models import Repertory
from .models import Group
from .models import Member
from .models import Officer

class AwardInline(admin.TabularInline):
    model = Award
    fields = [
        'name',
        'kind',
        'gender',
        'is_single',
        'group',
    ]
    readonly_fields = [
        'name',
        'status',
    ]
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]


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

class MemberInline(admin.TabularInline):
    model = Member
    fields = [
        'person',
        'group',
        'part',
        'start_date',
        'end_date',
        'status',
    ]
    autocomplete_fields = [
        'person',
        'group',
    ]
    ordering = (
        '-status',
        'part',
        'person__last_name',
        'person__first_name',
    )
    readonly_fields = [
        'status',
    ]

    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class OfficerInline(admin.TabularInline):
    model = Officer
    fields = [
        'office',
        'person',
        'group',
        'status',
    ]
    autocomplete_fields = [
        'person',
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    ordering = [
        'person__last_name',
        'person__first_name',
    ]
    readonly_fields = [
        'status',
    ]


# class ActiveChapterInline(admin.TabularInline):
#     model = Group
#     fields = [
#         'name',
#         'parent',
#         'code',
#         # 'kind',
#         'gender',
#         # 'bhs_id',
#         # 'status',
#     ]
#     fk_name = 'parent'
#     ordering = [
#     ]
#     show_change_link = True
#     extra = 0
#     classes = [
#         'collapse',
#     ]
#     verbose_name_plural = 'Active Chapters'

#     def get_queryset(self, request):
#         """Alter the queryset to return no existing entries."""
#         qs = super().get_queryset(request)
#         qs = qs.filter(
#             status__gt=0,
#             kind=Group.KIND.chapter,
#         )
#         return qs


# class ActiveChorusInline(admin.TabularInline):
#     model = Group
#     fields = [
#         'name',
#         'parent',
#         'bhs_id',
#         # 'code',
#         # 'kind',
#         'gender',
#         'status',
#         'mc_pk',
#     ]
#     fk_name = 'parent'
#     ordering = [
#     ]
#     show_change_link = True
#     extra = 0
#     classes = [
#         'collapse',
#     ]
#     verbose_name_plural = 'All Choruses'
#     readonly_fields = [
#         'status',
#     ]

#     def get_queryset(self, request):
#         """Alter the queryset to return no existing entries."""
#         qs = super().get_queryset(request)
#         qs = qs.filter(
#             kind=Group.KIND.chorus,
#         )
#         return qs


# class ActiveQuartetInline(admin.TabularInline):
#     model = Group
#     fields = [
#         'name',
#         'parent',
#         'bhs_id',
#         'is_senior',
#         'is_youth',
#         'gender',
#         # 'status',
#     ]
#     fk_name = 'parent'
#     ordering = [
#     ]
#     show_change_link = True
#     extra = 0
#     classes = [
#         'collapse',
#     ]
#     verbose_name_plural = 'Active Quartets'
#     readonly_fields = [
#         'status',
#     ]

#     def get_queryset(self, request):
#         """Alter the queryset to return no existing entries."""
#         qs = super().get_queryset(request)
#         qs = qs.filter(
#             status__gt=0,
#             kind=Group.KIND.quartet,
#         )
#         return qs



# class StructureInline(admin.TabularInline):
#     model = Structure
#     fields = [
#         'name',
#         'kind',
#         'gender',
#         'bhs_id',
#     ]
#     readonly_fields = [
#         'name',
#         'kind',
#         'gender',
#         'bhs_id',
#     ]
#     show_change_link = True
#     extra = 0
#     # classes = [
#     #     'collapse',
#     # ]
#     max_num = 0
#     can_delete = False


# class SubscriptionInline(admin.TabularInline):
#     model = Subscription
#     fields = [
#         'items_editable',
#         'current_through',
#         'status',
#         'human',
#     ]
#     readonly_fields = [
#         'items_editable',
#         'current_through',
#         'status',
#         'human',
#     ]
#     show_change_link = True
#     extra = 0
#     # classes = [
#     #     'collapse',
#     # ]
#     max_num = 0
#     can_delete = False


# class JoinInline(admin.TabularInline):
#     model = Join
#     fields = [
#         '__str__',
#         'subscription',
#         'membership',
#         'structure',
#         # 'human',
#         'part',
#         'inactive_date',
#         'status',
#         'paid',
#     ]
#     readonly_fields = [
#         '__str__',
#         'subscription',
#         'membership',
#         'structure',
#         # 'human',
#         'part',
#         'inactive_date',
#         'status',
#         'paid',
#     ]
#     show_change_link = True
#     extra = 0
#     # classes = [
#     #     'collapse',
#     # ]
#     max_num = 0
#     can_delete = False


# class MembershipInline(admin.TabularInline):
#     model = Membership
#     fields = [
#         '__str__',
#         'status',
#     ]
#     readonly_fields = [
#         '__str__',
#         'status',
#     ]
#     show_change_link = True
#     extra = 0
#     # classes = [
#     #     'collapse',
#     # ]
#     max_num = 0
#     can_delete = False


# class RoleInline(admin.TabularInline):
#     model = Role
#     fields = [
#         '__str__',
#         'start_date',
#         'end_date',
#     ]
#     readonly_fields = [
#         '__str__',
#         'start_date',
#         'end_date',
#     ]
#     show_change_link = True
#     extra = 0
#     # classes = [
#     #     'collapse',
#     # ]
#     max_num = 0
#     can_delete = False


