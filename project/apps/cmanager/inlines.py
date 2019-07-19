
# Django
from django.contrib import admin

# Local
from .models import Assignment
from .models import Convention


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'status',
        'category',
        'kind',
        # 'person_id',
        'user',
        'convention',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        # 'person',
        'convention',
    ]
    ordering = (
        'category',
        'kind',
        # 'person__last_name',
        # 'person__first_name',
    )
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]
    raw_id_fields = [
        'user',
    ]

class ConventionInline(admin.TabularInline):
    model = Convention
    fields = [
        'name',
        'group',
    ]
    autocomplete_fields = [
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]

