# Third-Party
# from fsm_admin.mixins import FSMTransitionMixin
from mptt.admin import MPTTModelAdmin

# Django
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group as AuthGroup

# Local
from .inlines import (
    AssignmentInline,
    AwardInline,
    ContestantInline,
    ContestInline,
    ConventionInline,
    GroupInline,
    HostInline,
    JudgeInline,
    MemberInline,
    PerformanceInline,
    PerformerInline,
    RoleInline,
    RoundInline,
    ScoreInline,
    SessionInline,
    SongInline,
    SubmissionInline,
)
from .models import (
    Assignment,
    Award,
    Catalog,
    Chapter,
    Contest,
    ContestScore,
    Contestant,
    ContestantScore,
    Convention,
    Group,
    Host,
    Judge,
    Member,
    Organization,
    Performance,
    PerformanceScore,
    Performer,
    PerformerScore,
    Person,
    Role,
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


# from django_fsm_log.models import StateLog


# @admin.register(StateLog)
# class StateLogAdmin(admin.ModelAdmin):
#     pass


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):

    fields = [
        # 'name',
        'status',
        'is_manual',
        'organization',
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
        'organization__level',
        'kind',
        'championship_season',
        'qualifier_season',
        'size',
        'scope',
        'is_manual',
        'is_novice',
        'is_improved',
        'organization',
    ]

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'organization__level',
        'organization__name',
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
        # 'name',
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


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'category',
        'kind',
        'start_date',
        'end_date',
        'person',
        'organization',
    ]

    list_display = [
        'nomen',
        'category',
        'kind',
        'status',
    ]

    list_filter = [
        'status',
        'category',
        'kind',
    ]

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'person',
        'organization',
    ]

    search_fields = [
        'nomen',
    ]

    ordering = (
        'nomen',
    )


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    search_fields = (
        'nomen',
    )

    list_display = (
        'nomen',
        'code',
        'organization',
        'status',
    )

    list_filter = (
        'status',
        'organization',
    )

    fields = (
        'nomen',
        'status',
        'organization',
        'code',
        'bhs_id',
    )

    readonly_fields = [
        'nomen',
    ]

    inlines = [
        GroupInline,
        MemberInline,
    ]

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'status',
        'award',
        'session',
        'cycle',
        'is_qualifier',
        'num_rounds',
    ]

    list_display = (
        'nomen',
        'session',
    )

    list_filter = [
        'status',
        'award__organization__level',
        'award__kind',
        'award__is_primary',
        'is_qualifier',
        'award__organization',
        'cycle',
    ]

    save_on_top = True

    inlines = [
        ContestantInline,
    ]

    readonly_fields = [
        'nomen',
        'cycle',
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
        'name',
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
        'nomen',
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
        'drcj',
    )

    list_display = (
        'nomen',
        'status',
        'start_date',
        'end_date',
        'venue',
    )

    list_filter = (
        'status',
        'level',
        'kind',
        'season',
        'hosts__organization',
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
        'drcj',
        'venue',
    ]

    ordering = (
        '-year',
        'level',
    )

    save_on_top = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = (
        'nomen',
    )

    fields = (
        'nomen',
        'status',
        'kind',
        ('age', 'is_novice',),
        'bhs_id',
        'start_date',
        'end_date',
        'chapter',
        'district',
        'division',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        'notes',
    )

    list_display = (
        'nomen',
        'name',
        'bhs_id',
        'status',
        'district',
        'division',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
    )

    list_filter = (
        'kind',
        'status',
    )

    inlines = [
        # RoleInline,
        # PerformerInline,
    ]

    raw_id_fields = [
        'chapter',
    ]

    readonly_fields = [
        'nomen',
    ]

    save_on_top = True

    ordering = (
        'nomen',
    )


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'convention',
        'organization',
    ]

    list_display = [
        'nomen',
        'status',
        'convention',
        'organization',
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


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'status',
        'category',
        'kind',
        'slot',
        'bhs_id',
        'session',
        'judge',
        'organization',
    ]

    list_display = [
        'nomen',
        'status',
        'kind',
        'category',
        'judge',
        'organization',
    ]

    list_filter = (
        'status',
        'category',
        'kind',
    )

    list_select_related = [
        'organization',
        'session',
        'judge',
    ]

    raw_id_fields = (
        'session',
        'judge',
    )

    readonly_fields = [
        'nomen',
    ]

    inlines = [
        ScoreInline,
    ]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'chapter',
        'person',
        'start_date',
        'end_date',
    ]

    list_display = [
        'nomen',
        'status',
        'start_date',
        'end_date',
    ]

    list_filter = [
        'status',
    ]

    raw_id_fields = [
        'chapter',
        'person',
    ]

    ordering = (
        'nomen',
    )

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]


