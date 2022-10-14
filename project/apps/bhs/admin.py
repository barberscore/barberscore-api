from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin
from django_object_actions import DjangoObjectActions


# Django
from django.contrib import admin
from reversion.admin import VersionAdmin
from django.conf import settings

# Local


from .models import Award
from .models import Person
from .models import Group
from .models import Chart
from .models import Convention

from .tasks import update_group_from_source

admin.site.disable_action('delete_selected')


@admin.register(Award)
class AwardAdmin(VersionAdmin, FSMTransitionMixin):
    fsm_field = [
        'status',
    ]
    save_on_top = True
    fields = [
        'id',
        'name',
        'status',
        'kind',
        'gender',
        'district',
        'division',
        'age',
        'level',
        'season',
        'is_single',
        'is_novice',
        ('threshold', 'minimum', 'spots',),
        'description',
        'notes',
    ]

    list_display = [
        # 'district',

        'name',
        # 'size',
        # 'scope',
        'district',
        'division',
        'kind',
        'age',
        'gender',
        'level',
        # 'size',
        # 'scope',
        # 'season',
        # 'rounds',
        # 'threshold',
        # 'advance',
        # 'minimum',
        'status',
    ]

    # list_editable = [
    #     'threshold',
    #     'advance',
    #     'minimum',
    # ]
    list_filter = [
        'status',
        'kind',
        'level',
        'district',
        'division',
        'age',
        'gender',
        'season',
        'is_single',
        'is_novice',
    ]

    readonly_fields = [
        'id',
    ]

    search_fields = [
        'name',
    ]

    ordering = (
        'tree_sort',
    )


@admin.register(Chart)
class ChartAdmin(VersionAdmin, FSMTransitionMixin):
    fsm_field = [
        'status',
    ]

    fields = [
        'status',
        'title',
        'arrangers',

        'composers',
        'lyricists',
        'holders',
        'description',
        'notes',
        'image',

        'created',
        'modified',
    ]

    list_display = [
        'status',
        'title',
        'arrangers',
    ]

    list_filter = [
        'status',
    ]

    readonly_fields = [
        'created',
        'modified',
    ]

    search_fields = [
        'title',
        'arrangers',
    ]

    ordering = [
        'title',
        'arrangers',
    ]


