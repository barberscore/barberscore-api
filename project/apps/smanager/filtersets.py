from django_filters.rest_framework import FilterSet
# Third-Party

# Local
from .models import Session
from .models import Entry


from .models import Assignment
from .models import Convention

from dry_rest_permissions.generics import DRYPermissionFiltersBase
from django.db.models import Q



# class RepertoryFilterBackend(DRYPermissionFiltersBase):

#     def filter_list_queryset(self, request, queryset, view):
#         """
#         Limits all list requests to only be seen by the owners or creators.
#         """
#         if request.user.is_staff:
#             return queryset
#         queryset = queryset.filter(
#             Q(
#                 group__officers__person__user=request.user,
#                 group__officers__status__gt=0,
#             ) |
#             Q(
#                 group__appearances__round__session__convention__assignments__person__user=request.user,
#                 group__appearances__round__session__convention__assignments__status__gt=0,
#                 group__appearances__round__session__convention__assignments__category__lte=10, # TODO
#             )
#         ).distinct()
#         return queryset

class AssignmentFilterset(FilterSet):
    class Meta:
        model = Assignment
        fields = {
            'user': [
                'exact',
            ],
            'status': [
                'exact',
            ],
            'convention__status': [
                'exact',
            ],
        }


class ConventionFilterset(FilterSet):
    class Meta:
        model = Convention
        fields = {
            'assignments__user': [
                'exact',
            ],
            'assignments__status': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }

class SessionFilterset(FilterSet):
    class Meta:
        model = Session
        fields = {
            'status': [
                'exact',
            ],
            'kind': [
                'exact',
            ],
            'is_invitational': [
                'exact',
            ],
        }


class EntryFilterset(FilterSet):
    class Meta:
        model = Entry
        fields = {
            'status': [
                'exact',
            ],
            'session__status': [
                'exact',
                'lt',
            ],
            'group_id': [
                'exact',
            ],
        }
