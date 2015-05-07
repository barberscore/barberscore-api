import logging
log = logging.getLogger(__name__)

import django_filters

from rest_framework import (
    viewsets,
    filters,
)

from .models import (
    Singer,
    Chorus,
    Quartet,
    Convention,
    Contest,
    Contestant,
    District,
    Performance,
)

from .serializers import (
    SingerSerializer,
    ChorusSerializer,
    QuartetSerializer,
    DistrictSerializer,
    ConventionSerializer,
    ContestSerializer,
    ContestantSerializer,
    PerformanceSerializer,
)


class PerformanceFilter(django_filters.FilterSet):
    convention = django_filters.CharFilter(
        name="contestant__contest__convention__slug",
    )

    contest = django_filters.CharFilter(
        name="contestant__contest__kind",
    )

    class Meta:
        model = Performance
        fields = [
            'round',
            'convention',
            'contest',
        ]
        ordering = [

        ]


class QuartetViewSet(viewsets.ModelViewSet):
    queryset = Quartet.objects.all()
    serializer_class = QuartetSerializer
    # lookup_field = 'slug'


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    # lookup_field = 'slug'


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    # lookup_field = 'slug'


class ChorusViewSet(viewsets.ModelViewSet):
    queryset = Chorus.objects.all()
    serializer_class = ChorusSerializer
    # lookup_field = 'slug'


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.all().prefetch_related('contests')
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all().prefetch_related('contestants')
    serializer_class = ContestSerializer
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.all().prefetch_related('performances')
    serializer_class = ContestantSerializer
    lookup_field = 'slug'
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('place',)
    ordering = [
        'place',
    ]


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    lookup_field = 'slug'
    filter_class = PerformanceFilter
