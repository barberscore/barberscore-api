import rest_framework_filters as filters

from django_filters import Filter
from django_filters.fields import Lookup

from .models import (
    Chart,
    Convention,
    Group,
    Person,
    Venue,
)


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


class VenueFilter(filters.FilterSet):
    class Meta:
        model = Venue
        fields = {
            'name': filters.ALL_LOOKUPS,
        }
