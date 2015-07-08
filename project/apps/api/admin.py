# import logging
# log = logging.getLogger(__name__)

from django.contrib import admin

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
    Singer,
    Director,
)


class PerformancesInline(admin.TabularInline):
    form = select2_modelform(
        Performance,
        attrs={'width': '250px'},
    )
    fields = (
        'contestant',
        'song',
        'arranger',
        'mus_points',
        'prs_points',
        'sng_points',
    )
    ordering = (
        'round',
        'order',
    )
    model = Performance
    extra = 0
    raw_id_fields = (
        'contestant',
        'song',
        'arranger',
    )
    can_delete = True
    show_change_link = True


class SingersInline(admin.TabularInline):
    form = select2_modelform(
        Singer,
        attrs={'width': '250px'},
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
    model = Singer
    extra = 0
    raw_id_fields = (
        'person',
        'contestant',
    )
    can_delete = True


class DirectorsInline(admin.TabularInline):
    form = select2_modelform(
        Director,
        attrs={'width': '250px'},
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
    can_delete = False


class ContestantsInline(admin.TabularInline):
    form = select2_modelform(
        Contestant,
        attrs={'width': '250px'},
    )
    fields = (
        'contest',
        'group',
        'district',
        'draw',
        'stagetime',
        'place',
        'score',
        'men',
    )
    ordering = (
        'draw',
        'place',
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


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Convention,
        attrs={'width': '250px'},
    )

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'location',
        'dates',
        'kind',
        'year',
        'district',
        'is_active',
    )

    fields = (
        'is_active',
        'name',
        'location',
        'dates',
        'timezone',
        'district',
        'kind',
        'year',
    )

    list_filter = (
        'kind',
        'year',
        'district',
    )

    readonly_fields = (
        'name',
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
        attrs={'width': '250px'},
    )
    save_on_top = True
    objectactions = [
        'import_legacy',
    ]

    inlines = [
        ContestantsInline,
    ]

    search_fields = (
        'name',
    )

    list_filter = (
        'level',
        'kind',
        'year',
        'district',
    )

    list_display = (
        'name',
        'panel',
        'scoresheet_pdf',
        'scoresheet_csv',
        'is_active',
        'is_complete',
        'is_place',
        # 'is_score',
    )

    fields = (
        ('is_active', 'is_complete', 'is_place',),
        'name',
        'convention',
        'level',
        'kind',
        'year',
        'district',
        'panel',
        'scoresheet_pdf',
        'scoresheet_csv',
    )

    raw_id_fields = (
        'convention',
    )

    readonly_fields = (
        'name',
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Group,
        attrs={'width': '250px'},
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
        ('kind', 'is_active',),
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

    objectactions = [
        'update_contestants',
    ]

    inlines = [
        SingersInline,
        DirectorsInline,
        PerformancesInline,
    ]

    list_display = (
        'name',
        'place',
        'score',
        'points',
        'men',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'contest__level',
        'contest__kind',
        'contest__year',
    )

    raw_id_fields = (
        'contest',
        'group',
    )

    fields = (
        (
            'contest',
        ), (
            'group',
        ), (
            'district',
        ), (
            'seed',
            'prelim',
            'draw',
            'stagetime',
        ), (
            'place',
            'score',
        ),
        # 'picture',
    )

    readonly_fields = (
        'name',
    )

    save_on_top = True


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Song,
        attrs={'width': '250px'},
    )

    save_on_top = True
    fields = (
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    form = select2_modelform(
        District,
        attrs={'width': '250px'},
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

    list_filter = (
        'kind',
    )

    save_on_top = True


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Person,
        attrs={'width': '250px'},
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
    ]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'name',
        'song',
        'arranger',
        'mus_points',
        'prs_points',
        'sng_points',
    )

    search_fields = (
        'name',
    )

    fields = (
        (
            'name',
        ),
        (
            'contestant',
        ),
        (
            'round',
            'order',
        ),
        (
            'song',
        ),
        (
            'arranger',
        ),
        (
            'mus_points',
            'prs_points',
            'sng_points',
        ),
        (
            'penalty',
        ),
    )

    list_filter = (
        'contestant__contest__level',
        'contestant__contest__kind',
        'round',
        'contestant__contest__year',
    )

    readonly_fields = (
        'name',
    )
    raw_id_fields = (
        'contestant',
        'song',
        'arranger',
    )

# @admin.register(Singer)
# class SingerAdmin(admin.ModelAdmin):
#     save_on_top = True


# @admin.register(Director)
# class DirectorAdmin(admin.ModelAdmin):
#     save_on_top = True
