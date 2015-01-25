from rest_framework import viewsets

from .models import (
    Singer,
    Chorus,
)

from .serializers import (
    SingerSerializer,
    ChorusSerializer,
)


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer


class ChorusViewSet(viewsets.ModelViewSet):
    queryset = Chorus.objects.all()
    serializer_class = ChorusSerializer
