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
    Performance,
    Singer,
    Note,
)


class PerformanceInline(admin.TabularInline):
    form = select2_modelform(
        Performance,
        attrs={'width': '250px'},
    )
    model = Performance
    extra = 0
    show_change_link = True


class ContestantInline(admin.TabularInline):
    form = select2_modelform(
        Contestant,
        attrs={'width': '250px'},
    )
    model = Contestant
    extra = 0
    show_change_link = True
    fields = (
        'group',
        'prelim',
        'seed',
        'score',
        'place',
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
    )
    fields = (
        'name',
        'location',
        'dates',
        'timezone',
    )
    save_on_top = True


@admin.register(Contest)
class ContestAdmin(DjangoObjectActions, admin.ModelAdmin):
    # @takes_instance_or_queryset
    # def import_scores(self, request, queryset):
    #     for obj in queryset:
    #         obj.import_scores()
    # import_scores.label = 'Import Scores'
    form = select2_modelform(
        Contest,
        attrs={'width': '250px'},
    )
    save_on_top = True
    # objectactions = [
    #     'import_scores',
    # ]

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
        '__unicode__',
        'convention',
        'level',
        'kind',
        'year',
        'district',
        'panel',
        'scoresheet_pdf',
        'scoresheet_csv',
    )

    fields = (
        'convention',
        'level',
        'kind',
        'year',
        'district',
        'panel',
        'scoresheet_pdf',
        'scoresheet_csv',
    )


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Performance,
        attrs={'width': '250px'},
    )
    list_display = (
        '__unicode__',
        'queue',
        'session',
        'stagetime',
        'place',
        'total_raw',
        'song1',
        'mus1',
        'prs1',
        'sng1',
        'song2',
        'mus2',
        'prs2',
        'sng2',
        'men',
    )

    list_filter = (
        'round',
        'contestant__contest',
        'stagetime',
    )

    ordering = (
        'place',
        'queue',
        'slug',
    )

    save_on_top = True


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
        'lead',
        'tenor',
        'baritone',
        'bass',
        'director',
        'chapter_name',
        'chapter_code',
    )

    save_on_top = True


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    @takes_instance_or_queryset
    def update_contestants(self, request, queryset):
        for obj in queryset:
            obj.save()
    update_contestants.label = 'Update Contestants'

    objectactions = [
        'update_contestants',
    ]

    list_display = (
        '__unicode__',
        'seed',
        'prelim',
        'place',
        'score',
    )

    search_fields = (
        'group__name',
    )

    list_filter = (
        'contest__level',
        'contest__kind',
        'contest__year',
    )

    inlines = [
        PerformanceInline,
    ]

    fields = (
        'contest',
        'group',
        'seed',
        'prelim',
        'place',
        'score',
    )

    save_on_top = True


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'name',
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'user',
        'performance',
        'text',
    )
