# Django
from django.contrib import admin

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

