from django.contrib import admin

# from ajax_select import make_ajax_form

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


class ChorusPerformanceInline(admin.TabularInline):
    model = ChorusPerformance
    fields = (
        'chorus',
        'queue',
        'song1',
        'song2',
    )
    # form = make_ajax_form(model, {'chorus': 'chorus'})


class QuartetPerformanceInline(admin.TabularInline):
    model = QuartetPerformance
    fields = (
        'quartet',
        'round',
        'queue',
        'song1',
        'song2',
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
class QuartetAdmin(CommonAdmin):
    inlines = [
        QuartetPerformanceInline,
    ]


@admin.register(Chorus)
class ChorusAdmin(CommonAdmin):
    inlines = [
        ChorusPerformanceInline,
    ]


@admin.register(QuartetPerformance)
class QuartetPerformanceAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(ChorusPerformance)
class ChorusPerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
