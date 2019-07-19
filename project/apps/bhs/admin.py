from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin


# Django
from django.contrib import admin
from reversion.admin import VersionAdmin
# Local


from .models import Award
from .models import Person
from .models import Group
from .models import Member
from .models import Officer
from .models import Chart
from .models import Repertory

from .inlines import RepertoryInline

from .inlines import MemberInline
from .inlines import OfficerInline

# from .models import Human
# from .models import Join
# from .models import Membership
# from .models import Role
# from .models import Structure
# from .models import Subscription

# from .inlines import JoinInline
# from .inlines import RoleInline
# from .inlines import SubscriptionInline
# from .inlines import StructureInline

from .filters import MCListFilter
from .filters import DistrictListFilter


admin.site.disable_action('delete_selected')


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)


@admin.register(Award)
class AwardAdmin(FSMTransitionMixin, admin.ModelAdmin):
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
        'name',
        # 'size',
        # 'scope',
        'group_id',
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
        # AwardQualifierLevelFilter,
        DistrictListFilter,
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
class ChartAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
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
        RepertoryInline,
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
class GroupAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
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
        'division',
        'owners',
        ('is_senior', 'is_youth',),
        ('bhs_id', 'mc_pk', 'code',),
        'parent',
        ('international', 'district', 'chapter',),
        'location',
        'email',
        'phone',
        'website',
        'image',
        'description',
        'participants',
        'notes',
        ('created', 'modified',),
    ]

    list_filter = [
        'status',
        'kind',
        'gender',
        'is_senior',
        'is_youth',
        DistrictListFilter,
        'division',
        MCListFilter,
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
        'international',
        'district',
        'chapter',
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
            OfficerInline,
            # MemberInline,
            RepertoryInline,
            # EntryInline,
            StateLogInline,
        ],
        'Quartet': [
            MemberInline,
            OfficerInline,
            RepertoryInline,
            # EntryInline,
            StateLogInline,
        ],
        'VLQ': [
            MemberInline,
            OfficerInline,
            RepertoryInline,
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
        ).prefetch_related('members')


@admin.register(Member)
class MemberAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]
    fields = [
        'id',
        'status',
        'person',
        'group',
        'part',
        'mc_pk',
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
        'created',
        'modified',
    ]
    list_display = [
        'person',
        'group',
        'part',
        'status',
    ]
    readonly_fields = [
        'id',
        'part',
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
        'created',
        'modified',
    ]

    autocomplete_fields = [
        'person',
        'group',
    ]
    search_fields = [
        'person__first_name',
        'person__last_name',
        'group__name',
        'person__bhs_id',
        'group__bhs_id',
    ]
    list_filter = [
        'status',
        MCListFilter,
        'group__kind',
        'group__status',
        'part',
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
        'created',
    ]
    list_select_related = [
        'person',
        'group',
    ]
    inlines = [
        StateLogInline,
    ]



@admin.register(Officer)
class OfficerAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'status',
        'person',
        'office',
        'group',
        'start_date',
        'end_date',
        'mc_pk'
    ]

    list_display = [
        'person',
        'office',
        'group',
        'status',
    ]
    readonly_fields = [
        'id',
    ]
    list_select_related = [
        'person',
        'group',
    ]
    list_filter = [
        'status',
        MCListFilter,
        'group__kind',
        'office',
    ]
    inlines = [
        StateLogInline,
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
        'office',
        'person__last_name',
        'person__first_name',
    ]



@admin.register(Person)
class PersonAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
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
        'district',
        'website',
        'image',
        'description',
        'notes',
        ('created', 'modified',),
        'user',
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
        'user',
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
        MemberInline,
        OfficerInline,
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


@admin.register(Repertory)
class RepertoryAdmin(VersionAdmin, FSMTransitionMixin, admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'status',
        'group',
        'chart',
    ]

    list_display = [
        'group',
        'chart',
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'id',
    ]

    autocomplete_fields = [
        'group',
        'chart',
    ]

    inlines = [
        StateLogInline,
    ]

    search_fields = [
        'group__name',
        'chart__title',
    ]


