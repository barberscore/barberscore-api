import logging
log = logging.getLogger(__name__)

from rest_framework import (
    viewsets,
    permissions,
)

from drf_haystack.viewsets import HaystackViewSet

from .filters import (
    ConventionFilter,
    PersonFilter,
    GroupFilter,
    TuneFilter,
)


from .models import (
    Arranger,
    Award,
    Catalog,
    Chapter,
    Contestant,
    Convention,
    Director,
    Group,
    Judge,
    Organization,
    Performance,
    Performer,
    Person,
    Round,
    Score,
    Session,
    Singer,
    Song,
    Tune,
)

from .serializers import (
    ArrangerSerializer,
    AwardSerializer,
    CatalogSerializer,
    ChapterSerializer,
    ContestantSerializer,
    ConventionSerializer,
    DirectorSerializer,
    GroupSearchSerializer,
    GroupSerializer,
    JudgeSerializer,
    OrganizationSerializer,
    PerformanceSerializer,
    PerformerSerializer,
    PersonSearchSerializer,
    PersonSerializer,
    RoundSerializer,
    ScoreSerializer,
    SessionSerializer,
    SingerSerializer,
    SongSerializer,
    TuneSerializer,
)


class ArrangerViewSet(viewsets.ModelViewSet):
    queryset = Arranger.objects.select_related(
        'catalog',
        'person',
    )
    serializer_class = ArrangerSerializer
    # lookup_field = 'slug'
    resource_name = "arranger"


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'organization',
    ).prefetch_related(
        'contestants',
    )
    serializer_class = AwardSerializer
    # lookup_field = 'slug'
    resource_name = "award"


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.select_related(
        'organization',
    )
    serializer_class = ChapterSerializer
    # lookup_field = 'slug'
    resource_name = "chapter"


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.select_related(
        'tune',
    ).prefetch_related(
        'arrangers',
    )
    serializer_class = CatalogSerializer
    # lookup_field = 'slug'
    resource_name = "catalog"


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
    )
    serializer_class = ContestantSerializer
    resource_name = 'contestant'
    # lookup_field = 'slug'
    resource_name = "contestant"


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related(
        'convention',
        'administrator',
    ).prefetch_related(
        'performers',
        'rounds',
        'judges',
    )
    serializer_class = SessionSerializer
    # lookup_field = 'slug'
    resource_name = "session"


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.select_related(
        'session',
        'organization',
    ).prefetch_related(
        'performances',
        'contestants',
        # 'directors',
        # 'singers',
    )
    serializer_class = PerformerSerializer
    # lookup_field = 'slug'
    resource_name = "performer"


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'organization',
    ).prefetch_related(
        'sessions',
    )
    serializer_class = ConventionSerializer
    # lookup_field = 'slug'
    resource_name = "convention"
    filter_class = ConventionFilter


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.select_related(
        'person',
        'performer',
    )
    serializer_class = DirectorSerializer
    # lookup_field = 'slug'
    resource_name = "director"


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        'performers',
    )
    serializer_class = GroupSerializer
    # lookup_field = 'slug'
    resource_name = "group"
    filter_fields = (
        'name',
    )
    filter_class = GroupFilter




class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'session',
        'person',
        'organization',
    ).prefetch_related(
        'scores',
    )
    serializer_class = JudgeSerializer
    # lookup_field = 'slug'
    resource_name = "judge"


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.exclude(level=2)
    serializer_class = OrganizationSerializer
    # lookup_field = 'slug'
    resource_name = "organization"


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'round',
        'performer',
    ).prefetch_related(
        'songs',
    )
    serializer_class = PerformanceSerializer
    # lookup_field = 'slug'
    resource_name = "performance"


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related(
        # 'catalogs',
        'choruses',
        'quartets',
    )
    serializer_class = PersonSerializer
    # lookup_field = 'slug'
    resource_name = "person"
    filter_fields = (
        'name',
    )
    filter_class = PersonFilter


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'judge',
    )
    serializer_class = ScoreSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]
    resource_name = "score"


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'performances',
    )
    serializer_class = RoundSerializer
    # lookup_field = 'slug'
    resource_name = "round"


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.select_related(
        'person',
        'performer',
    )
    serializer_class = SingerSerializer
    # lookup_field = 'slug'
    resource_name = "singer"


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'catalog',
        'performance',
    ).prefetch_related(
        'scores',
    )
    serializer_class = SongSerializer
    # lookup_field = 'slug'
    resource_name = "song"


class TuneViewSet(viewsets.ModelViewSet):
    queryset = Tune.objects.prefetch_related(
        # 'catalogs',
        'songs',
    )
    serializer_class = TuneSerializer
    # lookup_field = 'slug'
    resource_name = "tune"
    filter_fields = (
        'name',
    )
    filter_class = TuneFilter
