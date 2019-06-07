
# Django
from django.contrib import admin

# Local
from .models import Contest
from .models import Contestant
from .models import Entry
from .models import Session


class ContestInline(admin.TabularInline):
    model = Contest
    fields = [
        'award',
        # 'group',
        'session',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        'award',
        # 'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class ContestantInline(admin.TabularInline):
    model = Contestant
    fields = [
        'entry',
        'contest',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        # 'contest',
        'entry',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    raw_id_fields = [
        'contest',
    ]


class EntryInline(admin.TabularInline):
    model = Entry
    fields = [
        'session',
        'group',
        'base',
        'draw',
        'status',
    ]
    readonly_fields = [
        'status',
    ]
    autocomplete_fields = [
        'session',
        'group',
    ]
    ordering = [
        'group__name',
        'session__convention__year',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]

