from dry_rest_permissions.generics import DRYPermissionFiltersBase
from django.db.models import Q

from .models import Round

class AppearanceFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        queryset = queryset.filter(
            round__status=Round.STATUS.finished,
        )
        return queryset


class ScoreFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        queryset = queryset.filter(
            panelist__person__user=request.user,
        )
        return queryset
