# Third-Party
import rest_framework_filters as filters
from django_filters import Filter
from django_filters.fields import Lookup
from rest_framework.filters import BaseFilterBackend

# Local
from .models import (
    Certification,
    Chart,
    Contestant,
    Convention,
    Group,
    Performer,
    Person,
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
            'name': '__all__',
        }


class ConventionFilter(filters.FilterSet):
    season = ListFilter(name='season')

    class Meta:
        model = Convention
        fields = {
            'status': '__all__',
            'year': '__all__',
            # 'season': '__all__',
        }


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'chap_name': '__all__',
            'kind': '__all__',
        }


class CertificationFilter(filters.FilterSet):
    class Meta:
        model = Certification
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
    class Meta:
        model = Performer
        fields = {
            'name': '__all__',
        }


class PersonFilter(filters.FilterSet):
    certifications__category = ListFilter(name='certifications__category')

    class Meta:
        model = Person
        fields = [
            'status',
        ]
        fields = {
            'name': '__all__',
            'id_name': '__all__',
            # 'certifications__category': '__all__',
        }


class SubmissionFilter(filters.FilterSet):
    class Meta:
        model = Submission
        fields = {
            'chart__name': '__all__',
            'performer__id': '__all__',
        }


class VenueFilter(filters.FilterSet):
    class Meta:
        model = Venue
        fields = {
            'name': '__all__',
        }
