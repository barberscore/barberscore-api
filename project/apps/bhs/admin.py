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
        'organization',
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
        'get_organization_abbr',
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
        'organization',
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

    def get_organization_abbr(self, obj):
        if obj.organization:
            return obj.organization.abbreviation
        else:
            return None
    get_organization_abbr.short_description = 'ORG'


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
        'organization',
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
        'get_organization_abbr',
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
        'organization',
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
        '-start_date',
        'season',
        'district',
    ]
    list_select_related = [
    ]

    save_on_top = True

    class Media:
        js = ('bhs/js/admin/build_convention.js', 'bhs/js/admin/convention_owners.js',)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            convention = Convention.objects.get(id=object_id)
            if convention.status == 0:
                extra_context['show_build_convention'] = True

        return super(ConventionAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.image:
            logo = settings.DISTRICT_DEFAULT_LOGOS.get(obj.district)
            if logo:
                obj.image = logo
        super().save_model(request, obj, form, change)

    def get_organization_abbr(self, obj):
        if obj.organization:
            return obj.organization.abbreviation
        else:
            return None
    get_organization_abbr.short_description = 'ORG'

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
                'organization',
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
        'organization',
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


# ----------------------------------------------------------------------
# User administration
#
# Re-registers the rest_framework_jwt UserAdmin so that only super users
# (see settings.SUPER_USERS and apps.bhs.owners.is_super_user) may set
# passwords, grant staff access, or designate other super users.
# ----------------------------------------------------------------------

# Django
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import PermissionDenied

# Third-Party
from rest_framework_jwt.admin import UserAdmin as JWTUserAdmin

# Local
from .owners import is_super_user

User = get_user_model()


class UserSuperChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        required=False,
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        ),
    )

    is_superuser_flag = forms.BooleanField(
        label="Super user",
        required=False,
        help_text=(
            "Super users can set passwords, grant staff access, and "
            "designate other super users."
        ),
    )

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'is_superuser_flag' in self.fields:
            app_metadata = getattr(self.instance, 'app_metadata', None) or {}
            self.fields['is_superuser_flag'].initial = bool(
                app_metadata.get('is_superuser')
            )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        return self.initial.get('password')

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'is_superuser_flag' in self.cleaned_data:
            app_metadata = user.app_metadata or {}
            app_metadata['is_superuser'] = self.cleaned_data['is_superuser_flag']
            user.app_metadata = app_metadata
        if commit:
            user.save()
            self.save_m2m()
        return user


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(JWTUserAdmin):
    form = UserSuperChangeForm

    superuser_fieldsets = JWTUserAdmin.fieldsets + (
        ('Access', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser_flag',
                'password',
            ),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if obj and is_super_user(request.user):
            return self.superuser_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and not is_super_user(request.user):
            # Strip the privileged fields so they can neither be
            # rendered nor submitted by non-super users.
            form.base_fields.pop('is_superuser_flag', None)
            form.base_fields.pop('password', None)
        return form

    def user_change_password(self, request, id, form_url=''):
        if not is_super_user(request.user):
            raise PermissionDenied
        return super().user_change_password(request, id, form_url)
