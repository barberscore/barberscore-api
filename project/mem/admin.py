from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin
from reversion.admin import VersionAdmin
from .models import Person
from .models import Group
from .models import Member
from .models import Officer
from .inlines import MemberInline

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
        '__str__',
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
        MemberInline,
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
        ('established_date', 'chartered_date', 'licensed_date',),
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
        MemberInline,
        StateLogInline,
    ]

    save_on_top = True

    ordering = [
        'name',
    ]

    raw_id_fields = [
        'parent',
    ]


@admin.register(Member)
class MemberAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):

    def person_link(self, stream):
        url = reverse("admin:mem_person_change", args=[stream.person.id])
        link = '<a href="{0}">{1}</a>'.format(url, stream.person)
        return mark_safe(link)
    person_link.short_description = 'Person'

    def group_link(self, stream):
        url = reverse("admin:mem_group_change", args=[stream.group.id])
        link = '<a href="{0}">{1}</a>'.format(url, stream.group)
        return mark_safe(link)
    group_link.short_description = 'Group'


    fields = [
        'id',
        'status',
        'part',
        ('start_date', 'end_date'),
        ('person', 'group',),
        ('created', 'modified',),
    ]

    list_display = [
        'status',
        'person_link',
        'group_link',
    ]

    list_select_related = [
        'person',
        'group',
    ]
    list_filter = [
        'status',
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
        'person__last_name',
        'person__first_name',
        'person__nick_name',
        'person__email',
        'person__bhs_id',
        'group__bhs_id',
        'group__name',
    ]

    inlines = [
        StateLogInline,
    ]

    save_on_top = True

    ordering = [
    ]

    raw_id_fields = [
        'person',
        'group',
    ]

@admin.register(Officer)
class OfficerAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):

    def person_link(self, stream):
        url = reverse("admin:mem_person_change", args=[stream.person.id])
        link = '<a href="{0}">{1}</a>'.format(url, stream.person)
        return mark_safe(link)
    person_link.short_description = 'Person'

    def group_link(self, stream):
        url = reverse("admin:mem_group_change", args=[stream.group.id])
        link = '<a href="{0}">{1}</a>'.format(url, stream.group)
        return mark_safe(link)
    group_link.short_description = 'Group'

    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'status',
        'person',
        'group',
        'start_date',
        'end_date',
        'mc_pk'
    ]

    list_display = [
        'status',
        'person_link',
        'group_link',
    ]

    list_filter = [
        'status',
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
        'person__last_name',
        'group__name',
    ]
    autocomplete_fields = [
        'person',
        'group',
    ]
    ordering = [
        'person__last_name',
        'person__first_name',
    ]
