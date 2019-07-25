# Django
from django.contrib import admin

# Django
from django.contrib import admin
from django.apps import apps

class DistrictListFilter(admin.SimpleListFilter):
    title = 'district'
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        Group = apps.get_model('bhs.group')
        districts = Group.objects.filter(
            kind__in=[
                Group.KIND.district,
                Group.KIND.international,
            ],
            status=Group.STATUS.active,
        ).order_by(
            'tree_sort',
        ).values_list('code', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(group__code=district)
        return queryset

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


class ActiveConventionListFilter(admin.SimpleListFilter):
    title = 'Active Conventions'
    parameter_name = 'active_conventions'

    def lookups(self, request, model_admin):
        Convention = apps.get_model('smanager.convention')
        conventions = Convention.objects.filter(
            status__gte=0,
        ).order_by(
            'year',
            'season',
            'district',
        )
        conventions_tuple = [(x.id, x.__str__) for x in conventions]
        return conventions_tuple

    def queryset(self, request, queryset):
        convention_id = request.GET.get('active_conventions')
        if convention_id:
            return queryset.filter(convention__id=convention_id)
        return queryset


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
