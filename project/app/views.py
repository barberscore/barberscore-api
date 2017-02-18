# Standard Libary
import logging

# Third-Party
from django_filters.rest_framework import DjangoFilterBackend
from drf_fsm_transitions.viewset_mixins import \
    get_viewset_transition_action_mixin
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import (
    detail_route,
    list_route,
    parser_classes,
)
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

# Local
from .backends import (
    CoalesceFilterBackend,
    ContestPrivateFilterBackend,
    PerformancePrivateFilterBackend,
    PerformerScoreFilterBackend,
    ScoreFilterBackend,
    SongScoreFilterBackend,
)
from .filters import (
    AwardFilter,
    CatalogFilter,
    ContestantFilter,
    ConventionFilter,
    EntityFilter,
    PerformerFilter,
    PersonFilter,
    SessionFilter,
    SubmissionFilter,
    VenueFilter,
)
from .models import (
    Assignment,
    Award,
    Catalog,
    Contest,
    Contestant,
    ContestantPrivate,
    ContestPrivate,
    Convention,
    Entity,
    Host,
    Membership,
    Office,
    Officer,
    Performance,
    PerformancePrivate,
    Performer,
    PerformerScore,
    Person,
    Round,
    Score,
    Session,
    Slot,
    Song,
    SongScore,
    Submission,
    User,
    Venue,
)

from .paginators import PageNumberPagination

from .serializers import (
    AssignmentSerializer,
    AwardSerializer,
    CatalogSerializer,
    ContestantPrivateSerializer,
    ContestantSerializer,
    ContestPrivateSerializer,
    ContestSerializer,
    ConventionSerializer,
    EntitySerializer,
    HostSerializer,
    MembershipSerializer,
    OfficeCSVSerializer,
    OfficerSerializer,
    OfficeSerializer,
    PerformancePrivateSerializer,
    PerformanceSerializer,
    PerformerScoreSerializer,
    PerformerSerializer,
    PersonSerializer,
    RoundSerializer,
    ScoreSerializer,
    SessionSerializer,
    SlotSerializer,
    SongScoreSerializer,
    SongSerializer,
    SubmissionSerializer,
    UserSerializer,
    VenueSerializer,
)

log = logging.getLogger(__name__)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        'convention',
        'person',
    ).prefetch_related(
    )
    serializer_class = AssignmentSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "assignment"


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'entity',
    ).prefetch_related(
        'contests',
    )
    serializer_class = AwardSerializer
    filter_class = AwardFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "award"


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.select_related(
    ).prefetch_related(
        'submissions',
    )
    serializer_class = CatalogSerializer
    filter_class = CatalogFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "catalog"


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        'award',
    ).prefetch_related(
        'primary_session',
    )
    serializer_class = ContestSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contest"


class ContestPrivateViewSet(viewsets.ModelViewSet):
    queryset = ContestPrivate.objects.select_related(
    ).prefetch_related(
    )
    serializer_class = ContestPrivateSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        ContestPrivateFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contestprivate"


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
        'contest',
    ).prefetch_related(
    )
    serializer_class = ContestantSerializer
    filter_class = ContestantFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contestant"


class ContestantPrivateViewSet(viewsets.ModelViewSet):
    queryset = ContestantPrivate.objects.select_related(
    ).prefetch_related(
    )
    serializer_class = ContestantPrivateSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contestantprivate"


class ConventionViewSet(
    get_viewset_transition_action_mixin(Convention),
    viewsets.ModelViewSet
):
    queryset = Convention.objects.select_related(
        'venue',
    ).prefetch_related(
        'assignments',
        'hosts',
    )
    serializer_class = ConventionSerializer
    filter_class = ConventionFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "convention"


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.select_related(
    ).prefetch_related(
        'awards',
        'hosts',
        'memberships',
        'performers',
    )
    serializer_class = EntitySerializer
    filter_class = EntityFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "entity"


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.select_related(
        'convention',
        'entity',
    ).prefetch_related(
    )
    serializer_class = HostSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "host"


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.select_related(
        'entity',
        'person',
    ).prefetch_related(
        'officers',
    )
    serializer_class = MembershipSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "membership"


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.select_related(
    ).prefetch_related(
        'officers',
    )
    serializer_class = OfficeSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "office"


