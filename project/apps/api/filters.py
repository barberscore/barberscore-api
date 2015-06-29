from rest_framework import filters


class CoalesceFilterBackend(filters.BaseFilterBackend):
    """
    Support Ember Data coalesceFindRequests.

    """
    def filter_queryset(self, request, queryset, view):
        id_list = request.QUERY_PARAMS.getlist('ids[]')
        if id_list:
            queryset = queryset.filter(slug__in=id_list)
        return queryset
