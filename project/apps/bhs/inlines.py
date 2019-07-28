
# Django
from django.contrib import admin

# Local

from .models import Award
from .models import Convention

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

