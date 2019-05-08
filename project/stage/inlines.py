from django.contrib import admin

# Local
from .models import Grid

class GridInline(admin.TabularInline):
    model = Grid
    fields = [
        'period',
        'num',
        'onstage',
        'start',
        'round',
        'renditions',
    ]
    autocomplete_fields = [
        'round',
    ]
    show_change_link = True
    extra = 0
    ordering = [
        'period',
        'num',
    ]
    classes = [
        'collapse',
    ]
