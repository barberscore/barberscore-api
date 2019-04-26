
# Django
from django.contrib import admin

# Local
from .models import Member
from .models import Stream


class StreamInline(admin.TabularInline):
    model = Stream
    fields = [
        'id',
        'person',
        'group',
        'code',
        'status',
        'established_date',
        'current_through',
        'part',
    ]
    readonly_fields = [
        'id',
    ]
    show_change_link = True
    extra = 0
    # classes = [
    #     'collapse',
    # ]
    max_num = 0
    can_delete = False
    raw_id_fields = [
        'person',
        'group',
    ]
    ordering = [
        # '-is_current',
        'person__last_name',
        'person__first_name',
        'group__kind',
        'group__name',
        '-is_current',
    ]


class MemberInline(admin.TabularInline):
    model = Member
    fields = [
        'id',
        'status',
        'person',
        'group',
        'start_date',
        'end_date',
        'part',
    ]
    readonly_fields = [
        'id',
    ]
    show_change_link = True
    extra = 0
    # classes = [
    #     'collapse',
    # ]
    max_num = 0
    can_delete = False
    raw_id_fields = [
        'person',
        'group',
    ]
    ordering = [
        # '-is_current',
        'person__last_name',
        'person__first_name',
        'group__kind',
        'group__name',
    ]