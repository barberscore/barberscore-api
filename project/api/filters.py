# Third-Party
from django_filters.rest_framework import (
    FilterSet,
    OrderingFilter,
)

from django_filters import (
    UUIDFilter,
    NumberFilter,
    CharFilter,
)


from django.contrib import admin

# Local
from .models import (
    Award,
    Chart,
    Contestant,
    Convention,
    Competitor,
    Entry,
    Grantor,
    Group,
    Member,
    Office,
    Officer,
    Organization,
    Panelist,
    Participant,
    Person,
    Round,
    Score,
    Session,
    Venue,
)


class DistrictListFilter(admin.SimpleListFilter):
    title = 'district'
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        districts = Group.objects.order_by(
            'district',
        ).values_list('district', 'district').distinct()
        return tuple(districts)

    def queryset(self, request, queryset):
        district = request.GET.get('district')
        if district:
            return queryset.filter(district=district)
        return queryset


class DivisionListFilter(admin.SimpleListFilter):
    title = 'division'
    parameter_name = 'division'

    def lookups(self, request, model_admin):
        divisions = Group.objects.order_by(
            'division',
        ).values_list('division', 'division').distinct()
        return tuple(divisions)

    def queryset(self, request, queryset):
        division = request.GET.get('division')
        if division:
            return queryset.filter(division=division)
        return queryset


class OrganizationListFilter(admin.SimpleListFilter):
    title = ('organization')
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        orgs = Organization.objects.filter(
            kind__lte=Organization.KIND.division,
        ).values_list('id', 'code')
        return tuple(orgs)

    def queryset(self, request, queryset):
        org = request.GET.get('org')
        if org:
            return queryset.filter(organization=org)
        return queryset


class ParentOrganizationListFilter(admin.SimpleListFilter):
    title = ('parent')
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        orgs = Organization.objects.filter(
            kind__lte=Organization.KIND.division,
        ).values_list('id', 'code')
        return tuple(orgs)

    def queryset(self, request, queryset):
        org = request.GET.get('org')
        if org:
            return queryset.filter(parent=org)
        return queryset


class ConventionOrganizationListFilter(admin.SimpleListFilter):
    title = ('organization')
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        orgs = Organization.objects.filter(
            kind__lte=Organization.KIND.district,
        ).values_list('id', 'code')
        return tuple(orgs)

    def queryset(self, request, queryset):
        org = request.GET.get('org')
        if org:
            return queryset.filter(organization=org)
        return queryset


class SessionOrganizationListFilter(admin.SimpleListFilter):
    title = ('organization')
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        orgs = Organization.objects.filter(
            kind__lte=Organization.KIND.district,
        ).values_list('id', 'code')
        return tuple(orgs)

    def queryset(self, request, queryset):
        org = request.GET.get('org')
        if org:
            return queryset.filter(convention__organization=org)
        return queryset


class AwardFilter(FilterSet):
    class Meta:
        model = Award
        fields = {
            'nomen': [
                'icontains',
            ],
            'kind': [
                'exact',
            ],
            'gender': [
                'exact',
            ],
            'season': [
                'exact',
            ],
            'status': [
                'exact',
            ],
            'organization': [
                'exact',
            ],
            'organization__parent': [
                'exact',
            ],
            'organization__name': [
                'exact',
            ],
            'organization__kind': [
                'exact',
            ],
            'organization__officers__office__short_name': [
                'exact',
            ],
            'organization__officers__person__user': [
                'exact',
            ],
            'organization__officers__office__is_award_manager': [
                'exact',
            ],
            'organization__officers__status': [
                'exact',
                'gt',
            ],
            'organization__grantors__convention': [
                'exact',
            ],
        }


class ChartFilter(FilterSet):
    class Meta:
        model = Chart
        fields = {
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gte',
            ],
        }


class ContestantFilter(FilterSet):
    class Meta:
        model = Contestant
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class ConventionFilter(FilterSet):
    class Meta:
        model = Convention
        fields = {
            'status': [
                'exact',
                'lt',
            ],
            'year': [
                'exact',
            ],
            'assignments__person__user': [
                'exact',
            ],
            'organization__officers__person__user': [
                'exact',
            ],
            'assignments__kind': [
                'exact',
            ],
            'assignments__category': [
                'exact',
            ],
        }


