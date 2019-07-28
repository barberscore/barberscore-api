# Django
from django.contrib import admin

from .models import Group

# class ConventionStatusListFilter(admin.SimpleListFilter):
#     title = 'Convention Status'
#     parameter_name = 'convention_status'

#     def lookups(self, request, model_admin):
#         return (
#             (-10, 'Inactive'),
#             (0, 'New'),
#             (10, 'Active'),
#         )

#     def queryset(self, request, queryset):
#         status = self.value()
#         if status:
#             return queryset.filter(
#                 convention__status=status,
#             )


# class ActiveConventionListFilter(admin.SimpleListFilter):
#     title = 'Active Conventions'
#     parameter_name = 'active_conventions'

#     def lookups(self, request, model_admin):
#         Convention = apps.get_model('smanager.convention')
#         conventions = Convention.objects.filter(
#             status__gte=0,
#         ).order_by(
#             'year',
#             'season',
#             'district',
#         )
#         conventions_tuple = [(x.id, x.__str__) for x in conventions]
#         return conventions_tuple

#     def queryset(self, request, queryset):
#         convention_id = request.GET.get('active_conventions')
#         if convention_id:
#             return queryset.filter(convention__id=convention_id)
#         return queryset


# class SessionConventionStatusListFilter(admin.SimpleListFilter):
#     title = 'Convention Status'
#     parameter_name = 'convention_status'

#     def lookups(self, request, model_admin):
#         return (
#             (-10, 'Inactive'),
#             (0, 'New'),
#             (10, 'Active'),
#         )

#     def queryset(self, request, queryset):
#         status = self.value()
#         if status:
#             return queryset.filter(
#                 session__convention__status=status,
#             )

class AwardQualifierLevelFilter(admin.SimpleListFilter):
    title = 'Target Qualifier'
    parameter_name = 'parent__kind'

    def lookups(self, request, model_admin):
        return (
            (1, 'International'),
            (11, 'District'),
        )

    def queryset(self, request, queryset):
        kind = self.value()
        if kind:
            return queryset.filter(
                parent__group__kind=kind,
            )


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


class GroupListFilter(admin.SimpleListFilter):
    title = ('group')
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        orgs = Group.objects.filter(
            kind__lte=Group.KIND.chorus,
        ).values_list('id', 'code')
        return orgs

    def queryset(self, request, queryset):
        group = request.GET.get('group')
        if group:
            return queryset.filter(group=group)
        return queryset


class ParentGroupListFilter(admin.SimpleListFilter):
    title = ('parent')
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        orgs = Group.objects.filter(
            kind__lte=Group.KIND.district,
        ).values_list('id', 'code')
        return orgs

    def queryset(self, request, queryset):
        org = request.GET.get('org')
        if org:
            return queryset.filter(parent=org)
        return queryset


class ConventionGroupListFilter(admin.SimpleListFilter):
    title = ('district')
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.filter(
            kind__lte=Group.KIND.district,
        ).order_by(
            'tree_sort',
        ).values_list('id', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(group=district)
        return queryset


class SessionGroupListFilter(admin.SimpleListFilter):
    title = ('district')
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.filter(
            kind=Group.KIND.district,
        ).order_by(
            'tree_sort',
        ).values_list('id', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(convention__group=district)
        return queryset


class RoundGroupListFilter(admin.SimpleListFilter):
    title = ('district')
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.filter(
            kind=Group.KIND.district,
        ).order_by(
            'tree_sort',
        ).values_list('id', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(session__convention__group=district)
        return queryset
