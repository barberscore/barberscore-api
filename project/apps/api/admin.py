from django.contrib import admin

from ajax_select.admin import (
    AjaxSelectAdminTabularInline,
    AjaxSelectAdmin,
)

from ajax_select import make_ajax_form

from .models import (
    Singer,
    Chorus,
    Quartet,
    District,
    Chapter,
    Contest,
    QuartetPerformance,
    ChorusPerformance,
)


class ChorusPerformanceInline(AjaxSelectAdminTabularInline):
    model = ChorusPerformance
    form = make_ajax_form(
        ChorusPerformance,
        {'chorus': 'chorus'},
    )
    fields = (
        'chorus',
        'queue',
        'song1',
        'mus1',
        'prs1',
        'sng1',
        'song2',
        'mus2',
        'prs2',
        'sng2',
    )


class QuartetPerformanceInline(AjaxSelectAdminTabularInline):
    model = QuartetPerformance
    form = make_ajax_form(
        QuartetPerformance,
        {'quartet': 'quartet'},
    )
    fields = (
        'quartet',
        'round',
        'queue',
        'song1',
        'mus1',
        'prs1',
        'sng1',
        'song2',
        'mus2',
        'prs2',
        'sng2',
    )


class CommonAdmin(admin.ModelAdmin):
    search_fields = ['name']
    save_on_top = True


@admin.register(Singer)
class SingerAdmin(CommonAdmin):
    pass


@admin.register(District)
class DistrictAdmin(CommonAdmin):
    pass


@admin.register(Chapter)
class ChatperAdmin(CommonAdmin):
    pass


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):

    list_filter = [
        'year',
        'kind',
        'level',
    ]

    inlines = [
        ChorusPerformanceInline,
        QuartetPerformanceInline,
    ]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if obj.kind == Contest.CHORUS:
                if isinstance(inline, ChorusPerformanceInline):
                    yield inline.get_formset(request, obj), inline
                    break
                else:
                    continue
            else:
                if isinstance(inline, ChorusPerformanceInline):
                    continue
                else:
                    yield inline.get_formset(request, obj), inline


@admin.register(Quartet)
class QuartetAdmin(AjaxSelectAdmin, CommonAdmin):
    form = make_ajax_form(
        Quartet,
        {
            'lead': 'singer',
            'tenor': 'singer',
            'baritone': 'singer',
            'bass': 'singer'
        },
    )


@admin.register(Chorus)
class ChorusAdmin(CommonAdmin):
    pass


# @admin.register(QuartetPerformance)
# class QuartetPerformanceAdmin(admin.ModelAdmin):
#     save_on_top = True


# @admin.register(ChorusPerformance)
# class ChorusPerformanceAdmin(admin.ModelAdmin):
#     save_on_top = True
