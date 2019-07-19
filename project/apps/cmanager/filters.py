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
