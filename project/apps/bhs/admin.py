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


@admin.register(Convention)
class ConventionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = (
        'id',
        # 'legacy_selection',
        # 'legacy_complete',
        'status',
        'name',
        ('divisions', ),
        ('year', 'season', ),
        ('panel', 'kinds', ),
        ('open_date', 'close_date', ),
        ('start_date', 'end_date', ),
        'owners',
        'venue_name',
        'location',
        'timezone',
        'image',
        'description',
        # 'district',
    )

    list_display = (
        '__str__',
        'year',
        'season',
        # 'district',
        'name',
        # 'location',
        # 'timezone',
        # 'start_date',
        # 'end_date',
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
        # 'district',
        'year',
    )

    fsm_field = [
        'status',
    ]

    search_fields = [
        'name',
    ]

    inlines = [
        # AssignmentInline,
        # SessionInline,
    ]

    readonly_fields = (
        'id',
    )

    autocomplete_fields = [
        # 'group',
        'owners',
    ]

    ordering = (
        '-year',
        'season',
        # 'district',
        # 'group__tree_sort',
    )
    list_select_related = [
        # 'group',
    ]

    save_on_top = True


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
        'group_id',
        'kind',
        'gender',
        'representing',
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
        'name',
        # 'size',
        # 'scope',
        'group_id',
        'representing',
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
        'representing',
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
        'composers',
        'lyricists',
        'arrangers',
        'holders',
        'image',
        'description',
        'notes',
        'created',
        'modified',
        # 'gender',
        # 'tempo',
        # 'is_medley',
        # 'is_learning',
        # 'voicing',
    ]

    list_display = [
        'status',
        'title',
        'arrangers',
        'composers',
        'lyricists',
    ]

    list_editable = [
        'title',
        'arrangers',
        'composers',
        'lyricists',
    ]

    list_filter = [
        'status',
    ]

    inlines = [
        # RepertoryInline,
        StateLogInline,
    ]

    readonly_fields = [
        'created',
        'modified',
    ]

    search_fields = [
        'title',
        'arrangers',
    ]

    ordering = (
        'title',
        'arrangers',
    )


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
        'representing',
        'division',
        'owners',
        ('is_senior', 'is_youth',),
        ('bhs_id', 'mc_pk', 'code',),
        'parent',
        'location',
        'email',
        'phone',
        'website',
        'image',
        'description',
        'participants',
        'chapters',
        'notes',
        ('created', 'modified',),
    ]

    list_filter = [
        'status',
        'kind',
        'gender',
        'is_senior',
        'is_youth',
        'representing',
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
        'representing',
        'division',
        'parent',
        'bhs_id',
        'code',
        'status',
    ]
    list_select_related = [
        'parent',
    ]
    readonly_fields = [
        'id',
        'created',
        'modified',
    ]

    autocomplete_fields = [
        'owners',
        # 'parent',
    ]
    raw_id_fields = [
        'parent',
    ]

    ordering = [
        'tree_sort',
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
        ('first_name', 'middle_name', 'last_name', 'nick_name',),
        ('email', 'bhs_id', 'birth_date',),
        ('home_phone', 'work_phone', 'cell_phone',),
        ('part', 'gender',),
        ('is_deceased', 'is_honorary', 'is_suspended', 'is_expelled',),
        'mc_pk',
        'spouse',
        'location',
        'representing',
        'website',
        'image',
        'description',
        'notes',
        ('created', 'modified',),
        # 'user',
    ]

    list_display = [
        'common_name',
        'email',
        'cell_phone',
        'part',
        'gender',
        'status',
    ]

    list_filter = [
        'status',
        'gender',
        'part',
        'is_deceased',
    ]

    raw_id_fields = [
        # 'user',
    ]

    readonly_fields = [
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        'is_deceased',
        'bhs_id',
        'mc_pk',
        'birth_date',
        'part',
        'mon',
        'gender',
        'home_phone',
        'work_phone',
        'cell_phone',
        'common_name',
        'is_deceased',
        'is_honorary',
        'is_suspended',
        'is_expelled',
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

    # autocomplete_fields = [
    #     'user',
    # ]

    save_on_top = True

    inlines = [
        # MemberInline,
        # AssignmentInline,
        # PanelistInline,
        StateLogInline,
    ]

    ordering = [
        'last_name',
        'first_name',
    ]
    # readonly_fields = [
    #     'common_name',
    # ]

