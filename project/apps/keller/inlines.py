
# Django
from django.contrib import admin

# Local
from .models import Flat


class FlatInline(admin.TabularInline):
    model = Flat
    fields = [
        'selection',
        'complete',
        'score',
    ]
    extra = 0
    show_change_link = True
    classes = [
        'collapse',
    ]
    raw_id_fields = [
        'selection',
        'complete',
        'score',
    ]
