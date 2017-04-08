# Third-Party
from django_filters.rest_framework.backends import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissionFiltersBase

# Django
from django.db.models import Q


class CoalesceFilterBackend(DjangoFilterBackend):
    """Support Ember Data coalesceFindRequests."""

    def filter_queryset(self, request, queryset, view):
        raw = request.query_params.get('filter[id]')
        if raw:
            ids = raw.split(',')
            # Disable pagination, so all records can load.
            view.pagination_class = None
            queryset = queryset.filter(id__in=ids)
        return queryset


class ContestPrivateFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            return queryset.filter(
                # group__roles__person__user=request.user,
                Q(contest__session__convention__assignment__person__user=request.user)
                # session__assignment__judge__user=request.user,
            )
        return queryset.none()


class EntryPrivateFilterBackend(DRYPermissionFiltersBase):
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


class AppearancePrivateFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
        return queryset.none()


class ScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to entry if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            else:
                return queryset.filter(
                    song__appearance__entry__group__roles__person__user=request.user,
                )
        return queryset.none()


class SongPrivateFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
        return queryset.none()
