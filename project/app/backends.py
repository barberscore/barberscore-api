# Third-Party
from django_filters.rest_framework.backends import BaseFilterBackend
from dry_rest_permissions.generics import DRYPermissionFiltersBase
from django.db.models import Q


class CoalesceFilterBackend(BaseFilterBackend):
    """Support Ember Data coalesceFindRequests."""

    def filter_queryset(self, request, queryset, view):
        raw = request.query_params.get('filter[id]')
        if raw:
            ids = raw.split(',')
            # Disable pagination, so all records can load.
            view.pagination_class = None
            queryset = queryset.filter(id__in=ids)
        return queryset


class ContestScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            return queryset.filter(
                # group__roles__person__user=request.user,
                Q(session__assignment__person__user=request.user)
                # session__assignment__judge__user=request.user,
            )
        return queryset.none()


class PerformerScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            return queryset.filter(
                # group__roles__person__user=request.user,
                Q(session__assignment__person__user=request.user)
                # session__assignment__judge__user=request.user,
            )
        return queryset.none()


class PerformanceScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
        return queryset.none()


class ScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to performer if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            else:
                return queryset.filter(
                    song__performance__performer__group__roles__person__user=request.user,
                )
        return queryset.none()


class SongScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
        return queryset.none()