# @admin.register(Human)
# class HumanAdmin(ReadOnlyAdmin):
#     fields = [
#         'id',
#         ('first_name', 'middle_name', 'last_name', 'nick_name',),
#         ('email', 'bhs_id', 'birth_date',),
#         ('home_phone', 'work_phone', 'cell_phone',),
#         ('part', 'gender',),
#         ('is_deceased', 'is_honorary', 'is_suspended', 'is_expelled',),
#         ('merged_id', 'deleted_id',),
#         ('created', 'modified',),
#     ]

#     list_display = [
#         '__str__',
#         # 'first_name',
#         # 'middle_name',
#         # 'last_name',
#         # 'nick_name',
#         'email',
#         'home_phone',
#         'cell_phone',
#         'work_phone',
#         'bhs_id',
#         'birth_date',
#         'gender',
#         'part',
#         'created',
#         'modified',
#     ]

#     readonly_fields = [
#         'id',
#         'first_name',
#         'middle_name',
#         'last_name',
#         'nick_name',
#         'email',
#         'home_phone',
#         'cell_phone',
#         'work_phone',
#         'bhs_id',
#         'birth_date',
#         'gender',
#         'part',
#         'mon',
#         'is_deceased',
#         'is_honorary',
#         'is_suspended',
#         'is_expelled',
#         'created',
#         'modified',
#     ]

#     list_filter = [
#         'gender',
#         'part',
#         'is_deceased',
#         'is_honorary',
#         'is_suspended',
#         'is_expelled',
#     ]

#     search_fields = [
#         'first_name',
#         'last_name',
#         'bhs_id',
#         'email',
#     ]

#     inlines = [
#         RoleInline,
#         SubscriptionInline,
#     ]

#     ordering = (
#         'last_name',
#         'first_name',
#     )


# @admin.register(Structure)
# class StructureAdmin(ReadOnlyAdmin):
#     fields = [
#         'id',
#         'name',
#         'kind',
#         'gender',
#         'division',
#         'bhs_id',
#         'preferred_name',
#         'chapter_code',
#         'phone',
#         'email',
#         'website',
#         'facebook',
#         'twitter',
#         'established_date',
#         'status',
#         'parent',
#         'created',
#         'modified',
#     ]

#     list_display = [
#         '__str__',
#         'name',
#         'kind',
#         'gender',
#         'bhs_id',
#         'preferred_name',
#         'chapter_code',
#         'phone',
#         'email',
#         'established_date',
#         'status',
#         'parent',
#         'created',
#         'modified',
#     ]

#     readonly_fields = [
#         'id',
#         'name',
#         'kind',
#         'gender',
#         'division',
#         'bhs_id',
#         'preferred_name',
#         'chapter_code',
#         'phone',
#         'email',
#         'website',
#         'facebook',
#         'twitter',
#         'established_date',
#         'status',
#         'parent',
#         'created',
#         'modified',
#     ]

#     list_filter = [
#         'kind',
#         'gender',
#         'division',
#     ]
#     search_fields = [
#         'name',
#         'bhs_id',
#         'chapter_code',
#     ]

#     list_select_related = [
#         'parent',
#     ]

#     ordering = (
#         '-created',
#     )

#     INLINES = {
#         'organization': [
#             RoleInline,
#         ],
#         'district': [
#             RoleInline,
#         ],
#         'group': [
#             RoleInline,
#         ],
#         'chapter': [
#             RoleInline,
#             StructureInline,
#         ],
#         'chorus': [
#             RoleInline,
#         ],
#         'quartet': [
#             RoleInline,
#             JoinInline,
#         ],
#     }

#     def get_inline_instances(self, request, obj=None):
#         inline_instances = []
#         inlines = self.INLINES[obj.kind]
#         # try:
#         #     inlines = self.INLINES[obj.kind]
#         # except AttributeError:
#         #     return inline_instances
#         # except KeyError:
#         #     # Defaults to Group
#         #     inlines = self.INLINES['Group']

