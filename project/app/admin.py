# Third-Party
from mptt.admin import MPTTModelAdmin

# Django
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group as AuthGroup

# Local
from .inlines import (
    # AssignmentInline,
    # AwardInline,
    ContestantInline,
    ContestInline,
    # ConventionInline,
    HostInline,
    PerformanceInline,
    PerformerInline,
    RoundInline,
    ScoreInline,
    SessionInline,
    # SongInline,
    SubmissionInline,
)
from .models import (
    Assignment,
    Award,
    Catalog,
    Contest,
    ContestScore,
    Contestant,
    ContestantScore,
    Convention,
    Entity,
    Host,
    Office,
    Officer,
    Membership,
    Performance,
    PerformanceScore,
    Performer,
    PerformerScore,
    Person,
    Round,
    Score,
    Session,
    Slot,
    Song,
    SongScore,
    Submission,
    User,
    Venue,
)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'short_name',
        'kind',
    ]
    search_fields = [
        'nomen',
    ]

    list_filter = [
        'status',
        'kind',
    ]


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'office',
        'membership',
    ]
    list_filter = [
        'office__name',
    ]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'person',
        'entity',
    ]
    search_fields = [
        'nomen',
    ]
    list_filter = [
        'status',
        'part',
        'entity__kind',
    ]


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'status',
        'category',
        'kind',
        'slot',
        'bhs_id',
        'convention',
        'person',
    ]

    list_display = [
        'nomen',
        'status',
        'kind',
        'category',
        'person',
        'convention',
    ]

    list_filter = (
        'status',
        'category',
        'kind',
    )

    list_select_related = [
        'convention',
        'person',
    ]

    search_fields = [
        'nomen',
    ]

    raw_id_fields = (
        'convention',
        'person',
    )

    readonly_fields = [
        'nomen',
    ]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'is_manual',
        'kind',
        'championship_season',
        'qualifier_season',
        'size',
        'size_range',
        'scope',
        'scope_range',
        'idiom',
        ('is_primary', 'is_improved', 'is_novice'),
        ('is_multi', 'is_qualification_required',),
        'championship_rounds',
        'qualifier_rounds',
        'threshold',
        'minimum',
        'advance',
    ]

    list_display = [
        'nomen',
        'status',
        'is_primary',
        'is_qualification_required',
        'is_manual',
        'kind',
        'size',
        'size_range',
        'scope',
        'scope_range',
        'is_improved',
        'is_novice',
        'idiom',
        'championship_season',
        'qualifier_season',
    ]

    list_filter = [
        'status',
        'is_primary',
        'is_qualification_required',
        'kind',
        'championship_season',
        'qualifier_season',
        'size',
        'scope',
        'is_manual',
        'is_novice',
        'is_improved',
    ]

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'kind',
        '-is_primary',
        'is_improved',
        'size',
        'scope',
        'is_novice',
        'idiom',
    )


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):

    fields = [
        'nomen',
        'status',
        'bhs_id',
        'title',
        'published',
        'arranger',
        'arranger_fee',
        'difficulty',
        'gender',
        'tempo',
        'is_medley',
        'is_learning',
        'voicing',
    ]

    list_display = [
        'nomen',
        'status',
        'title',
        'arranger',
    ]

    list_editable = [
        'title',
        'arranger',
    ]

    list_filter = [
        'status',
    ]

    # inlines = [
    #     SubmissionInline,
    # ]

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'nomen',
    )


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'award',
        'session',
        'is_qualifier',
        'num_rounds',
    ]

    list_display = (
        'nomen',
        'session',
    )

    list_filter = [
        'status',
        'award__kind',
        'award__is_primary',
        'is_qualifier',
    ]

    save_on_top = True

    inlines = [
        ContestantInline,
    ]

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'award',
        'session',
    ]

    search_fields = [
        'nomen',
    ]


@admin.register(ContestScore)
class ContestScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):

    fields = [
        'status',
        'performer',
        'contest',
    ]

    list_filter = (
        'status',
    )

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'performer',
        'contest',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'nomen',
    )


