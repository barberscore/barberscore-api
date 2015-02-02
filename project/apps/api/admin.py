import logging
log = logging.getLogger(__name__)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from easy_select2 import select2_modelform

from .models import (
    Award,
    Convention,
    Singer,
    Chorus,
    Quartet,
    District,
    Contest,
    QuartetPerformance,
    ChorusPerformance,
    QuartetMember,
    QuartetAward,
    ChorusAward,
    QuartetFinish,
    ChorusFinish,
)

ConventionForm = select2_modelform(
    Convention,
    attrs={'width': '250px'},
)

DistrictForm = select2_modelform(
    District,
    attrs={'width': '250px'},
)

QuartetMemberForm = select2_modelform(
    QuartetMember,
    attrs={'width': '250px'},
)

ChorusForm = select2_modelform(
    Chorus,
    attrs={'width': '250px'},
)

ContestForm = select2_modelform(
    Contest,
    attrs={'width': '250px'},
)

SingerForm = select2_modelform(
    Singer,
    attrs={'width': '250px'},
)

QuartetPerformanceForm = select2_modelform(
    QuartetPerformance,
    attrs={'width': '250px'},
)

ChorusPerformanceForm = select2_modelform(
    ChorusPerformance,
    attrs={'width': '250px'},
)

QuartetAwardForm = select2_modelform(
    QuartetAward,
    attrs={'width': '250px'},
)

ChorusAwardForm = select2_modelform(
    ChorusAward,
    attrs={'width': '250px'},
)


QuartetFinishForm = select2_modelform(
    QuartetFinish,
    attrs={'width': '250px'},
)


ChorusFinishForm = select2_modelform(
    ChorusFinish,
    attrs={'width': '250px'},
)


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = ConventionForm
    list_filter = [
        'year',
        'district',
        'kind',
    ]
    search_fields = ['name']
    save_on_top = True


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    search_fields = ['name']
    save_on_top = True


# @admin.register(QuartetFinish)
# class QuartetFinishAdmin(admin.ModelAdmin):
#     save_on_top = True


# @admin.register(ChorusFinish)
# class ChorusFinishAdmin(admin.ModelAdmin):
#     save_on_top = True


class QuartetMembershipInline(admin.TabularInline):
    model = Quartet.members.through
    form = QuartetMemberForm


class ChorusPerformanceInline(admin.TabularInline):
    form = ChorusPerformanceForm
    model = ChorusPerformance


class ChorusScoreInline(admin.TabularInline):
    form = ChorusPerformanceForm

    model = ChorusPerformance
    fields = (
        'place',
        'chorus',
        'song1',
        'mus1',
        'prs1',
        'sng1',
        'song2',
        'mus2',
        'prs2',
        'sng2',
    )
    ordering = ('place',)


class QuartetScoreInline(admin.TabularInline):
    form = QuartetPerformanceForm

    model = QuartetPerformance
    fields = (
        'place',
        'quartet',
        'song1',
        'mus1',
        'prs1',
        'sng1',
        'song2',
        'mus2',
        'prs2',
        'sng2',
    )
    ordering = ('place',)


class QuartetAwardInline(admin.TabularInline):
    form = QuartetAwardForm
    model = QuartetAward


class ChorusAwardInline(admin.TabularInline):
    form = ChorusAwardForm
    model = ChorusAward


class QuartetFinishInline(admin.TabularInline):
    form = QuartetFinishForm
    model = QuartetFinish


class ChorusFinishInline(admin.TabularInline):
    form = ChorusFinishForm
    model = ChorusFinish


class QuartetPerformanceInline(admin.TabularInline):
    form = QuartetPerformanceForm

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


@admin.register(Chorus)
class ChorusAdmin(CommonAdmin):
    form = ChorusForm
    # inlines = [
    #     ChorusAwardInline,
    #     ChorusFinishInline,
    # ]

    list_filter = ['district']


@admin.register(Singer)
class SingerAdmin(CommonAdmin):
    form = SingerForm


@admin.register(District)
class DistrictAdmin(CommonAdmin):
    form = DistrictForm
    list_filter = ['kind']


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    form = ContestForm
    list_filter = [
        'kind',
        'convention',
    ]

    inlines = [
        ChorusScoreInline,
        QuartetScoreInline,
        ChorusPerformanceInline,
        QuartetPerformanceInline,
        # ChorusFinishInline,
        # QuartetFinishInline,
    ]
    search_fields = ['name']
    save_on_top = True

    # def get_formsets_with_inlines(self, request, obj=None):
    #     for inline in self.get_inline_instances(request, obj):
    #         if obj.kind == Contest.CHORUS:
    #             if isinstance(inline, ChorusPerformanceInline):
    #                 yield inline.get_formset(request, obj), inline
    #                 break
    #             else:
    #                 continue
    #         else:
    #             if isinstance(inline, ChorusPerformanceInline):
    #                 continue
    #             else:
    #                 yield inline.get_formset(request, obj), inline


@admin.register(Quartet)
class QuartetAdmin(CommonAdmin):
    inlines = [
        QuartetMembershipInline,
        # QuartetAwardInline,
        # QuartetFinishInline,
    ]
    exclude = ('members',)
