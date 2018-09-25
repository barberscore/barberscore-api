# Django
from django.contrib import admin

from .models import Convention
from .models import Group

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


class OrphanListFilter(admin.SimpleListFilter):
    title = 'orphan'
    parameter_name = 'is_orphan'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(
                kind__in=[
                    Group.KIND.quartet,
                    Group.KIND.chorus,
                    Group.KIND.chapter,
                ],
                parent__code__in=[
                    'EVG',
                    'FWD',
                    'LOL',
                    'MAD'
                    'NED',
                    'SWD',
                ],
                # status=Group.STATUS.active,
            )


class RoundLegacyOssListFilter(admin.SimpleListFilter):
    title = 'Legacy OSS'
    parameter_name = 'is_legacy_oss'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(
                session__convention__status=Convention.STATUS.imported,
                legacy_oss__isnull=False,
            )
        if self.value() == 'No':
            return queryset.filter(
                session__convention__status=Convention.STATUS.imported,
                legacy_oss__isnull=True,
            )


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


class MCUserListFilter(admin.SimpleListFilter):
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
                person__mc_pk__isnull=False,
            )
        if self.value() == 'No':
            return queryset.filter(
                person__mc_pk__isnull=True,
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


class DistrictListFilter(admin.SimpleListFilter):
    title = 'district'
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.filter(
            kind__in=[
                Group.KIND.district,
                Group.KIND.noncomp,
                Group.KIND.affiliate
            ],
            status=Group.STATUS.active,
        ).order_by(
            'tree_sort',
        ).values_list('code', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(district=district)
        return queryset


class DivisionListFilter(admin.SimpleListFilter):
    title = 'division'
    parameter_name = 'division'

    def lookups(self, request, model_admin):
        divisions = Group.objects.filter(
            kind=Group.KIND.division,
            status=Group.STATUS.active,
        ).order_by(
            'tree_sort',
        ).values_list('name', 'name')
        return divisions

    def queryset(self, request, queryset):
        division = request.GET.get('division')
        if division:
            return queryset.filter(division=division)
        return queryset


class GroupListFilter(admin.SimpleListFilter):
    title = ('group')
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        orgs = Group.objects.filter(
            kind__lte=Group.KIND.division,
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
            kind__lte=Group.KIND.division,
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
