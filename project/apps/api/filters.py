import django_filters

from .models import (
    Group,
)


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_type='icontains',
    )

    class Meta:
        model = Group
        fields = [
            'name',
        ]
