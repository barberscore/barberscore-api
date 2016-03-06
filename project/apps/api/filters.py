import rest_framework_filters as filters

from .models import (
    Chart,
    Convention,
    Group,
    Person,
    Venue,
)


class ChartFilter(filters.FilterSet):
    class Meta:
        model = Chart
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class ConventionFilter(filters.FilterSet):
    class Meta:
        model = Convention
        fields = {
            'status': filters.ALL_LOOKUPS,
            'year': filters.ALL_LOOKUPS,
        }


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class PersonFilter(filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class VenueFilter(filters.FilterSet):
    class Meta:
        model = Venue
        fields = {
            'name': filters.ALL_LOOKUPS,
        }
