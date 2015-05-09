import logging
log = logging.getLogger(__name__)

from rest_framework import (
    viewsets,
)

from .models import (
    Convention,
    Chorus,
    Quartet,
)

from .serializers import (
    ConventionSerializer,
    ChorusSerializer,
    QuartetSerializer,
)


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.filter(
        slug__startswith='bhs-summer',
    )
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ChorusViewSet(viewsets.ModelViewSet):
    queryset = Chorus.objects.all()
    serializer_class = ChorusSerializer
    lookup_field = 'slug'


class QuartetViewSet(viewsets.ModelViewSet):
    queryset = Quartet.objects.all()
    serializer_class = QuartetSerializer
    lookup_field = 'slug'