class OfficerViewSet(viewsets.ModelViewSet):
    queryset = Officer.objects.select_related(
        'office',
        'membership',
    ).prefetch_related(
    )
    serializer_class = OfficerSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "officer"


class PerformanceViewSet(
    get_viewset_transition_action_mixin(Performance),
    viewsets.ModelViewSet,
):
    queryset = Performance.objects.select_related(
        'round',
        'performer',
        'slot',
        'session',
    ).prefetch_related(
    )
    serializer_class = PerformanceSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "performance"


class PerformancePrivateViewSet(viewsets.ModelViewSet):
    queryset = PerformancePrivate.objects.select_related(
    ).prefetch_related(
    )
    serializer_class = PerformancePrivateSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        PerformancePrivateFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "performanceprivate"


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.select_related(
        'session',
        'entity',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'director',
        'codirector',
    ).prefetch_related(
        'contestants',
        'performances',
        'submissions',
    )
    serializer_class = PerformerSerializer
    filter_class = PerformerFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "performer"


class PerformerScoreViewSet(viewsets.ModelViewSet):
    queryset = PerformerScore.objects.select_related(
    ).prefetch_related(
    )
    serializer_class = PerformerScoreSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        PerformerScoreFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "performerscore"


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'user',
    ).prefetch_related(
        'assignments',
        'memberships',
        'performers_tenor',
        'performers_lead',
        'performers_baritone',
        'performers_bass',
        'performers_director',
        'performers_codirector',
        'scores',
    )
    serializer_class = PersonSerializer
    filter_class = PersonFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "person"

    @detail_route(methods=['POST'], permission_classes=[AllowAny])
    @parser_classes((FormParser, MultiPartParser,))
    def picture(self, request, *args, **kwargs):
        if 'upload' in request.data:
            person = self.get_object()
            person.picture.delete()

            upload = request.data['upload']

            person.picture.save(upload.name, upload)

            return Response(status=status.HTTP_201_CREATED, headers={'Location': person.picture.url})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RoundViewSet(
    get_viewset_transition_action_mixin(Round),
    viewsets.ModelViewSet
):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'performances',
        'current_session',
        'slots',
    )
    serializer_class = RoundSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "round"


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'person',
    ).prefetch_related(
    )
    serializer_class = ScoreSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        ScoreFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "score"


class SessionViewSet(
    get_viewset_transition_action_mixin(Session),
    viewsets.ModelViewSet
):
    queryset = Session.objects.select_related(
        'convention',
    ).prefetch_related(
        'contests',
        'performers',
        'rounds',
    )
    serializer_class = SessionSerializer
    filter_class = SessionFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "session"


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'performance',
        'submission',
    ).prefetch_related(
        'scores',
    )
    serializer_class = SongSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "song"


class SongScoreViewSet(viewsets.ModelViewSet):
    queryset = SongScore.objects.select_related(
    ).prefetch_related(
    )
    serializer_class = SongScoreSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        SongScoreFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "songscore"


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.select_related(
        'round',
        'performance',
    ).prefetch_related(
    )
    serializer_class = SlotSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "slot"


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related(
        'performer',
        'catalog',
    ).prefetch_related(
        'songs',
    )
    serializer_class = SubmissionSerializer
    filter_class = SubmissionFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "submission"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.select_related(
    ).prefetch_related(
        'conventions',
    )
    serializer_class = VenueSerializer
    filter_class = VenueFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "venue"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related(
        'person',
    ).prefetch_related(
    )
    serializer_class = UserSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "user"

    @list_route(methods=['get'], permission_classes=[AllowAny])
    def me(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


# CSV View
class OfficeRendererCSV(CSVRenderer):
    header = [
        'id',
        'name',
        'nomen',
        'status',
        'kind',
        'short_name',
        'long_name',
    ]


class OfficeViewCSV(viewsets.ReadOnlyModelViewSet):
    queryset = Office.objects.select_related(
    ).prefetch_related(
    )
    serializer_class = OfficeCSVSerializer
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]
    pagination_class = None
    renderer_classes = [
        OfficeRendererCSV,
    ]