@admin.register(Convention)
class ConventionAdmin(VersionAdmin, FSMTransitionMixin):
    fields = (
        'id',
        # 'legacy_selection',
        # 'legacy_complete',
        'status',
        'name',
        ('district', 'divisions', ),
        'district_display_name',
        ('year', 'season', ),
        ('panel', 'kinds', ),
        ('open_date', 'close_date', ),
        ('start_date', 'end_date', ),
        'owners',
        'venue_name',
        'location',
        'timezone',
        'image',
        'bbstix_report',
        'bbstix_practice_report',
        'persons',
        'description',
    )

    list_display = (
        'year',
        'district',
        'season',
        'divisions',
        'name',
        'location',
        # 'timezone',
        'start_date',
        'end_date',
        # 'status',
    )

    list_editable = [
        'name',
        # 'location',
        # 'start_date',
        # 'end_date',
    ]

    list_filter = (
        'status',
        'season',
        'district',
        'year',
    )

    fsm_field = [
        'status',
    ]

    search_fields = [
        'name',
    ]

    inlines = [
        StateLogInline,
    ]

    readonly_fields = (
        'id',
    )

    autocomplete_fields = [
        'persons',
        'owners',
    ]

    ordering = [
        '-year',
        'season',
        'district',
    ]
    list_select_related = [
    ]

    save_on_top = True

    class Media:
        js = ('bhs/js/admin/build_convention.js',)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            convention = Convention.objects.get(id=object_id)
            if convention.status == 0:
                extra_context['show_build_convention'] = True

        return super(ConventionAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.image:
            if settings.DISTRICT_DEFAULT_LOGOS[obj.district]:
                obj.image = settings.DISTRICT_DEFAULT_LOGOS[obj.district]
        super().save_model(request, obj, form, change)

@admin.register(Group)
class GroupAdmin(DjangoObjectActions, VersionAdmin, FSMTransitionMixin):
    save_on_top = True
    fsm_field = [
        'status',
    ]
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'status',
            ),
        }),
        ('Group Info (primarily from Member Center)', {
            'fields': (
                'name',
                'kind',
                'gender',
                'district',
                'division',
                'bhs_id',
                'code',
                'is_senior',
                'is_youth',
            ),
        }),
        ('Group Info (expanded)', {
            'fields': (
                'description',
                'image',
            ),
        }),
        ('Repertory', {
            'fields': (
                'charts',
            ),
        }),
        ('Misc', {
            'fields': (
                'source_id',
                'owners',
                'location',
                'website',
                'notes',
                'created',
                'modified',
            ),
        }),
    )

    list_filter = [
        'status',
        'kind',
        'gender',
        'is_senior',
        'is_youth',
        'district',
        'division',
    ]

    search_fields = [
        'name',
        'bhs_id',
        'code',
        'owners__email',
    ]

    list_display = [
        'name',
        'kind',
        'gender',
        'district',
        'division',
        'bhs_id',
        'code',
        'status',
    ]
    list_select_related = [
    ]
    readonly_fields = [
        'id',
        'created',
        'modified',
    ]

    autocomplete_fields = [
        'owners',
        'charts',
    ]
    raw_id_fields = [
    ]

    ordering = [
        'kind',
        'name',
    ]

    INLINES = {
        'International': [
            # AwardInline,
            # OfficerInline,
            # ConventionInline,
            StateLogInline,
        ],
        'District': [
            # AwardInline,
            # OfficerInline,
            # ConventionInline,
            # ActiveChapterInline,
            # ActiveQuartetInline,
            StateLogInline,
        ],
        'Noncompetitive': [
            # OfficerInline,
            # GroupInline,
            StateLogInline,
        ],
        'Affiliate': [
            # OfficerInline,
            # GroupInline,
            StateLogInline,
        ],
        'Chapter': [
            # ActiveChorusInline,
            # OfficerInline,
            StateLogInline,
        ],
        'Chorus': [
            # MemberInline,
            # RepertoryInline,
            # EntryInline,
            StateLogInline,
        ],
        'Quartet': [
            # MemberInline,
            # RepertoryInline,
            # EntryInline,
            StateLogInline,
        ],
        'VLQ': [
            # MemberInline,
            # RepertoryInline,
            # EntryInline,
            StateLogInline,
        ],
    }

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        try:
            inlines = self.INLINES[obj.KIND[obj.kind]]
        except AttributeError:
            return inline_instances

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            inline_instances.append(inline)
        return inline_instances

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(
            request
        )
        # ).prefetch_related('members')

    def update_from_source(self, request, obj):
        return update_group_from_source(obj)
    update_from_source.label = "Update"
    update_from_source.short_description = "Update from Source Database"

    change_actions = ('update_from_source', )


@admin.register(Person)
class PersonAdmin(VersionAdmin, FSMTransitionMixin):
    fields = [
        'id',
        'status',
        ('name', 'first_name', 'last_name',),
        ('email', 'bhs_id',),
        ('home_phone', 'work_phone', 'cell_phone',),
        ('part', 'gender',),
        'district',
        'source_id',
        'image',
        'description',
        'notes',
        ('created', 'modified',),
        'owners',
    ]

    list_display = [

        'name',
        # 'district',
        'email',
        # 'cell_phone',
        # 'part',
        # 'gender',
        # 'bhs_id',
    ]

    list_filter = [
        'status',
        'district',
        'gender',
        'part',
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
        'last_name',
        'first_name',
        'bhs_id',
        'email',
        'bhs_id',
    ]

    autocomplete_fields = [
        'owners',
    ]

    save_on_top = True

    inlines = [
    ]

    ordering = [
        'last_name',
        'first_name',
    ]
