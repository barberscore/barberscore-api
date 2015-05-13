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

from .filters import (
    ScheduleFilter,
    GroupFilter,
)


from .serializers import (
    ConventionSerializer,
    ContestSerializer,
    GroupSerializer,
    ContestantSerializer,
    PerformanceSerializer,
    ScheduleSerializer,

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
            # 'Pittsburgh 2015',
        ]
    ).prefetch_related('contests')
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'convention',
    ).all().prefetch_related('contestants')
    serializer_class = ContestSerializer
    # filter_class = ChorusFilter
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'contest', 'group',
    ).all().prefetch_related('performances')
    serializer_class = ContestantSerializer
    # filter_class = QuartetFilter
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'lead', 'tenor', 'baritone', 'bass'
    ).all().prefetch_related('contestants')
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    # filter_class = PerformanceFilter
    lookup_field = 'slug'


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'contestant__contest',
        'contestant__group',
    ).filter(
        contestant__contest__convention__name='Pittsburgh 2015'
    )
    serializer_class = ScheduleSerializer
    filter_class = ScheduleFilter
