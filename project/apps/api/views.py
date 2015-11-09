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
    Tune,
    Person,
    Song,
    Singer,
    Score,
    Director,
    Catalog,
    Panelist,
    Award,
    Performance,
    Organization,
)

from .serializers import (
    ConventionSerializer,
    ContestSerializer,
    GroupSerializer,
    ContestantSerializer,
    TuneSerializer,
    PersonSerializer,
    SearchSerializer,
    SongSerializer,
    SingerSerializer,
    ScoreSerializer,
    DirectorSerializer,
    CatalogSerializer,
    PanelistSerializer,
    AwardSerializer,
    PerformanceSerializer,
    OrganizationSerializer,
)


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'organization',
    ).exclude(
        status=Convention.STATUS.new,
    ).prefetch_related(
        'contests',
    )
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'organization',
        'convention',
    ).filter(
        history=Contest.HISTORY.complete,
    ).prefetch_related(
        'organization',
        'contestants',
    )
    serializer_class = ContestSerializer
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'group',
        'contest',
        'organization',
    ).prefetch_related(
        'performances',
        'directors',
        'singers',
        # 'awards',
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
        # 'catalogs',
        'choruses',
        'quartets',
        'panels',
    )
    serializer_class = PersonSerializer
    lookup_field = 'slug'


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'slug'


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'catalog',
        'performance',
    ).prefetch_related(
        'scores',
    )
    serializer_class = SongSerializer
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'contestant',
    ).prefetch_related(
        'songs',
    )
    serializer_class = PerformanceSerializer
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


class TuneViewSet(viewsets.ModelViewSet):
    queryset = Tune.objects.prefetch_related(
        # 'catalogs',
        'songs',
    )
    serializer_class = TuneSerializer
    lookup_field = 'slug'


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'panelist',
    )
    serializer_class = ScoreSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.select_related(
        'tune',
        'person',
    )
    serializer_class = CatalogSerializer
    lookup_field = 'slug'


class SearchViewSet(HaystackViewSet):
    serializer_class = SearchSerializer


class PanelistViewSet(viewsets.ModelViewSet):
    queryset = Panelist.objects.select_related(
        'person',
        'contest',
        'organization',
    ).prefetch_related(
        'scores',
    )
    serializer_class = PanelistSerializer
    lookup_field = 'slug'


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'contestant',
    )
    serializer_class = AwardSerializer
    lookup_field = 'slug'
