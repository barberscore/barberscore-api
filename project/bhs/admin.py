# Django
# Third-Party
from django.contrib import admin
from .models import (
    Membership,
)

@admin.register(Membership)
class Membership(admin.ModelAdmin):
    fields = [
        'id',
        'first_name',
        'last_name',
    ]

    readonly_fields = [
        'id',
        'first_name',
        'last_name',
    ]
