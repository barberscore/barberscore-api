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
    Singer,
    Note,
    District,
    Director,
    Judge,
    Song,
)


class ContestantInline(admin.TabularInline):
    form = select2_modelform(
        Contestant,
        attrs={'width': '250px'},
    )
    model = Contestant
    extra = 0
    show_change_link = True
    fields = (
        'contest',
        'group',
        # 'director',
        # 'district',
        # 'tenor',
        # 'lead',
        # 'baritone',
        # 'bass',
        # 'prelim',
        # 'seed',
        # 'score',
        # 'place',
        'place',
        'score',
        'finals_song1',
        'finals_mus1_points',
        'finals_prs1_points',
        'finals_sng1_points',
        'finals_song2',
        'finals_mus2_points',
        'finals_prs2_points',
        'finals_sng2_points',
        'men',
    )


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Convention,
        attrs={'width': '250px'},
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
        ContestantInline,
    ]

    list_filter = (
        'level',
        'kind',
        'year',
        'district',
    )

    list_display = (
        'name',
        'district',
        'convention',
        'level',
        'kind',
        'year',
        'panel',
        'scoresheet_pdf',
        'scoresheet_csv',
        'is_active',
    )

    fields = (
        ('is_active', 'is_complete',),
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
        # 'bsmdb_id',
        'picture',
    )

    inlines = [
        ContestantInline,
    ]

    list_filter = (
        'kind',
    )

    readonly_fields = (
        'director',
        'lead',
        'tenor',
        'baritone',
        'bass',
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

    list_display = (
        'name',
        'district',
        # 'director',
        # 'tenor',
        # 'lead',
        # 'baritone',
        # 'bass',
        # 'seed',
        # 'prelim',
        'place',
        'score',
        'finals_song1',
        'finals_mus1_points',
        'finals_prs1_points',
        'finals_sng1_points',
        'finals_song2',
        'finals_mus2_points',
        'finals_prs2_points',
        'finals_sng2_points',
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

    # inlines = [
    #     PerformanceInline,
    # ]

    fields = (
        (
            'contest',
            'group',
            'district',
        ), (
            'director', 'men',
        ), (
            'tenor',
            'lead',
            'baritone',
            'bass',
        ), (
            'seed',
            'prelim',
            'draw',
            'stagetime',
        ), (
            'place',
            'score',
        ), (
            'quarters_song1',
            'quarters_mus1_points',
            'quarters_prs1_points',
            'quarters_sng1_points',
        ), (
            'quarters_song2',
            'quarters_mus2_points',
            'quarters_prs2_points',
            'quarters_sng2_points',
        ), (
            'semis_song1',
            'semis_mus1_points',
            'semis_prs1_points',
            'semis_sng1_points',
        ), (
            'semis_song2',
            'semis_mus2_points',
            'semis_prs2_points',
            'semis_sng2_points',
        ), (
            'finals_song1',
            'finals_mus1_points',
            'finals_prs1_points',
            'finals_sng1_points',
        ), (
            'finals_song2',
            'finals_mus2_points',
            'finals_prs2_points',
            'finals_sng2_points',
        ),
    )

    readonly_fields = (
        'name',
    )

    save_on_top = True


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Singer,
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
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
    )


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Director,
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
    )


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Judge,
        attrs={'width': '250px'},
    )

    save_on_top = True
    fields = (
        'name',
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Note,
        attrs={'width': '250px'},
    )

    save_on_top = True
    fields = (
        'user',
        'performance',
        'text',
    )


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
