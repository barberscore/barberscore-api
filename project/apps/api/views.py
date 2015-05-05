import logging
log = logging.getLogger(__name__)

from rest_framework import viewsets

from .models import (
    Singer,
    Chorus,
    Quartet,
    Convention,
    Contest,
    Contestant,
    Performance,
)

from .serializers import (
    SingerSerializer,
    ChorusSerializer,
    QuartetSerializer,
    ConventionSerializer,
    ContestSerializer,
    ContestantSerializer,
    PerformanceSerializer,
)


class QuartetViewSet(viewsets.ModelViewSet):
    queryset = Quartet.objects.all()
    serializer_class = QuartetSerializer
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
    queryset = Convention.objects.all()
    serializer_class = ConventionSerializer
    # lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    # lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.all()
    serializer_class = ContestantSerializer
    # lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    # lookup_field = 'slug'
