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
    extra = 4


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    save_on_top = True


@admin.register(Quartet)
class QuartetAdmin(admin.ModelAdmin):
    inlines = [
        QuartetMembershipInline,
        QuartetPerformanceInline,
    ]
    exclude = ('members',)
    save_on_top = True


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Chapter)
class ChatperAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Chorus)
class ChorusAdmin(admin.ModelAdmin):
    inlines = [
        ChorusPerformanceInline,
    ]
    save_on_top = True


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(QuartetPerformance)
class QuartetPerformanceAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(ChorusPerformance)
class ChorusPerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
