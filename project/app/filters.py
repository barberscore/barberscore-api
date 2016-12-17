# Third-Party
import rest_framework_filters as filters
from dry_rest_permissions.generics import DRYPermissionFiltersBase
from rest_framework.filters import BaseFilterBackend
from django.db.models import Q

# Local
from .models import (
    Catalog,
    Contestant,
    Convention,
    Group,
    Judge,
    Performer,
    Person,
    Session,
    Submission,
    Venue,
    # User,
)


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


class ConventionFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            else:
                return queryset.filter(
                    Q(drcj__user=request.user) |
                    Q(sessions__assignments__judge__person__user=request.user)
                )
        return queryset.none()


class OrganizationFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            else:
                return queryset.filter(
                    Q(representative__user=request.user) |
                    Q(conventions__sessions__assignments__judge__person__user=request.user)
                )
        return queryset.none()


class ContestantFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
        return queryset.none()


class PerformerScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            return queryset.filter(
                # group__roles__person__user=request.user,
                Q(session__assignment__judge__person__user=request.user)
                # session__assignment__judge__person__user=request.user,
            )
        return queryset.none()


class PerformanceScoreFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
        return queryset.none()


class SessionFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """Limit all list requests to at least validated if not superuser."""
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
            else:
                return queryset.filter(
                    Q(convention__drcj__user=request.user) |
                    Q(assignments__judge__person__user=request.user)
                )
        return queryset.none()


class SongScoreFilterBackend(DRYPermissionFiltersBase):
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


class UserFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        if request.user.is_authenticated():
            if request.user.is_staff:
                return queryset.all()
        if request.user.is_authenticated:
            return queryset.filter(pk=request.user.pk)
        return queryset.none()


class CatalogFilter(filters.FilterSet):

    class Meta:
        model = Catalog
        fields = {
            'title': '__all__',
        }


class ConventionFilter(filters.FilterSet):

    class Meta:
        model = Convention
        fields = {
            'status': '__all__',
            'year': '__all__',
        }


class GroupFilter(filters.FilterSet):
    name = filters.AllLookupsFilter(name='name')

    class Meta:
        model = Group
        fields = {
            'nomen': '__all__',
            'kind': '__all__',
            'status': '__all__',
        }


class JudgeFilter(filters.FilterSet):
    class Meta:
        model = Judge
        fields = {
            'name': '__all__',
            'category': '__all__',
        }


class ContestantFilter(filters.FilterSet):
    class Meta:
        model = Contestant
        fields = {
            'name': '__all__',
        }


class PerformerFilter(filters.FilterSet):
    group = filters.RelatedFilter(GroupFilter, name='group')

    class Meta:
        model = Performer
        fields = {
            'name': '__all__',
        }


class PersonFilter(filters.FilterSet):

    class Meta:
        model = Person
        fields = [
            'status',
        ]
        fields = {
            'name': '__all__',
            'nomen': '__all__',
        }


class SessionFilter(filters.FilterSet):
    convention = filters.RelatedFilter(ConventionFilter, name='convention')

    class Meta:
        model = Session
        fields = {
            'status': '__all__',
        }


class SubmissionFilter(filters.FilterSet):
    class Meta:
        model = Submission
        fields = {
            # 'performer__id': '__all__',
            'status': '__all__',
        }


class VenueFilter(filters.FilterSet):
    class Meta:
        model = Venue
        fields = {
            'name': '__all__',
        }