@admin.register(ContestantScore)
class ContestantScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):

    fields = (
        'name',
        'status',
        'kind',
        'level',
        'venue',
        'bhs_id',
        'is_prelims',
        'risers',
        'start_date',
        'end_date',
        'year',
        'season',
        # 'drcj',
    )

    list_display = (
        'nomen',
        'name',
        'panel',
        'season',
        'is_prelims',
        # 'status',
        'start_date',
        'end_date',
        'level',
        # 'venue',
    )

    list_filter = (
        'status',
        'level',
        'kind',
        'season',
        'year',
    )

    fsm_field = [
        'status',
    ]

    search_fields = (
        'nomen',
    )

    inlines = [
        HostInline,
        SessionInline,
    ]

    readonly_fields = (
        'nomen',
    )

    raw_id_fields = [
        # 'drcj',
        'venue',
    ]

    ordering = (
        '-year',
        'level',
    )

    save_on_top = True


@admin.register(Entity)
class EntityAdmin(MPTTModelAdmin):
    exclude = [
        'level',
    ]
    # fields = [
    #     'name',
    #     'status',
    #     'parent',
    #     'level',
    #     'kind',
    #     'code',
    #     'start_date',
    #     'end_date',
    #     'short_name',
    #     'long_name',
    #     'location',
    #     'representative',
    #     'spots',
    #     'website',
    #     'facebook',
    #     'twitter',
    #     'email',
    #     'phone',
    #     'picture',
    #     'description',
    #     'notes',
    # ]

    list_filter = [
        'status',
        'kind',
    ]

    search_fields = [
        'nomen',
    ]

    # list_display = [
    #     'nomen',
    #     'status',
    #     'code',
    #     'short_name',
    #     'long_name',
    #     'level',
    #     'kind',
    # ]

    # inlines = [
    #     AwardInline,
    #     # OrganizationInline,
    # ]

    # readonly_fields = [
    #     'nomen',
    # ]

    raw_id_fields = [
        'parent',
    ]

    # readonly_fields = [
    #     'level',
    # ]


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'convention',
    ]

    list_display = [
        'nomen',
        'status',
        'convention',
    ]

    list_filter = [
        'status',
    ]

    raw_id_fields = [
        'convention',
    ]

    ordering = (
        'nomen',
    )

    search_fields = [
        'nomen',
    ]

    readonly_fields = [
        'nomen',
    ]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        'status',
        'actual_start',
        'actual_finish',
        'performer',
        'round',
        'num',
        'slot',
    ]

    list_display = [
        'nomen',
        'status',
    ]

    list_filter = [
        'status',
        'round__session__kind',
        'round__session__convention__season',
        'round__session__convention__year',
        # 'round__session__convention__organization',
    ]

    fsm_field = [
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = (
        'performer',
    )

    search_fields = (
        'nomen',
    )

    inlines = [
        # SongInline,
    ]


@admin.register(PerformanceScore)
class PerformanceScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    fields = (
        # 'name',
        'status',
        'bhs_id',
        'picture',
        # 'csa_pdf',
        'session',
        # 'group',
        # 'district',
        # 'division',
        'risers',
        ('is_evaluation', 'is_private',),
        ('tenor', 'lead', 'baritone', 'bass',),
        ('director', 'codirector', 'men'),
        'prelim',
        'seed',
    )

    list_display = (
        'nomen',
        'status',
    )

    list_filter = [
        'status',
        'session__convention__level',
        'session__kind',
        'session__convention__season',
        # 'session__convention__organization',
        'session__convention__year',
        'risers',
    ]

    fsm_field = [
        'status',
    ]

    inlines = [
        PerformanceInline,
        ContestantInline,
        SubmissionInline,
    ]

    search_fields = (
        'nomen',
    )

    raw_id_fields = (
        'session',
        # 'group',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'director',
        'codirector',
    )

    readonly_fields = (
        'nomen',
    )

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(PerformerScore)
class PerformerScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'user',
        'common_name',
        'status',
        'kind',
        'birth_date',
        'start_date',
        'end_date',
        'dues_thru',
        'mon',
        'spouse',
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'postal_code',
        # 'organization',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'bhs_id',
        'picture',
        'description',
        'notes',
    )

    list_display = (
        'nomen',
        'status',
        'bhs_id',
        'location',
        'website',
        'facebook',
        'twitter',
        'picture',
    )

    list_filter = [
        'status',
    ]

    raw_id_fields = [
        'user',
    ]

    readonly_fields = [
        'nomen',
    ]

    # inlines = [
    #     RoleInline,
    #     MemberInline,
    #     JudgeInline,
    # ]

    search_fields = (
        'nomen',
    )

    save_on_top = True

    readonly_fields = [
        'common_name',
    ]


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        'status',
        ('session', 'kind',),
        'num_songs',
        # 'mt',
        'start_date',
        'end_date',
        'ann_pdf',
    ]

    list_display = [
        'nomen',
        'status',
    ]

    list_filter = [
        'status',
        'session__kind',
        'session__convention__level',
        'session__convention__season',
        'session__convention__year',
        # 'session__convention__organization',
    ]

    fsm_field = [
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'nomen',
        # 'session',
        # 'kind',
    ]

    raw_id_fields = (
        'session',
        # 'mt',
    )

    inlines = [
        PerformanceInline,
    ]

    search_fields = [
        'nomen',
    ]


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        # 'status',
        'song',
        'person',
        'category',
        'kind',
        'original',
        'violation',
        'penalty',
        'points',
    ]

    readonly_fields = [
        'nomen',
        'song',
        'person',
    ]

    list_display = [
        'nomen',
        # 'status',
        'points',
    ]

    # list_filter = [
    #     'status',
    # ]

    raw_id_fields = [
        'song',
        'person',
    ]

    ordering = [
        'song',
        'person',
    ]
    save_on_top = True


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True
    fields = [
        # 'name',
        'status',
        'convention',
        'kind',
        'num_rounds',
        'panel_size',
        # 'start_date',
        # 'end_date',
        'primary',
        'current',
        # 'cursor',
        # 'year',
        # # 'size',
        'scoresheet_pdf',
    ]

    list_display = [
        'nomen',
        'status',
    ]

    list_filter = (
        'status',
        'kind',
        'convention__level',
        'convention__season',
        'convention__year',
        # 'convention__organization',
    )

    raw_id_fields = (
        'convention',
        'current',
        'primary',
    )

    readonly_fields = [
        'nomen',
    ]

    inlines = [
        RoundInline,
        PerformerInline,
        ContestInline,
    ]

    list_select_related = [
        'convention',
    ]

    ordering = (
        '-convention__year',
        'convention__level',
        # 'convention__organization__name',
        '-convention__season',
        'kind',
    )

    search_fields = [
        'nomen',
    ]


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        # 'name',
        'status',
        'num',
        'onstage',
        'round',
    ]
    list_display = [
        'nomen',
        'status',
        'onstage',
    ]

    list_filter = (
        'status',
    )

    readonly_fields = [
        'nomen',
    ]
    raw_id_fields = [
        'round',
    ]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = [
        # 'name',
        # 'status',
        'performance',
        'submission',
        'num',

        # 'title',
    ]

    list_display = (
        'nomen',
        # 'status',
        # 'title',
        'performance',
        'submission',
        'num',
    )

    # list_filter = (
    #     'status',
    # )

    search_fields = (
        'nomen',
    )

    inlines = [
        ScoreInline,
    ]
    save_on_top = True

    readonly_fields = (
        'nomen',
    )

    raw_id_fields = (
        'performance',
        'submission',
    )

    ordering = (
        'nomen',
        'num',
    )


