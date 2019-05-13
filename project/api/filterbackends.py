from dry_rest_permissions.generics import DRYPermissionFiltersBase
from django.db.models import Q

from .models import Appearance
from .models import Assignment
from .models import Round

class AppearanceFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        if request.user.is_staff:
            return queryset
        queryset = queryset.filter(
            Q(
                round__status=Round.STATUS.finished,
            ) |
            Q(
                round__session__convention__assignments__person__user=request.user,
                round__session__convention__assignments__status__gt=0,
                round__session__convention__assignments__category__lte=Assignment.CATEGORY.ca,
            )
        ).distinct()
        return queryset


class OutcomeFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        if request.user.is_staff:
            return queryset
        queryset = queryset.filter(
            Q(
                round__status=Round.STATUS.finished,
            ) |
            Q(
                round__session__convention__assignments__person__user=request.user,
                round__session__convention__assignments__status__gt=0,
                round__session__convention__assignments__category__lte=Assignment.CATEGORY.ca,
            )
        ).distinct()
        return queryset


class ScoreFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        if request.user.is_staff:
            return queryset
        queryset = queryset.filter(
            # Assigned DRCJs and CAs can always see
            Q(
                song__appearance__round__session__convention__assignments__person__user=request.user,
                song__appearance__round__session__convention__assignments__status__gt=0,
                song__appearance__round__session__convention__assignments__category__lte=Assignment.CATEGORY.ca,
            ) |
            # Panelists can see their own scores
            Q(
                panelist__person__user=request.user,
                panelist__status__gt=0,
            ) |
            # Panelists can see others' scores if Appearance is complete.
            Q(
                song__appearance__round__panelists__person__user=request.user,
                song__appearance__round__panelists__status__gt=0,
                song__appearance__status__lte=Appearance.STATUS.completed,
            ) |
            # Group members can see their own scores if complete.
            Q(
                song__appearance__group__members__person__user=request.user,
                song__appearance__group__members__status__gt=0,
                song__appearance__status__lte=Appearance.STATUS.completed,
            )
        ).distinct()
        return queryset


class SongFilterBackend(DRYPermissionFiltersBase):

    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the owners or creators.
        """
        if request.user.is_staff:
            return queryset
        queryset = queryset.filter(
            Q(
                appearance__round__status=Round.STATUS.finished,
            ) |
            Q(
                appearance__round__session__convention__assignments__person__user=request.user,
                appearance__round__session__convention__assignments__status__gt=0,
                appearance__round__session__convention__assignments__category__lte=Assignment.CATEGORY.ca,
            )
        ).distinct()
        return queryset