import rest_framework_filters as filters
from rest_framework.filters import BaseFilterBackend

from django_filters import Filter
from django_filters.fields import Lookup

from .models import (
    Chart,
    Certification,
    Contestant,
    Convention,
    Group,
    Person,
    Performer,
    Submission,
    Venue,
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


class ListFilter(Filter):
    def filter(self, qs, value):
        value_list = value.split(u',')
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))


class ChartFilter(filters.FilterSet):
    class Meta:
        model = Chart
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class ConventionFilter(filters.FilterSet):
    season = ListFilter(name='season')

    class Meta:
        model = Convention
        fields = {
            'status': filters.ALL_LOOKUPS,
            'year': filters.ALL_LOOKUPS,
            # 'season': filters.ALL_LOOKUPS,
        }


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'chap_name': filters.ALL_LOOKUPS,
        }


class CertificationFilter(filters.FilterSet):
    class Meta:
        model = Certification
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class ContestantFilter(filters.FilterSet):
    class Meta:
        model = Contestant
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class PerformerFilter(filters.FilterSet):
    class Meta:
        model = Performer
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class PersonFilter(filters.FilterSet):
    certifications__category = ListFilter(name='certifications__category')

    class Meta:
        model = Person
        fields = [
            'status',
        ]
        fields = {
            'name': filters.ALL_LOOKUPS,
            # 'status': filters.ALL_LOOKUPS,
            # 'certifications__category': filters.ALL_LOOKUPS,
        }


class SubmissionFilter(filters.FilterSet):
    class Meta:
        model = Submission
        fields = {
            'chart__name': filters.ALL_LOOKUPS,
            'performer__id': filters.ALL_LOOKUPS,
        }


class VenueFilter(filters.FilterSet):
    class Meta:
        model = Venue
        fields = {
            'name': filters.ALL_LOOKUPS,
        }
