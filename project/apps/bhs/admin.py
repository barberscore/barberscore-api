from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin


# Django
from django.contrib import admin
from reversion.admin import VersionAdmin

# Local


from .models import Award
from .models import Person
from .models import Group
from .models import Chart
from .models import Convention


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
        ('threshold', 'minimum', 'advance', 'spots',),
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
        ('year', 'season', ),
        ('panel', 'kinds', ),
        ('open_date', 'close_date', ),
        ('start_date', 'end_date', ),
        'owners',
        'venue_name',
        'location',
        'timezone',
        'image',
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


@admin.register(Group)
class GroupAdmin(VersionAdmin, FSMTransitionMixin):
    save_on_top = True
    fsm_field = [
        'status',
    ]
    fields = [
        'id',
        'name',
        'status',
        'kind',
        'gender',
        'district',
        'division',
        'owners',
        ('is_senior', 'is_youth',),
        ('bhs_id', 'source_id', 'code',),
        'location',
        'website',
        'image',
        'description',
        'participants',
        'chapters',
        'charts',
        'notes',
        ('created', 'modified',),
    ]

    list_filter = [
        # 'district',

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
    ]

    list_display = [
        'name',
        'kind',
        'gender',
        'is_senior',
        'is_youth',
        'chapters',
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


@admin.register(Person)
class PersonAdmin(VersionAdmin, FSMTransitionMixin):
    fields = [
        'id',
        'status',
        ('name', 'first_name', 'last_name',),
        ('email', 'bhs_id',),
        ('home_phone', 'work_phone', 'cell_phone',),
        ('part', 'gender',),
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
