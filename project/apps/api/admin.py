# import logging
# log = logging.getLogger(__name__)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from django_object_actions import (
    DjangoObjectActions,
    takes_instance_or_queryset,
)

from easy_select2 import select2_modelform

from .models import (
    Convention,
    Contest,
    District,
    Quartet,
    Chorus,
    Award,
    Performance,
    Singer,
    # GroupMember,
    GroupAward,
    Appearance,
)


# class GroupMemberInline(admin.TabularInline):
#     form = select2_modelform(
#         GroupMember,
#         attrs={'width': '250px'},
#     )
#     model = GroupMember
#     extra = 0
#     show_change_link = True


class GroupAwardInline(admin.TabularInline):
    form = select2_modelform(
        GroupAward,
        attrs={'width': '250px'},
    )
    model = GroupAward
    extra = 0
    show_change_link = True


class AppearanceInline(admin.TabularInline):
    form = select2_modelform(
        Appearance,
        attrs={'width': '250px'},
    )
    model = Appearance
    extra = 0
    show_change_link = True


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Convention,
        attrs={'width': '250px'},
    )
    list_display = (
        '__unicode__',
        'location',
        'dates',
    )
    list_filter = (
        'district',
        'kind',
        'year',
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
        AppearanceInline,
    ]

    list_filter = (
        'kind',
        'year',
        'district',
    )

    list_display = (
        '__unicode__',
        'convention',
        'panel',
        'scoresheet_pdf',
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    form = select2_modelform(
        District,
        attrs={'width': '250px'},
    )
    save_on_top = True


QuartetForm = select2_modelform(
    Quartet,
    attrs={'width': '250px'},
)


# SingerForm = select2_modelform(
#     Singer,
#     attrs={'width': '250px'},
# )


@admin.register(Quartet)
class QuartetAdmin(admin.ModelAdmin):
    form = QuartetForm
    inlines = (
        # GroupMemberInline,
        AppearanceInline,
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
        'is_picture',
    )

    readonly_fields = (
        'is_picture',
    )

    # inlines = (
    #     GroupMemberInline,
    #     GroupAwardInline,
    # )
    save_on_top = True


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Chorus,
        attrs={'width': '250px'},
    )

    save_on_top = True


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Performance,
        attrs={'width': '250px'},
    )
    list_display = (
        'group',
        'contest',
        'round',
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
        'contest',
    )

    ordering = (
        'place',
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


# @admin.register(GroupMember)
# class GroupMemberAdmin(admin.ModelAdmin):
#     save_on_top = True


@admin.register(Appearance)
class AppearanceAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'seed',
        'prelim',
        'place',
        'score',
    )

    list_filter = (
        'contest',
        'group',
    )

    save_on_top = True


@admin.register(GroupAward)
class GroupAwardAdmin(admin.ModelAdmin):
    save_on_top = True