@admin.register(Organization)
class OrganizationAdmin(MPTTModelAdmin):
    fields = [
        'name',
        'status',
        'parent',
        'level',
        'kind',
        'code',
        'start_date',
        'end_date',
        'short_name',
        'long_name',
        'location',
        'representative',
        'spots',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        'notes',
    ]

    list_filter = [
        'status',
        'level',
        'kind',
    ]

    list_display = [
        'nomen',
        'status',
        'code',
        'short_name',
        'long_name',
        'level',
        'kind',
    ]

    inlines = [
        AwardInline,
        # OrganizationInline,
    ]

    readonly_fields = [
        'nomen',
    ]

    raw_id_fields = [
        'representative',
    ]

    readonly_fields = [
        'level',
    ]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    fields = [
        'name',
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
        'round__session__convention__organization',
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
        SongInline,
    ]


@admin.register(PerformanceScore)
class PerformanceScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'status',
        'bhs_id',
        'picture',
        'csa_pdf',
        'session',
        'group',
        'district',
        'division',
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
        'session__convention__organization',
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
        'group',
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

    inlines = [
        RoleInline,
        # MemberInline,
        JudgeInline,
    ]

    search_fields = (
        'nomen',
    )

    save_on_top = True

    readonly_fields = [
        'common_name',
    ]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'status',
        'start_date',
        'end_date',
        'group',
        'person',
        'part',
    ]

    list_display = [
        'nomen',
        'status',
        'start_date',
        'end_date',
    ]

    list_filter = [
        'status',
    ]

    readonly_fields = [
        'nomen',
    ]

    search_fields = [
        'nomen',
    ]

    raw_id_fields = (
        'group',
        'person',
    )


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'status',
        ('session', 'kind',),
        'num_songs',
        'mt',
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
        'session__convention__organization',
    ]

    fsm_field = [
        'status',
    ]

    save_on_top = True

    readonly_fields = [
        'nomen',
        'session',
        'kind',
    ]

    raw_id_fields = (
        'session',
        'mt',
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
        'name',
        # 'status',
        'song',
        'assignment',
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
        'assignment',
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
        'assignment',
    ]

    ordering = [
        'song',
        'assignment',
    ]
    save_on_top = True


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fsm_field = [
        'status',
    ]

    save_on_top = True
    fields = [
        'name',
        'status',
        'convention',
        'kind',
        'num_rounds',
        'start_date',
        'end_date',
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
        'convention__organization',
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
        AssignmentInline,
        ContestInline,
    ]

    list_select_related = [
        'convention',
    ]

    ordering = (
        '-convention__year',
        'convention__level',
        'convention__organization__name',
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
        'name',
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
        'name',
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
        'name',
        'status',
        'performer',
        'title',
        'arranger',
        'source',
        'is_medley',
        'is_parody',
    ]

    list_display = [
        'nomen',
        'status',
        'title',
        'arranger',
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
        'nomen',
        'status',
        'name',
        'city',
        'state',
        'airport',
        'timezone',
    )

    list_display = [
        'nomen',
        'nomen',
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


# admin.site.register(User, UserAdmin)
admin.site.unregister(AuthGroup)
