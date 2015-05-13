import django_filters

from .models import (
    Group,
    Performance,
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


class ScheduleFilter(django_filters.FilterSet):
    day = django_filters.CharFilter(
        name='stagetime',
        lookup_type='week_day',
    )

    class Meta:
        model = Performance
        fields = [
            'day',
        ]
        order_by = [
            'stagetime',
        ]
