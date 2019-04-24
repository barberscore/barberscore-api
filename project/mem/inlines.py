
# Django
from django.contrib import admin

# Local
from .models import Stream


class StreamInline(admin.TabularInline):
    model = Stream
    fields = [
        'id',
        'person',
        'group',
        'code',
        'status',
        'inactive_date',
        'inactive',
        'is_current',
        'is_paid',
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
        '-is_current',
        'person__last_name',
        'person__first_name',
        'group__kind',
        'group__name',
    ]