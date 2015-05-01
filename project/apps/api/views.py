import logging
log = logging.getLogger(__name__)

from rest_framework import viewsets

from .models import (
    Singer,
    Chorus,
    Quartet,
    Convention,
    Contest,
    Performance,
)

from .serializers import (
    SingerSerializer,
    ChorusSerializer,
    QuartetSerializer,
    ConventionSerializer,
    ContestSerializer,
    PerformanceSerializer,
)


class QuartetViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Quartet.objects.all()
    serializer_class = QuartetSerializer


class SingerViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer


class ChorusViewSet(viewsets.ModelViewSet):
    queryset = Chorus.objects.all()
    serializer_class = ChorusSerializer
    lookup_field = 'slug'


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.all()
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    lookup_field = 'slug'
