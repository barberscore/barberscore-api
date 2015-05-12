import logging
log = logging.getLogger(__name__)

# import watson

from rest_framework import (
    # mixins,
    viewsets,
    # filters,
)

from .models import (
    Convention,
    Contest,
    Group,
    Contestant,
    Performance,
)

# from .filters import (
#     # ChorusFilter,
#     # QuartetFilter,
# )


from .serializers import (
    ConventionSerializer,
    ContestSerializer,
    GroupSerializer,
    ContestantSerializer,
    PerformanceSerializer,

    # SearchSerializer,
)


# class SearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

#     serializer_class = SearchSerializer

#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         term = request.GET.get('q', None)
#         if term:
#             queryset = watson.search(term)
#         else:
#             queryset = None
#         return queryset


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.filter(
        name__in=[
            'Philadelphia 2010',
            'Kansas City 2011',
            'Portland 2012',
            'Toronto 2013',
            'Las Vegas 2014',
            'Pittsburgh 2015',
        ]
    ).prefetch_related('contests')
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all().prefetch_related('contestants')
    serializer_class = ContestSerializer
    # filter_class = ChorusFilter
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.all().prefetch_related('performances', 'group')
    serializer_class = ContestantSerializer
    # filter_class = QuartetFilter
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # filter_class = QuartetFilter
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    # filter_class = QuartetFilter
    lookup_field = 'slug'
