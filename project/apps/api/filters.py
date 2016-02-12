import rest_framework_filters as filters

from .models import (
    Convention,
    Person,
    Award,
    Group,
)

# class CoalesceFilterBackend(filters.BaseFilterBackend):
#     """
#     Support Ember Data coalesceFindRequests.

#     """
#     def filter_queryset(self, request, queryset, view):
#         id_list = request.query_params.getlist('ids[]')
#         if id_list:
#             queryset = queryset.filter(slug__in=id_list)
#         return queryset


class ConventionFilter(filters.FilterSet):
    class Meta:
        model = Convention
        fields = {
            'status': filters.ALL_LOOKUPS,
        }


class PersonFilter(filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class AwardFilter(filters.FilterSet):
    class Meta:
        model = Award
        fields = {
            'name': filters.ALL_LOOKUPS,
        }

class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'name': filters.ALL_LOOKUPS,
        }
