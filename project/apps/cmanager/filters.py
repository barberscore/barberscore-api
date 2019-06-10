# Django
from django.contrib import admin
from django.apps import apps

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


