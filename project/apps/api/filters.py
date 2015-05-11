import django_filters

from .models import (
    Quartet,
    Chorus,
)


class ChorusFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_type='icontains',
    )

    class Meta:
        model = Chorus
        fields = [
            'name',
        ]


class QuartetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_type='icontains',
    )

    class Meta:
        model = Quartet
        fields = [
            'name',
        ]
