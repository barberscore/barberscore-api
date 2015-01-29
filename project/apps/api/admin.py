import logging
log = logging.getLogger(__name__)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from easy_select2 import select2_modelform

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
    QuartetMember,
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

ChapterForm = select2_modelform(
    Chapter,
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


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = ConventionForm


class QuartetMembershipInline(admin.TabularInline):
    model = Quartet.members.through
    form = QuartetMemberForm


class ChorusPerformanceInline(admin.TabularInline):
    form = ChorusPerformanceForm

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


class ChorusScoreInline(admin.TabularInline):
    form = ChorusPerformanceForm

    model = ChorusPerformance
    fields = (
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


class QuartetScoreInline(admin.TabularInline):
    form = QuartetPerformanceForm

    model = QuartetPerformance
    fields = (
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


@admin.register(Singer)
class SingerAdmin(CommonAdmin):
    form = SingerForm


@admin.register(District)
class DistrictAdmin(CommonAdmin):
    form = DistrictForm


@admin.register(Chapter)
class Chapter(admin.ModelAdmin):
    form = ChapterForm


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    form = ContestForm
    fields = (
        'convention',
        'year',
        'kind',
    )

    list_filter = [
        'year',
        'kind',
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
class QuartetAdmin(CommonAdmin):
    inlines = [
        QuartetMembershipInline,
    ]
    exclude = ('members',)


@admin.register(Chorus)
class ChorusAdmin(CommonAdmin):
    form = ChorusForm