class CompetitorFilter(FilterSet):
    class Meta:
        model = Competitor
        fields = {
            'nomen': [
                'icontains',
            ],
            'is_archived': [
                'exact',
            ],
        }


class EntryFilter(FilterSet):
    class Meta:
        model = Entry
        fields = {
            'nomen': [
                'icontains',
            ],
            'is_archived': [
                'exact',
            ],
        }


class GrantorFilter(FilterSet):
    class Meta:
        model = Grantor
        fields = {
            'status': [
                'exact',
            ],
            'organization': [
                'exact',
            ],
            'convention': [
                'exact',
            ],
        }


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            'id': [
                'exact',
            ],
            'kind': [
                'exact',
                'lt',
                'in',
                'lte',
            ],
            'gender': [
                'exact',
            ],
            'organization': [
                'exact',
            ],
            'members__person__user': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gt',
            ],
        }


class PanelistFilter(FilterSet):
    class Meta:
        model = Panelist
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class ParticipantFilter(FilterSet):
    class Meta:
        model = Participant
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class MemberFilter(FilterSet):
    class Meta:
        model = Member
        fields = {
            'group': [
                'exact',
            ],
            'person__user': [
                'exact',
            ],
            'is_admin': [
                'exact',
            ],
            'status': [
                'gte',
                'exact',
            ]
        }


class OfficeFilter(FilterSet):
    class Meta:
        model = Office
        fields = {
            'kind': [
                'exact',
            ],
        }


class OfficerFilter(FilterSet):
    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('office__name', 'officeName'),
        ),

        # labels do not need to retain order
        field_labels={
            'office__name': 'Office',
        }
    )

    class Meta:
        model = Officer
        fields = {
            'nomen': [
                'icontains',
            ],
            'office__short_name': [
                'exact',
            ],
            'office__kind': [
                'exact',
            ],
        }


class OrganizationFilter(FilterSet):
    class Meta:
        model = Organization
        fields = {
            'id': [
                'exact',
            ],
            'kind': [
                'exact',
                'lt',
                'in',
                'lte',
            ],
            'parent': [
                'exact',
            ],
            'officers__person__user': [
                'exact',
            ],
            'officers__office__is_award_manager': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gt',
            ],
        }


class PersonFilter(FilterSet):
    class Meta:
        model = Person
        fields = {
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
            ],
            'user': [
                'exact',
            ],
            'officers__office__kind': [
                'exact',
            ],
            'officers__office__is_judge_manager': [
                'exact',
            ],
        }


class RoundFilter(FilterSet):
    class Meta:
        model = Round
        fields = {
            'session__convention__status': [
                'exact',
            ],
            'session__convention__assignments__person__user': [
                'exact',
            ],
            'session__convention__year': [
                'exact',
            ],
            'status': [
                'exact',
                'lt',
            ],
        }


class ScoreFilter(FilterSet):
    class Meta:
        model = Score
        fields = {
            'song__appearance': [
                'exact',
            ],
        }


class SessionFilter(FilterSet):
    convention__assignments__person__user = UUIDFilter(
        field_name='convention__assignments__person__user',
        lookup_expr='exact',
        distinct=True,
    )

    convention__assignments__kind = NumberFilter(
        field_name='convention__assignments__kind',
        lookup_expr='exact',
        distinct=True,
    )

    convention__assignments__category = NumberFilter(
        field_name='convention__assignments__category',
        lookup_expr='exact',
        distinct=True,
    )

    status__lt = NumberFilter(
        field_name='status',
        lookup_expr='lt',
        distinct=True,
    )

    status = NumberFilter(
        field_name='status',
        lookup_expr='exact',
        distinct=True,
    )

    nomen__icontains = CharFilter(
        field_name='status',
        lookup_expr='icontains',
        distinct=True,
    )

    class Meta:
        model = Session
        fields = [
            'status',
            'status__lt',
            'is_archived',
            'kind',
            'gender',
            'convention',
            'is_invitational',
            'convention__status',
            'nomen__icontains',
            'convention__assignments__person__user',
            'convention__assignments__kind',
            'convention__assignments__category',
        ]


class VenueFilter(FilterSet):
    class Meta:
        model = Venue
        fields = {
            'nomen': [
                'icontains',
            ],
        }
