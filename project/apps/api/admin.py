from django.contrib import admin
from django.db import models
from django.forms import (
    widgets,
)

from django_object_actions import (
    DjangoObjectActions,
    takes_instance_or_queryset,
)

from easy_select2 import select2_modelform

from .models import (
    Convention,
    Contest,
    Contestant,
    Group,
    District,
    Song,
    Person,
    Performance,
    Score,
    Judge,
    Singer,
    Director,
    Session,
    # Catalog,
    Award,
    Appearance,
    User,
)

from grappelli.forms import GrappelliSortableHiddenMixin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    save_on_top = True


class PerformancesInline(admin.TabularInline):
    form = select2_modelform(
        Performance,
        attrs={'width': '100px'},
    )
    fields = (
        'appearance',
        'order',
        'song',
        'mus_points',
        'prs_points',
        'sng_points',
    )
    ordering = (
        'appearance',
        'order',
    )
    model = Performance
    extra = 0
    raw_id_fields = (
        'appearance',
        'song',
    )
    can_delete = True
    show_change_link = True


class ScoresInline(admin.TabularInline):
    model = Score
    form = select2_modelform(
        Score,
        attrs={'width': '300px'},
    )
    fields = (
        'performance',
        'judge',
        'category',
        'points',
    )
    ordering = (
        'judge',
    )
    extra = 0
    raw_id_fields = (
        'judge',
    )
    can_delete = True
    show_change_link = True


class JudgesInline(admin.TabularInline):
    model = Judge
    form = select2_modelform(
        Judge,
        attrs={'width': '100px'},
    )
    fields = (
        'contest',
        'person',
        'district',
        'part',
        'num',
        'is_practice',
    )
    ordering = (
        'part',
        'num',
    )
    extra = 0
    raw_id_fields = (
        'person',
        'contest',
    )
    can_delete = True
    show_change_link = True
    readonly_fields = [
        'person',
    ]
    classes = ('grp-collapse grp-closed',)


class SingersInline(admin.TabularInline):
    model = Singer
    form = select2_modelform(
        Singer,
        attrs={'width': '100px'},
    )
    fields = (
        'contestant',
        'person',
        'part',
    )
    ordering = (
        'part',
        'contestant',
    )
    extra = 0
    raw_id_fields = (
        'person',
        'contestant',
    )
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-closed',)


class DirectorsInline(admin.TabularInline):
    form = select2_modelform(
        Director,
        attrs={'width': '100px'},
    )
    fields = (
        'contestant',
        'person',
        'part',
    )
    ordering = (
        'part',
        'contestant',
    )
    model = Director
    extra = 0
    raw_id_fields = (
        'person',
        'contestant',
    )
    can_delete = True
    classes = ('grp-collapse grp-closed',)


# class CatalogsInline(admin.TabularInline):
#     model = Catalog
#     fields = (
#         'person',
#         'song',
#     )
#     extra = 0
#     raw_id_fields = (
#         'song',
#         'person',
#     )
#     can_delete = True
#     show_change_link = True


class AwardsInline(admin.TabularInline):
    model = Award
    fields = (
        'name',
    )
    extra = 0
    can_delete = True
    show_change_link = True
    classes = ('grp-collapse grp-closed',)


class ContestantsInline(admin.TabularInline):
    form = select2_modelform(
        Contestant,
        attrs={'width': '100px'},
    )
    fields = (
        'contest',
        'group',
        'district',
        'seed',
        'prelim',
        'place',
        'total_score',
        'men',
    )
    ordering = (
        'place',
        'seed',
        'group',
    )
    show_change_link = True

    model = Contestant
    extra = 0
    raw_id_fields = (
        'contest',
        'group',
    )
    can_delete = True
    readonly_fields = (
        'group',
    )
    classes = ('grp-collapse grp-closed',)


class AppearancesInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    form = select2_modelform(
        Appearance,
        attrs={'width': '100px'},
    )
    formfield_overrides = {
        models.DateTimeField: {'widget': widgets.DateInput}
    }

    fields = (
        'contestant',
        'session',
        'position',
        'draw',
        'start',
    )
    sortable_field_name = "position"
    show_change_link = True

    model = Appearance
    extra = 0
    raw_id_fields = (
        'contestant',
    )
    can_delete = True
    readonly_fields = (
        'contestant',
        'draw',
    )


