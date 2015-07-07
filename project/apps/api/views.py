import logging
log = logging.getLogger(__name__)

from rest_framework import (
    viewsets,
)

from drf_haystack.viewsets import HaystackViewSet

# from rest_framework.pagination import (
#     PageNumberPagination,
# )

from .models import (
    Convention,
    Contest,
    Group,
    Contestant,
    District,
    Song,
    Person,
    Performance,
    Singer,
    Director,
)

from .serializers import (
    ConventionSerializer,
    ContestSerializer,
    GroupSerializer,
    ContestantSerializer,
    DistrictSerializer,
    SongSerializer,
    PersonSerializer,
    SearchSerializer,
    PerformanceSerializer,
    SingerSerializer,
    DirectorSerializer,
)


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'district',
    ).filter(
        is_active=True,
    ).prefetch_related(
        'contests',
    )
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'district',
        'convention',
    ).filter(
        level=Contest.INTERNATIONAL,
        is_active=True,
    ).prefetch_related(
        'district',
        'contestants',
    )
    serializer_class = ContestSerializer
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'group',
        'contest',
        # 'performances',
        'district',
        # 'lead',
        # 'tenor',
        # 'baritone',
        # 'bass',
    ).prefetch_related(
        'performances',
        'directors',
        'singers',
    )
    serializer_class = ContestantSerializer
    # pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        'contestants',
    )
    serializer_class = GroupSerializer
    lookup_field = 'slug'


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related(
        'contestants_director',
        'contestants_lead',
        'contestants_tenor',
        'contestants_baritone',
        'contestants_bass',
    )
    serializer_class = PersonSerializer
    lookup_field = 'slug'


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.prefetch_related(
        'contestants',
    )
    serializer_class = DistrictSerializer
    # pagination_class = PageNumberPagination
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'song',
        'arranger',
    )
    serializer_class = PerformanceSerializer
    lookup_field = 'slug'


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    lookup_field = 'slug'


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'slug'


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.prefetch_related(
        'contestants_finals_song1',
        'contestants_finals_song2',
        'contestants_semis_song1',
        'contestants_semis_song2',
        'contestants_quarters_song1',
        'contestants_quarters_song2',
        'contestants_finals_song1',
        'contestants_finals_song2',
        'contestants_semis_song1',
        'contestants_semis_song2',
        'contestants_quarters_song1',
        'contestants_quarters_song2',
    )
    serializer_class = SongSerializer
    lookup_field = 'slug'


class SearchViewSet(HaystackViewSet):
    serializer_class = SearchSerializer
