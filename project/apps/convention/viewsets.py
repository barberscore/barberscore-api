from rest_framework import viewsets

from .models import (
    Contest,
    Contestant,
    Performance,
)

from .serializers import (
    PerformanceSerializer,
    ContestSerializer,
    ContestantSerializer,
)


class ContestantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows contestants to be viewed or edited.
    """
    queryset = Contestant.objects.all()
    serializer_class = ContestantSerializer
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows performances to be viewed or edited.
    """
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class ContestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows contests to be viewed or edited.
    """
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_field = 'slug'
