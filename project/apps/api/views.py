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
    Catalog,
    Judge,
    Award,
    Appearance,
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
    CatalogSerializer,
    JudgeSerializer,
    AwardSerializer,
    AppearanceSerializer,
)


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'district',
    ).exclude(
        status=Convention.STATUS.new,
    ).prefetch_related(
        'contests',
    )
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'district',
        'convention',
    ).exclude(
        status=Contest.STATUS.new,
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
        'district',
    ).prefetch_related(
        'appearances',
        'directors',
        'singers',
        'awards',
    )
    serializer_class = ContestantSerializer
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        'contestants',
    )
    serializer_class = GroupSerializer
    lookup_field = 'slug'


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related(
        'catalogs',
        'choruses',
        'quartets',
        'panels',
    )
    serializer_class = PersonSerializer
    lookup_field = 'slug'


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.prefetch_related(
        'contestants',
    )
    serializer_class = DistrictSerializer
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'catalog',
        'appearance',
    ).prefetch_related(
        'scores',
    )
    serializer_class = PerformanceSerializer
    lookup_field = 'slug'


class AppearanceViewSet(viewsets.ModelViewSet):
    queryset = Appearance.objects.select_related(
        'contestant',
    ).prefetch_related(
        'performances',
    )
    serializer_class = AppearanceSerializer
    lookup_field = 'slug'


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.select_related(
        'person',
        'contestant',
    )
    serializer_class = SingerSerializer
    lookup_field = 'slug'


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.select_related(
        'person',
        'contestant',
    )
    serializer_class = DirectorSerializer
    lookup_field = 'slug'


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.prefetch_related(
        'catalogs',
        'performances',
    )
    serializer_class = SongSerializer
    lookup_field = 'slug'


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'performance',
        'judge',
    )
    serializer_class = ScoreSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.select_related(
        'song',
        'person',
    )
    serializer_class = CatalogSerializer
    lookup_field = 'slug'


class SearchViewSet(HaystackViewSet):
    serializer_class = SearchSerializer


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'person',
        'contest',
        'district',
    ).prefetch_related(
        'scores',
    )
    serializer_class = JudgeSerializer
    lookup_field = 'slug'


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'contestant',
    )
    serializer_class = AwardSerializer
    lookup_field = 'slug'
