from django.contrib import admin

from .models import (
    Singer,
    Chorus,
    Quartet,
    Collegiate,
    District,
    Chapter,
    Contest,
    QuartetPerformance,
    ChorusPerformance,
)


class QuartetMembershipInline(admin.TabularInline):
    model = Quartet.members.through
    extra = 4


class CollegiateMembershipInline(admin.TabularInline):
    model = Collegiate.members.through
    extra = 4


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    save_on_top = True


@admin.register(Quartet)
class QuartetAdmin(admin.ModelAdmin):
    inlines = [
        QuartetMembershipInline,
    ]
    exclude = ('members',)
    save_on_top = True


@admin.register(Collegiate)
class CollegiateAdmin(admin.ModelAdmin):
    inlines = [
        CollegiateMembershipInline,
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
