# Django
from django.contrib import admin

class ConventionStatusListFilter(admin.SimpleListFilter):
    title = 'Convention Status'
    parameter_name = 'convention_status'

    def lookups(self, request, model_admin):
        return (
            (-10, 'Inactive'),
            (0, 'New'),
            (10, 'Active'),
        )

    def queryset(self, request, queryset):
        status = self.value()
        if status:
            return queryset.filter(
                convention__status=status,
            )


class SessionConventionStatusListFilter(admin.SimpleListFilter):
    title = 'Convention Status'
    parameter_name = 'convention_status'

    def lookups(self, request, model_admin):
        return (
            (-10, 'Inactive'),
            (0, 'New'),
            (10, 'Active'),
        )

    def queryset(self, request, queryset):
        status = self.value()
        if status:
            return queryset.filter(
                session__convention__status=status,
            )
