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
    Quartet,
    Chorus,
    Performance,
    Singer,
    Contestant,
    # Award,
    # District,
    # GroupAward,
)


# class GroupAwardInline(admin.TabularInline):
#     form = select2_modelform(
#         GroupAward,
#         attrs={'width': '250px'},
#     )
#     model = GroupAward
#     extra = 0
#     show_change_link = True


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
    @takes_instance_or_queryset
    def import_scores(self, request, queryset):
        for obj in queryset:
            obj.import_scores()
    import_scores.label = 'Import Scores'
    form = select2_modelform(
        Contest,
        attrs={'width': '250px'},
    )
    save_on_top = True
    objectactions = [
        'import_scores',
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


QuartetForm = select2_modelform(
    Quartet,
    attrs={'width': '250px'},
)


@admin.register(Quartet)
class QuartetAdmin(admin.ModelAdmin):
    form = QuartetForm
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
    )

    inlines = (
        ContestantInline,
        # GroupAwardInline,
    )
    save_on_top = True


@admin.register(Chorus)
class ChorusAdmin(admin.ModelAdmin):
    def is_picture(self, obj):
        return bool(obj.picture)

    form = select2_modelform(
        Chorus,
        attrs={'width': '250px'},
    )

    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'director',
        'chapter_name',
        'chapter_code',
        'picture',
    )

    readonly_fields = (
        'is_picture',
    )

    save_on_top = True


# @admin.register(Award)
# class AwardAdmin(admin.ModelAdmin):
#     form = select2_modelform(
#         Chorus,
#         attrs={'width': '250px'},
#     )

#     save_on_top = True


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
        'contestant__contest',
    )

    ordering = (
        'place',
        'queue',
        'slug',
    )

    save_on_top = True


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    fields = (
        'name',
    )

    form = select2_modelform(
        Singer,
        attrs={'width': '250px'},
    )
    save_on_top = True


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'seed',
        'prelim',
        'place',
        'score',
    )

    inlines = [
        PerformanceInline,
    ]

    save_on_top = True


# @admin.register(GroupAward)
# class GroupAwardAdmin(admin.ModelAdmin):
#     save_on_top = True
