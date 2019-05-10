from django.contrib import admin
from django.utils import timezone

from .models import Grid
from .models import Venue
from fsm_admin.mixins import FSMTransitionMixin
from django_fsm_log.admin import StateLogInline



@admin.register(Venue)
class VenueAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = (
        'id',
        'name',
        'status',
        'city',
        'state',
        'airport',
        'timezone',
    )

    list_display = [
        'name',
        'city',
        'state',
        'airport',
        'timezone',
    ]

    inlines = [
        StateLogInline,
    ]


    list_filter = (
        'status',
    )

    search_fields = [
        'name',
        'city',
        'state',
    ]

    readonly_fields = [
        'id',
    ]


@admin.register(Grid)
class GridAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        # 'name',
        'status',
        'period',
        'num',
        'onstage',
        'start',
        'venue',
        'round',
        # 'appearance',
        'renditions',
    ]
    list_display = [
        'status',
        'onstage',
        'start',
    ]
    list_filter = (
        'status',
        'onstage',
        'period',
    )
    readonly_fields = [
    ]
    autocomplete_fields = [
        'round',
        'venue',
        # 'appearance',
    ]
    ordering = [
        'round',
        'period',
        'num',
    ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        try:
            timezone.activate(obj.venue.timezone)
        except AttributeError:
            pass
        return super().change_view(request, object_id, form_url, extra_context)

