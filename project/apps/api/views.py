import logging
log = logging.getLogger(__name__)

from rest_framework import (
    viewsets,
    permissions,
)

from drf_haystack.viewsets import HaystackViewSet

from .models import (
    Convention,
    Session,
    Award,
    Competitor,
    Round,
    Group,
    Contestant,
    Tune,
    Person,
    Song,
    Singer,
    Score,
    Director,
    Catalog,
    Judge,
    Performance,
    Organization,
)

from .serializers import (
    ConventionSerializer,
    SessionSerializer,
    AwardSerializer,
    CompetitorSerializer,
    RoundSerializer,
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
    JudgeSerializer,
    PerformanceSerializer,
    OrganizationSerializer,
)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'session',
        'organization',
    ).filter(
        # history=Session.HISTORY.complete,
    ).prefetch_related(
        'competitors',
    )
    serializer_class = AwardSerializer
    lookup_field = 'slug'


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.select_related(
        'tune',
        'person',
    )
    serializer_class = CatalogSerializer
    lookup_field = 'slug'


class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.select_related(
        'award',
        'contestant',
    )
    serializer_class = CompetitorSerializer
    lookup_field = 'slug'


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related(
        'convention',
    ).filter(
        # history=Session.HISTORY.complete,
    ).prefetch_related(
        'awards',
        'contestants',
        'rounds',
        'judges',
    )
    serializer_class = SessionSerializer
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'session',
        'organization',
    ).prefetch_related(
        'performances',
        'competitors',
        'directors',
        'singers',
    )
    serializer_class = ContestantSerializer
    lookup_field = 'slug'


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'organization',
    ).exclude(
        status=Convention.STATUS.new,
    ).prefetch_related(
        'sessions',
    )
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.select_related(
        'person',
        'contestant',
    )
    serializer_class = DirectorSerializer
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        'contestants',
    )
    serializer_class = GroupSerializer
    lookup_field = 'slug'


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'session',
        'person',
        'organization',
    ).prefetch_related(
        'scores',
    )
    serializer_class = JudgeSerializer
    lookup_field = 'slug'


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'round',
        'contestant',
    ).prefetch_related(
        'songs',
    )
    serializer_class = PerformanceSerializer
    lookup_field = 'slug'


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related(
        # 'catalogs',
        'choruses',
        'quartets',
        'sessions',
    )
    serializer_class = PersonSerializer
    lookup_field = 'slug'


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'judge',
    )
    serializer_class = ScoreSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]


class SearchViewSet(HaystackViewSet):
    serializer_class = SearchSerializer


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'performances',
    )
    serializer_class = RoundSerializer
    lookup_field = 'slug'


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.select_related(
        'person',
        'contestant',
    )
    serializer_class = SingerSerializer
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


class TuneViewSet(viewsets.ModelViewSet):
    queryset = Tune.objects.prefetch_related(
        # 'catalogs',
        'songs',
    )
    serializer_class = TuneSerializer
    lookup_field = 'slug'
