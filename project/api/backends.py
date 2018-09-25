
# Third-Party
from django_filters.rest_framework.backends import DjangoFilterBackend


class CoalesceFilterBackend(DjangoFilterBackend):
    """Support Ember Data coalesceFindRequests."""

    def filter_queryset(self, request, queryset, view):
        raw = request.query_params.get('filter[id]')
        if raw:
            ids = raw.split(',')
            view.pagination_class = None
            queryset = queryset.filter(id__in=ids)
        return queryset
