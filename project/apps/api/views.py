import logging

from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import (
    viewsets,
    permissions,
    status,
)

# from drf_haystack.viewsets import HaystackViewSet

from .filters import (
    ConventionFilter,
    PersonFilter,
    GroupFilter,
    VenueFilter,
)


from .models import (
    Award,
    Chapter,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Organization,
    Performance,
    Performer,
    Person,
    Round,
    Score,
    Session,
    Setlist,
    Role,
    Song,
    Venue,
)

from .serializers import (
    AwardSerializer,
    ChapterSerializer,
    ContestSerializer,
    ContestantSerializer,
    ConventionSerializer,
    GroupSerializer,
    JudgeSerializer,
    OrganizationSerializer,
    PerformanceSerializer,
    PerformerSerializer,
    PersonSerializer,
    RoundSerializer,
    ScoreSerializer,
    SessionSerializer,
    SetlistSerializer,
    RoleSerializer,
    SongSerializer,
    VenueSerializer,
)

log = logging.getLogger(__name__)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'organization',
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


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        'award',
        'parent',
    ).prefetch_related(
        'contestants',
    )
    serializer_class = ContestSerializer
    resource_name = 'contest'
    # lookup_field = 'slug'
    resource_name = "contest"


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
        'contest',
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
        'contests',
    )
    serializer_class = SessionSerializer
    # lookup_field = 'slug'
    resource_name = "session"


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.select_related(
        'session',
        'organization',
        'group',
    ).prefetch_related(
        'performances',
        'contestants',
        'roles',
    )
    serializer_class = PerformerSerializer
    # lookup_field = 'slug'
    resource_name = "performer"


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'organization',
        'venue',
    ).prefetch_related(
        'sessions',
    )
    serializer_class = ConventionSerializer
    # lookup_field = 'slug'
    resource_name = "convention"
    filter_class = ConventionFilter


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


class SetlistViewSet(viewsets.ModelViewSet):
    queryset = Setlist.objects.select_related(
        'performer',
        'chart',
    )
    serializer_class = SetlistSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]
    resource_name = "setlist"


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'performances',
    )
    serializer_class = RoundSerializer
    # lookup_field = 'slug'
    resource_name = "round"

    @detail_route(methods=['put'])
    def draw(self, request, pk=None):
        round = self.get_object()
        response = round.draw()
        if response:
            return Response(response)
        else:
            return Response(
                {'error': 'did not draw'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related(
        'person',
        'performer',
    )
    serializer_class = RoleSerializer
    # lookup_field = 'slug'
    resource_name = "role"


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'catalog',
        'performance',
        'tune',
    ).prefetch_related(
        'scores',
    )
    serializer_class = SongSerializer
    # lookup_field = 'slug'
    resource_name = "song"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.prefetch_related(
        'conventions',
    )
    serializer_class = VenueSerializer
    # lookup_field = 'slug'
    resource_name = "venue"
    filter_fields = (
        'name',
    )
    filter_class = VenueFilter
