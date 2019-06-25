from dry_rest_permissions.generics import DRYPermissionFiltersBase
from django.db.models import Q



class RepertoryFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        if request.user.is_staff:
            return queryset
        queryset = queryset.filter(
            Q(
                # group__officers__person__user=request.user,
                group__officers__status__gt=0,
            ) |
            Q(
                # group__appearances__round__session__convention__assignments__person__user=request.user,
                group__appearances__round__session__convention__assignments__status__gt=0,
                group__appearances__round__session__convention__assignments__category__lte=10, # TODO
            )
        ).distinct()
        return queryset

