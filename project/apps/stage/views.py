from rest_framework import viewsets
from rest_framework_json_api.django_filters import DjangoFilterBackend
from dry_rest_permissions.generics import DRYPermissions

from .models import Grid
from .models import Venue

from .serializers import GridSerializer
from .serializers import VenueSerializer


class GridViewSet(viewsets.ModelViewSet):
    queryset = Grid.objects.select_related(
        'round',
        'venue',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = GridSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "grid"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.select_related(
    ).prefetch_related(
        'conventions',
        'grids',
    ).order_by('name')
    serializer_class = VenueSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "venue"
