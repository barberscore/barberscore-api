import rest_framework_filters as filters

from .models import (
    Convention,
    Person,
    Award,
    Group,
)


class ConventionFilter(filters.FilterSet):
    class Meta:
        model = Convention
        fields = {
            'status': filters.ALL_LOOKUPS,
        }


class PersonFilter(filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class AwardFilter(filters.FilterSet):
    class Meta:
        model = Award
        fields = {
            'name': filters.ALL_LOOKUPS,
        }


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'name': filters.ALL_LOOKUPS,
        }
