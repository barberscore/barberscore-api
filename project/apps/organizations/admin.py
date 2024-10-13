from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin
from django_object_actions import DjangoObjectActions


# Django
from django.contrib import admin
from reversion.admin import VersionAdmin
from django.conf import settings
from django.contrib.admin.filters import RelatedOnlyFieldListFilter

# Local


# Models
from .models import Organization
from .models import District
from .models import Division


if 'delete_selected' in admin.site.actions:
    admin.site.disable_action('delete_selected')

@admin.register(Organization)
class OrganizationAdmin(VersionAdmin, FSMTransitionMixin):
    save_on_top = True

    ordering = ['name']

    # list_display = [
    #     '__str__',
    #     'name',
    # ]

    fields = [
        'id',
        'name',
        'abbreviation',
        'logo',
        'district_nomen',
        'division_nomen',
        'drcj_nomen',
        'default_owners',
    ]

    # list_display = [
    #     # 'district',

    #     'name',
    #     # 'size',
    #     # 'scope',
    #     'district',
    #     'division',
    #     'kind',
    #     'age',
    #     'gender',
    #     'level',
    #     # 'size',
    #     # 'scope',
    #     # 'season',
    #     # 'rounds',
    #     # 'threshold',
    #     # 'advance',
    #     # 'minimum',
    #     'status',
    # ]

    # # list_editable = [
    # #     'threshold',
    # #     'advance',
    # #     'minimum',
    # # ]
    # list_filter = [
    #     'status',
    #     'kind',
    #     'level',
    #     'district',
    #     'division',
    #     'age',
    #     'gender',
    #     'season',
    #     'is_single',
    #     'is_novice',
    # ]

    autocomplete_fields = [
        'default_owners',
    ]

    readonly_fields = [
        'id',
    ]

    # search_fields = [
    #     'name',
    # ]

    # ordering = (
    #     'tree_sort',
    # )


@admin.register(District)
class DistrictAdmin(VersionAdmin, FSMTransitionMixin):
    save_on_top = True

    ordering = ['name']

    list_display = [
        'name',
        'organization',
    ]

    list_filter = [
        'organization',
    ]

    search_fields = [
        'name',
        'organization',
    ]


    # fsm_field = [
    #     'status',
    # ]

    # fields = [
    #     'status',
    #     'title',
    #     'arrangers',

    #     'composers',
    #     'lyricists',
    #     'holders',
    #     'description',
    #     'notes',
    #     'image',

    #     'created',
    #     'modified',
    # ]

    # readonly_fields = [
    #     'created',
    #     'modified',
    # ]


@admin.register(Division)
class DivisionAdmin(VersionAdmin, FSMTransitionMixin):
    save_on_top = True

    ordering = ['name']

    list_display = [
        'name',
        'district',
        'organization',
    ]

    list_filter = [
        'district',
    ]

    search_fields = [
        'name',
        'district',
        'organization',
    ]

    def organization(self, obj):
        return obj.district.organization

    # fields = (
    #     'id',
    #     # 'legacy_selection',
    #     # 'legacy_complete',
    #     'status',
    #     'name',
    #     ('district', 'divisions', ),
    #     'district_display_name',
    #     ('year', 'season', ),
    #     ('panel', 'kinds', ),
    #     ('open_date', 'close_date', ),
    #     ('start_date', 'end_date', ),
    #     'owners',
    #     'venue_name',
    #     'location',
    #     'timezone',
    #     'image',
    #     'bbstix_report',
    #     'bbstix_practice_report',
    #     'persons',
    #     'description',
    # )

    # list_display = (
    #     'year',
    #     'district',
    #     'season',
    #     'divisions',
    #     'name',
    #     'location',
    #     # 'timezone',
    #     'start_date',
    #     'end_date',
    #     # 'status',
    # )

    # list_editable = [
    #     'name',
    #     # 'location',
    #     # 'start_date',
    #     # 'end_date',
    # ]

    # list_filter = (
    #     'status',
    #     'season',
    #     'district',
    #     'year',
    # )

    # fsm_field = [
    #     'status',
    # ]

    # search_fields = [
    #     'name',
    # ]

    # inlines = [
    #     StateLogInline,
    # ]

    # readonly_fields = (
    #     'id',
    # )

    # autocomplete_fields = [
    #     'persons',
    #     'owners',
    # ]

    # list_select_related = [
    # ]
