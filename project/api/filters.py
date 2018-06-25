# Third-Party
from django_filters.rest_framework import FilterSet

# Django
from django.contrib import admin
from django_fsm_log.models import StateLog

# Local
from .models import Assignment
from .models import Convention
from .models import Group
from .models import Officer
from .models import Score
from .models import Round
from .models import Session
from .models import User


class OrphanListFilter(admin.SimpleListFilter):
    title = 'orphan'
    parameter_name = 'is_orphan'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(
                kind__in=[
                    Group.KIND.quartet,
                    Group.KIND.chorus,
                    Group.KIND.chapter,
                ],
                parent__code__in=[
                    'EVG',
                    'FWD',
                    'LOL',
                    'MAD'
                    'NED',
                    'SWD',
                ],
                # status=Group.STATUS.active,
            )


class MCListFilter(admin.SimpleListFilter):
    title = 'Member Center'
    parameter_name = 'is_mc'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(
                mc_pk__isnull=False,
            )
        if self.value() == 'No':
            return queryset.filter(
                mc_pk__isnull=True,
            )


class MCUserListFilter(admin.SimpleListFilter):
    title = 'Member Center'
    parameter_name = 'is_mc'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(
                person__mc_pk__isnull=False,
            )
        if self.value() == 'No':
            return queryset.filter(
                person__mc_pk__isnull=True,
            )


class ConventionStatusListFilter(admin.SimpleListFilter):
    title = 'Convention Status'
    parameter_name = 'convention_status'

    def lookups(self, request, model_admin):
        return (
            (-10, 'Inactive'),
            (0, 'New'),
            (10, 'Active'),
        )

    def queryset(self, request, queryset):
        status = self.value()
        if status:
            return queryset.filter(
                convention__status=status,
            )


class SessionConventionStatusListFilter(admin.SimpleListFilter):
    title = 'Convention Status'
    parameter_name = 'convention_status'

    def lookups(self, request, model_admin):
        return (
            (-10, 'Inactive'),
            (0, 'New'),
            (10, 'Active'),
        )

    def queryset(self, request, queryset):
        status = self.value()
        if status:
            return queryset.filter(
                session__convention__status=status,
            )


class AppearanceConventionStatusListFilter(admin.SimpleListFilter):
    title = 'Convention Status'
    parameter_name = 'convention_status'

    def lookups(self, request, model_admin):
        return (
            (-10, 'Inactive'),
            (0, 'New'),
            (10, 'Active'),
        )

    def queryset(self, request, queryset):
        status = self.value()
        if status:
            return queryset.filter(
                round__session__convention__status=status,
            )


class DistrictListFilter(admin.SimpleListFilter):
    title = 'district'
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.filter(
            kind__in=[
                Group.KIND.district,
                Group.KIND.noncomp,
                Group.KIND.affiliate
            ],
            status=Group.STATUS.active,
        ).order_by(
            'tree_sort',
        ).values_list('code', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(district=district)
        return queryset


class DivisionListFilter(admin.SimpleListFilter):
    title = 'division'
    parameter_name = 'division'

    def lookups(self, request, model_admin):
        divisions = Group.objects.filter(
            kind=Group.KIND.division,
            status=Group.STATUS.active,
        ).order_by(
            'tree_sort',
        ).values_list('name', 'name')
        return divisions

    def queryset(self, request, queryset):
        division = request.GET.get('division')
        if division:
            return queryset.filter(division=division)
        return queryset


class GroupListFilter(admin.SimpleListFilter):
    title = ('group')
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        orgs = Group.objects.filter(
            kind__lte=Group.KIND.division,
        ).values_list('id', 'code')
        return orgs

    def queryset(self, request, queryset):
        group = request.GET.get('group')
        if group:
            return queryset.filter(group=group)
        return queryset


class ParentGroupListFilter(admin.SimpleListFilter):
    title = ('parent')
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        orgs = Group.objects.filter(
            kind__lte=Group.KIND.division,
        ).values_list('id', 'code')
        return orgs

    def queryset(self, request, queryset):
        org = request.GET.get('org')
        if org:
            return queryset.filter(parent=org)
        return queryset


class ConventionGroupListFilter(admin.SimpleListFilter):
    title = ('district')
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.filter(
            kind__lte=Group.KIND.district,
        ).order_by(
            'tree_sort',
        ).values_list('id', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(group=district)
        return queryset


class SessionGroupListFilter(admin.SimpleListFilter):
    title = ('district')
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.filter(
            kind=Group.KIND.district,
        ).order_by(
            'tree_sort',
        ).values_list('id', 'code')
        return districts

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(convention__group=district)
        return queryset


class AssignmentFilter(FilterSet):
    class Meta:
        model = Assignment
        fields = {
            'person__user': [
                'exact',
            ],
            'status': [
                'exact',
            ],
            'convention__status': [
                'exact',
            ],
        }


class ConventionFilter(FilterSet):
    class Meta:
        model = Convention
        fields = {
            'assignments__person__user': [
                'exact',
            ],
            'assignments__status': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            'kind': [
                'gt',
            ],
            'officers__person__user': [
                'exact',
            ],
            'officers__status': [
                'exact',
            ],
            'members__person__user': [
                'exact',
            ],
            'members__status': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }


class OfficerFilter(FilterSet):
    class Meta:
        model = Officer
        fields = {
            'person__user': [
                'exact',
            ],
            'group__status': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }


class RoundFilter(FilterSet):
    class Meta:
        model = Round
        fields = {
            'session__convention__assignments__person__user': [
                'exact',
            ],
        }


class ScoreFilter(FilterSet):
    class Meta:
        model = Score
        fields = {
            'panelist': [
                'exact',
            ],
            'song__appearance': [
                'exact',
            ],
        }


class SessionFilter(FilterSet):
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
            'convention__assignments__person__user': [
                'exact',
            ],
            'convention__status': [
                'exact',
            ],
            'convention__assignments__category': [
                'exact',
            ],
        }


class StateLogFilter(FilterSet):
    class Meta:
        model = StateLog
        fields = {
            'object_id': [
                'exact',
            ],
        }


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'username': [
                'exact',
            ],
        }
