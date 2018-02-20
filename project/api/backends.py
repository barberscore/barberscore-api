# Third-Party
from django_filters.rest_framework.backends import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissionFiltersBase


class CoalesceFilterBackend(DjangoFilterBackend):
    """Support Ember Data coalesceFindRequests."""

    def filter_queryset(self, request, queryset, view):
        raw = request.query_params.get('filter[id]')
        if raw:
            ids = raw.split(',')
            view.pagination_class = None
            queryset = queryset.filter(id__in=ids)
        return queryset


class GroupFilterBackend(DjangoFilterBackend):
    """Support Ember Data coalesceFindRequests."""

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.exclude(
            kind__lte=30
        )
        return queryset


class MemberFilterBackend(DjangoFilterBackend):
    """Support Ember Data coalesceFindRequests."""

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.exclude(
            group__kind__lte=30
        )
        return queryset


class ScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all requests to superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            # else:
            #     return queryset.filter(
            #         song__appearance__entry__entity__officers__person__user=request.user,
            #     )
        return queryset.none()

