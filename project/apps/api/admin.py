from django.contrib import admin

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


class QuartetPerformanceInline(admin.TabularInline):
    model = QuartetPerformance


class QuartetMembershipInline(admin.TabularInline):
    model = Quartet.members.through


class CommonAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Singer)
class SingerAdmin(CommonAdmin):
    pass


@admin.register(Quartet)
class QuartetAdmin(CommonAdmin):
    inlines = [
        QuartetMembershipInline,
        QuartetPerformanceInline,
    ]
    exclude = ('members',)


@admin.register(District)
class DistrictAdmin(CommonAdmin):
    pass


@admin.register(Chapter)
class ChatperAdmin(CommonAdmin):
    pass


@admin.register(Chorus)
class ChorusAdmin(CommonAdmin):
    inlines = [
        ChorusPerformanceInline,
    ]


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(QuartetPerformance)
class QuartetPerformanceAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(ChorusPerformance)
class ChorusPerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
