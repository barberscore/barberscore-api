import logging
log = logging.getLogger(__name__)

from rest_framework import (
    viewsets,
    permissions,
)

from drf_haystack.viewsets import HaystackViewSet

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
    Score,
    Director,
    Arrangement,
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
    ScoreSerializer,
    DirectorSerializer,
    ArrangementSerializer,
    ScheduleSerializer,
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


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'district',
        'convention',
    ).filter(
        is_active=True,
    ).prefetch_related(
        'district',
        'contestants',
    )
    serializer_class = ContestSerializer


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'group',
        'contest',
        'district',
    ).prefetch_related(
        'performances',
        'directors',
        'singers',
    )
    serializer_class = ContestantSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        'contestants',
    )
    serializer_class = GroupSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related(
        'arrangements',
        'choruses',
        'quartets',
    )
    serializer_class = PersonSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.prefetch_related(
        'contestants',
    )
    serializer_class = DistrictSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'arrangement',
        'contestant',
    )
    serializer_class = PerformanceSerializer


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.select_related(
        'person',
        'contestant',
    )
    serializer_class = SingerSerializer


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.select_related(
        'person',
        'contestant',
    )
    serializer_class = DirectorSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.prefetch_related(
        'arrangements',
    )
    serializer_class = SongSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]


class ArrangementViewSet(viewsets.ModelViewSet):
    queryset = Arrangement.objects.select_related(
        'song',
        'arranger',
    )
    serializer_class = ArrangementSerializer


class SearchViewSet(HaystackViewSet):
    serializer_class = SearchSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'group',
        'contest',
        'district',
    ).prefetch_related(
        'performances',
        'directors',
        'singers',
    )
    serializer_class = ScheduleSerializer