@admin.register(SongScore)
class SongScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        # 'name',
        'status',
        'performer',
        'title',
        'bhs_catalog',
        'arrangers',
        'composers',
        'holders',
        # 'source',
        'is_medley',
        'is_parody',
    ]

    list_display = [
        'nomen',
        'status',
        'title',
        'arrangers',
    ]

    list_filter = (
        'status',
    )

    raw_id_fields = (
        'performer',
    )

    readonly_fields = [
        'nomen',
    ]


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
        'status',
        'city',
        'state',
        'airport',
        'timezone',
    )

    list_display = [
        'nomen',
        'name',
        'city',
        'state',
        'timezone',
    ]

    list_filter = (
        'status',
    )

    search_fields = (
        'nomen',
    )

    readonly_fields = [
        'nomen',
    ]

    inlines = [
        # ConventionInline,
    ]


class UserCreationForm(forms.ModelForm):
    # password = forms.CharField(
    #     label='Password',
    #     widget=forms.PasswordInput,
    # )
    # password2 = forms.CharField(
    #     label='Password confirmation',
    #     widget=forms.PasswordInput,
    # )

    class Meta:
        model = User
        fields = []
    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        # user.set_password(self.cleaned_data["password"])
        user.set_password(None)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            'username',
            'is_active',
            'is_staff',
        ]

    # def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        # return self.initial["password"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        'username',
        'is_active',
        'is_staff',
    ]

    list_filter = (
        'is_active',
        'is_staff',
    )

    fieldsets = (
        (None, {'fields': ('username', 'is_active', 'is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',)}),
    )

    search_fields = [
        'username',
    ]
    ordering = ('username',)
    filter_horizontal = ()


admin.site.unregister(AuthGroup)
