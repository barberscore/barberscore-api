from django.contrib import admin
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin
from reversion.admin import VersionAdmin
from .models import Person
from .models import Group


@admin.register(Person)
class PersonAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'prefix',
        ('first_name', 'middle_name', 'last_name',),
        'suffix',
        'nick_name',
        'email',
        ('birth_date', 'is_deceased'),
        ('home_phone', 'cell_phone', 'work_phone'),
        ('bhs_id', 'mon'),
        ('gender', 'part'),
        ('created', 'modified',),
    ]

    list_display = [
        'last_name',
        'first_name',
        'email',
        'gender',
        'part',
        'status',
    ]

    list_filter = [
        'status',
        'gender',
        'part',
        'is_deceased',
    ]

    readonly_fields = [
        'id',
        'created',
        'modified',
    ]

    fsm_field = [
        'status',
    ]

    search_fields = [
        'last_name',
        'first_name',
        'nick_name',
        'bhs_id',
        'email',
    ]

    inlines = [
        StateLogInline,
    ]

    save_on_top = True

    ordering = [
        'last_name',
        'first_name',
    ]


@admin.register(Group)
class GroupAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
    fields = [
        'id',
        'status',
        'name',
        ('kind', 'gender'),
        ('bhs_id', 'legacy_code'),
        'division',
        ('website', 'email'),
        ('main_phone', 'fax_phone'),
        'facebook',
        'twitter',
        'youtube',
        'pinterest',
        'flickr',
        'instagram',
        'soundcloud',
        'tin',
        ('preferred_name', 'first_alternate_name', 'second_alternate_name'),
        'description',
        'visitor_information',
        ('established_date','chartered_date', 'licensed_date',),
        'parent',
        ('created', 'modified',),
    ]

    list_display = [
        'name',
        'kind',
        'gender',
        'email',
        'status',
    ]

    list_filter = [
        'status',
        'kind',
        'gender',
        'division',
    ]

    readonly_fields = [
        'id',
        'created',
        'modified',
    ]

    fsm_field = [
        'status',
    ]

    search_fields = [
        'name',
        'bhs_id',
        'legacy_code',
        'tin',
    ]

    inlines = [
        StateLogInline,
    ]

    save_on_top = True

    ordering = [
        'name',
    ]

    raw_id_fields = [
        'parent',
    ]