
# Django
from django.contrib import admin

# Local
from .models import Contest
from .models import Entry
from .models import Session


from .models import Assignment
from .models import Repertory


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


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'status',
        'category',
        'kind',
        # 'person_id',
        'user',
        # 'convention',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        # 'person',
        # 'convention',
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

class ContestInline(admin.TabularInline):
    model = Contest
    fields = [
        # 'award',
        # 'group',
        'session',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        # 'award',
        # 'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class EntryInline(admin.TabularInline):
    model = Entry
    fields = [
        'session',
        # 'group',
        'base',
        'draw',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        'session',
        # 'group',
    ]
    ordering = [
        # 'group__name',
        'session__convention__year',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class SessionInline(admin.TabularInline):
    model = Session
    fields = [
        'convention',
        'kind',
        # 'num_rounds',
    ]
    autocomplete_fields = [
        'convention',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    readonly_fields = [
        'status',
    ]