class SessionsInline(admin.TabularInline):
    form = select2_modelform(
        Session,
        attrs={'width': '100px'},
    )
    formfield_overrides = {
        models.DateTimeField: {'widget': widgets.DateInput}
    }

    fields = (
        'contest',
        'kind',
        'start',
    )
    ordering = (
        'contest',
        'kind',
    )
    show_change_link = True

    model = Session
    extra = 0
    raw_id_fields = (
        'contest',
    )
    can_delete = True


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Convention,
        attrs={'width': '100px'},
    )

    formfield_overrides = {
        models.DateTimeField: {'widget': widgets.DateInput}
    }

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'status',
        'status_monitor',
        'location',
        'dates',
        'kind',
        'year',
        'district',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        ('location', 'timezone',),
        'dates',
        'district',
        'kind',
        'year',
    )

    list_filter = (
        'status',
        'kind',
        'year',
        'district',
    )

    readonly_fields = (
        'name',
        'status_monitor',
    )

    save_on_top = True


@admin.register(Contest)
class ContestAdmin(DjangoObjectActions, admin.ModelAdmin):
    @takes_instance_or_queryset
    def import_legacy(self, request, queryset):
        for obj in queryset:
            obj.import_legacy()
    import_legacy.label = 'Import Legacy'

    form = select2_modelform(
        Contest,
        attrs={'width': '150px'},
    )
    formfield_overrides = {
        models.DateTimeField: {'widget': widgets.DateInput}
    }

    save_on_top = True
    objectactions = [
        'import_legacy',
    ]

    inlines = [
        ContestantsInline,
        JudgesInline,
        SessionsInline,
    ]

    search_fields = (
        'name',
    )

    list_filter = (
        'status',
        'goal',
        'level',
        'kind',
        'year',
        'district',
    )

    list_display = (
        'name',
        'status',
        'rep',
        'admin',
        'goal',
        'rounds',
        'panel',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        ('rep', 'admin',),
        ('level', 'kind', 'goal', 'year',),
        'district',
        ('rounds', 'panel',),
    )

    raw_id_fields = (
        'rep',
        'admin',
    )

    readonly_fields = (
        'name',
        'status_monitor',
    )

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "convention":
    #         try:
    #             parent_obj_id = request.resolver_match.args[0]
    #             obj = Contest.objects.get(pk=parent_obj_id)
    #             kwargs["queryset"] = Convention.objects.filter(year=obj.year)
    #         except IndexError:
    #             pass
    #     return super(ContestAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Group,
        attrs={'width': '100px'},
    )

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'chapter_name',
        'chapter_code',
        'picture',
    )

    fields = (
        'name',
        'kind',
        ('start_date', 'end_date',),
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        ('chapter_name', 'chapter_code',),
        'notes',
    )

    list_filter = (
        'kind',
    )

    inlines = [
        ContestantsInline,
    ]

    save_on_top = True


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    @takes_instance_or_queryset
    def update_contestants(self, request, queryset):
        for obj in queryset:
            obj.save()
    update_contestants.label = 'Update Contestants'

    form = select2_modelform(
        Contestant,
        attrs={'width': '150px'},
    )

    formfield_overrides = {
        models.DateTimeField: {'widget': widgets.DateInput}
    }

    objectactions = [
        'update_contestants',
    ]

    inlines = [
        SingersInline,
        DirectorsInline,
        AwardsInline,
        AppearancesInline,
    ]

    list_display = (
        'name',
        'status',
        'seed',
        'prelim',
        'mus_score',
        'prs_score',
        'sng_score',
        'total_score',
        'men',
        'place',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'status',
        'contest__level',
        'contest__kind',
        'contest__year',
    )

    raw_id_fields = (
        'contest',
        'group',
    )

    fields = (
        'name',
        ('status', 'status_monitor',),
        ('contest', 'group', 'district',),
        ('seed', 'prelim',),
        ('place', 'men',),
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    )

    readonly_fields = (
        'name',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points',
        'mus_score',
        'prs_score',
        'sng_score',
        'total_score',
    )

    save_on_top = True


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Song,
        attrs={'width': '100px'},
    )

    save_on_top = True
    fields = (
        'name',
    )

    search_fields = (
        'name',
    )

    # inlines = [
    #     CatalogsInline,
    # ]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    form = select2_modelform(
        District,
        attrs={'width': '100px'},
    )

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'long_name',
        'kind',
    )

    fields = (
        'name',
        'long_name',
        'kind',
        ('start_date', 'end_date',),
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

    list_filter = (
        'kind',
    )

    save_on_top = True


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Person,
        attrs={'width': '100px'},
    )

    search_fields = (
        'name',
    )

    save_on_top = True
    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
    )

    fields = (
        'name',
        'kind',
        ('start_date', 'end_date',),
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

    inlines = [
        DirectorsInline,
        SingersInline,
        # CatalogsInline,
        JudgesInline,
    ]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
    formfield_overrides = {
        models.DateTimeField: {'widget': widgets.DateInput}
    }

    list_display = (
        'name',
        'status',
        'song',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points'
    )

    search_fields = (
        'name',
    )

    fields = [
        'name',
        ('status', 'status_monitor',),
        'order',
        'song',
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    ]

    inlines = [
        ScoresInline,
    ]

    list_filter = (
        'status',
        'appearance__contestant__contest__level',
        'appearance__contestant__contest__kind',
        'appearance__contestant__contest__year',
    )

    readonly_fields = (
        'name',
        'total_points',
        'mus_score',
        'prs_score',
        'sng_score',
        'total_score',
    )
    raw_id_fields = (
        'appearance',
        'catalog',
    )


# @admin.register(Catalog)
# class CatalogAdmin(admin.ModelAdmin):
#     save_on_top = True
#     fields = (
#         'song',
#         'person',
#         'bhs_id',
#         'bhs_published',
#         'bhs_fee',
#         'bhs_difficulty',
#         'bhs_tempo',
#         'bhs_medley',
#     )
#     raw_id_fields = (
#         'song',
#         'person',
#     )
#     search_fields = (
#         'song__name',
#         'person__name',
#     )
#     inlines = [
#         PerformancesInline,
#     ]
#     list_display = [
#         'name',
#         'song',
#         'bhs_songname',
#         'person',
#         'bhs_arranger',
#         'bhs_id',
#         # 'bhs_published',
#         # 'bhs_fee',
#         # 'bhs_difficulty',
#         # 'bhs_tempo',
#         # 'bhs_medley',
#     ]


@admin.register(Appearance)
class Appearance(admin.ModelAdmin):
    save_on_top = True
    formfield_overrides = {
        models.DateTimeField: {'widget': widgets.DateInput}
    }

    inlines = [
        PerformancesInline,
    ]
    list_display = [
        'name',
        'draw',
        'start',
    ]
    list_filter = [
        'status',
        'session',
        'contestant__contest__level',
        'contestant__contest__kind',
        'contestant__contest__year',
    ]

    fields = [
        'name',
        ('status', 'status_monitor',),
        'contestant',
        'contest',
        ('session', 'draw', 'start',),
        ('mus_points', 'prs_points', 'sng_points', 'total_points',),
        ('mus_score', 'prs_score', 'sng_score', 'total_score',),
    ]

    readonly_fields = [
        'name',
        'mus_points',
        'prs_points',
        'sng_points',
        'total_points',
        'mus_score',
        'prs_score',
        'sng_score',
        'total_score',
    ]


@admin.register(Score)
class Score(admin.ModelAdmin):
    save_on_top = True


@admin.register(Judge)
class Judge(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'name',
        'person',
    ]


@admin.register(Session)
class Session(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'name',
        'status',
        'start',
    ]
    fields = [
        'name',
        ('status', 'status_monitor',),
        ('contest', 'kind',),
        'start',
    ]

    readonly_fields = [
        'name',
    ]

    list_filter = (
        'status',
        'contest__level',
        'contest__kind',
        'contest__year',
    )

    inlines = [
        AppearancesInline,
    ]