#         for inline_class in inlines:
#             inline = inline_class(self.model, self.admin_site)
#             inline_instances.append(inline)
#         return inline_instances

#     def get_formsets(self, request, obj=None):
#         for inline in self.get_inline_instances(request, obj):
#             yield inline.get_formset(request, obj)


# @admin.register(Membership)
# class MembershipAdmin(ReadOnlyAdmin):
#     fields = [
#         'structure',
#         'code',
#         'status',
#         'created',
#         'modified',
#     ]

#     list_display = [
#         'structure',
#         'code',
#         'status',
#         'created',
#         'modified',
#     ]

#     list_select_related = [
#         'structure',
#     ]

#     list_filter = [
#         'structure__kind',
#         'code',
#         'status',
#     ]

#     readonly_fields = [
#         'structure',
#         'code',
#         'status',
#         'created',
#         'modified',
#     ]

#     inlines = [
#         JoinInline,
#     ]

#     ordering = (
#         'structure__name',
#         'code',
#     )

#     search_fields = [
#         'structure__name',
#     ]


# @admin.register(Subscription)
# class SubscriptionAdmin(ReadOnlyAdmin):
#     fields = [
#         '__str__',
#         'items_editable',
#         'current_through',
#         'status',
#         'created',
#         'modified',
#     ]

#     list_display = [
#         '__str__',
#         'items_editable',
#         'current_through',
#         'status',
#         'created',
#         'modified',
#     ]

#     readonly_fields = [
#         '__str__',
#         'items_editable',
#         'current_through',
#         'status',
#         'created',
#         'modified',
#     ]

#     list_filter = [
#         'status',
#     ]
#     search_fields = (
#         'human__last_name',
#         'human__first_name',
#         'human__bhs_id',
#     )

#     ordering = (
#         'human__last_name',
#     )

#     inlines = [
#         JoinInline,
#     ]


# @admin.register(Role)
# class RoleAdmin(ReadOnlyAdmin):
#     fields = [
#         'name',
#         'human',
#         'structure',
#         'start_date',
#         'end_date',
#         'abbv',
#         'officer_roles_id',
#         'created',
#         'modified',
#     ]

#     list_display = [
#         'name',
#         'human',
#         'structure',
#         'start_date',
#         'end_date',
#         'abbv',
#         'created',
#         'modified',
#     ]

#     list_select_related = [
#         'structure',
#         'human',
#     ]
#     list_filter = [
#         'name',
#     ]

#     readonly_fields = [
#         'name',
#         'human',
#         'structure',
#         'start_date',
#         'end_date',
#         'abbv',
#         'officer_roles_id',
#         'created',
#         'modified',
#     ]

#     ordering = (
#         'structure__name',
#     )

#     search_fields = [
#         'structure__name',
#         'human__first_name',
#         'human__last_name',
#         'human__bhs_id',
#     ]


# @admin.register(Join)
# class JoinAdmin(ReadOnlyAdmin):
#     fields = [
#         'id',
#         'status',
#         'paid',
#         'part',
#         'subscription',
#         'membership',
#         'established_date',
#         'inactive_date',
#         'inactive_reason',
#         'created',
#         'modified',
#     ]

#     list_display = [
#         'id',
#         'status',
#         'paid',
#         'subscription',
#         'membership',
#         'part',
#         'inactive_date',
#         'inactive_reason',
#         'established_date',
#         'created',
#         'modified',
#     ]

#     list_select_related = [
#         'subscription',
#         'membership',
#     ]
#     readonly_fields = [
#         'id',
#         'status',
#         'paid',
#         'subscription',
#         'membership',
#         'part',
#         'inactive_date',
#         'inactive_reason',
#         'established_date',
#         'created',
#         'modified',
#     ]

#     list_display_links = [
#         'id',
#     ]

#     list_filter = [
#         'status',
#         'paid',
#         'part',
#         'structure__kind',
#         'inactive_date',
#     ]

#     search_fields = [
#         'subscription__human__last_name',
#         'subscription__human__bhs_id',
#         # 'membership__structure__name',
#         # 'membership__structure__bhs_id',
#     ]
