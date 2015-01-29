import logging
log = logging.getLogger(__name__)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from ajax_select.admin import (
    AjaxSelectAdminTabularInline,
    AjaxSelectAdmin,
)

from ajax_select import make_ajax_form

from .models import (
    Convention,
    Singer,
    Chorus,
    Quartet,
    District,
    Chapter,
    Contest,
    QuartetPerformance,
    ChorusPerformance,
)


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    pass


class ChorusPerformanceInline(AjaxSelectAdminTabularInline):
    def chorus_prelim(self, obj):
        return obj.chorus.prelim
    # show_num_photos.admin_order_field = 'num_photos'

    def chorus_rank(self, obj):
        return obj.chorus.rank
    # show_num_photos.admin_order_field = 'num_photos'

    def chorus_link(self, obj):
        return mark_safe(
            '<a href="{0}">{1}</a>'.format(
                reverse('admin:api_chorus_change', args=[obj.chorus.pk]),
                obj.chorus.pk,
            )
        )
    chorus_link.allow_tags = True

    readonly_fields = [
        'chorus_prelim',
        'chorus_rank',
        'chorus_link',
    ]
    model = ChorusPerformance
    form = make_ajax_form(
        ChorusPerformance,
        {'chorus': 'chorus'},
    )
    fields = (
        'chorus',
        'chorus_link',
        'queue',
        'chorus_prelim',
        'chorus_rank',
        # 'chorus__rank',
        # 'stagetime',
        # 'song1',
        # 'mus1',
        # 'prs1',
        # 'sng1',
        # 'song2',
        # 'mus2',
        # 'prs2',
        # 'sng2',
    )


class QuartetPerformanceInline(AjaxSelectAdminTabularInline):
    def quartet_prelim(self, obj):
        return obj.quartet.prelim
    # show_num_photos.admin_order_field = 'num_photos'

    def quartet_rank(self, obj):
        return obj.quartet.rank
    # show_num_photos.admin_order_field = 'num_photos'

    def quartet_link(self, obj):
        return mark_safe(
            '<a href="{0}">{1}</a>'.format(
                reverse('admin:api_quartet_change', args=[obj.quartet.pk]),
                obj.quartet.pk,
            )
        )
    quartet_link.allow_tags = True

    readonly_fields = [
        'quartet_prelim',
        'quartet_rank',
        'quartet_link',
    ]
    model = QuartetPerformance
    form = make_ajax_form(
        QuartetPerformance,
        {'quartet': 'quartet'},
    )
    fields = (
        'quartet',
        'quartet_link',
        'round',
        'queue',
        'quartet_prelim',
        'quartet_rank',
        # 'stagetime',
        # 'song1',
        # 'mus1',
        # 'prs1',
        # 'sng1',
        # 'song2',
        # 'mus2',
        # 'prs2',
        # 'sng2',
    )


class CommonAdmin(admin.ModelAdmin):
    def show_website(self, obj):
        url = '<a href="{0}">{1}</a>'.format(obj.website, obj.website)
        return mark_safe(url)
    show_website.allow_tags = True

    def show_email(self, obj):
        url = '<a href="mailto:{0}">{1}</a>'.format(obj.email, obj.email)
        return mark_safe(url)
    show_email.allow_tags = True

    def show_facebook(self, obj):
        url = '<a href="{0}">{1}</a>'.format(obj.facebook, obj.facebook)
        return mark_safe(url)
    show_facebook.allow_tags = True

    list_display = [
        'name',
        'location',
        'show_website',
        'show_email',
        'show_facebook',
        'phone',
        'twitter',
        'picture',
    ]
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

    fields = (
        'convention',
        'year',
        'kind',
        'dates',
        'location',
        'timezone',
    )

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
