# Django
from django.contrib import admin

class MCListFilter(admin.SimpleListFilter):
    title = 'Member Center'
    parameter_name = 'is_mc'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(
                mc_pk__isnull=False,
            )
        if self.value() == 'No':
            return queryset.filter(
                mc_pk__isnull=True,
            )


# class MCUserListFilter(admin.SimpleListFilter):
#     title = 'Member Center'
#     parameter_name = 'is_mc'

#     def lookups(self, request, model_admin):
#         return (
#             ('Yes', 'Yes'),
#             ('No', 'No'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'Yes':
#             return queryset.filter(
#                 person__mc_pk__isnull=False,
#             )
#         if self.value() == 'No':
#             return queryset.filter(
#                 person__mc_pk__isnull=True,
#             )


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


class AppearanceConventionStatusListFilter(admin.SimpleListFilter):
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
                round__session__convention__status=status,
            )
