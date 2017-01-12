# Standard Libary
import logging

# Third-Party
from django_filters.rest_framework import DjangoFilterBackend
from drf_fsm_transitions.viewset_mixins import (
    get_viewset_transition_action_mixin,
)
from rest_framework import (
    viewsets,
    status,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.decorators import (
    detail_route,
    list_route,
    parser_classes,
)

from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)

# Local
from .backends import (
    CoalesceFilterBackend,
    ConventionFilterBackend,
    # OrganizationFilterBackend,
    PerformanceScoreFilterBackend,
    PerformerScoreFilterBackend,
    ScoreFilterBackend,
    SessionFilterBackend,
    UserFilterBackend,
)

from .filters import (
    CatalogFilter,
    ContestantFilter,
    ConventionFilter,
    GroupFilter,
    JudgeFilter,
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
    Chapter,
    Contest,
    ContestScore,
    Contestant,
    ContestantScore,
    Convention,
    Group,
    Host,
    Judge,
    Member,
    Organization,
    Performance,
    PerformanceScore,
    Performer,
    PerformerScore,
    Person,
    Role,
    Round,
    Score,
    Session,
    Slot,
    Song,
    SongScore,
    Submission,
    Venue,
    User,
)

from .paginators import (
    PageNumberPagination,
    PersonPaginator,
)

from .serializers import (
    AssignmentSerializer,
    AwardSerializer,
    CatalogSerializer,
    ChapterSerializer,
    ContestantSerializer,
    ContestantScoreSerializer,
    ContestSerializer,
    ContestScoreSerializer,
    ConventionSerializer,
    GroupSerializer,
    HostSerializer,
    JudgeSerializer,
    MemberSerializer,
    OrganizationSerializer,
    PerformanceSerializer,
    PerformanceScoreSerializer,
    PerformerSerializer,
    PerformerScoreSerializer,
    PersonSerializer,
    RoleSerializer,
    RoundSerializer,
    ScoreSerializer,
    SessionSerializer,
    SlotSerializer,
    SongSerializer,
    SongScoreSerializer,
    SubmissionSerializer,
    VenueSerializer,
    UserSerializer,
)

log = logging.getLogger(__name__)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'organization',
    ).prefetch_related(
        'contests',
    ).order_by(
        'organization',
        '-is_primary',
        'kind',
        'size',
        'scope',
    )
    serializer_class = AwardSerializer
    resource_name = "award"
    pagination_class = PageNumberPagination
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.prefetch_related(
        'submissions',
    )
    serializer_class = CatalogSerializer
    filter_class = CatalogFilter
    resource_name = "catalog"
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'person',
    ).prefetch_related(
        'assignments',
    )
    serializer_class = JudgeSerializer
    filter_class = JudgeFilter
    resource_name = "judge"
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.select_related(
        'organization',
    ).prefetch_related(
        'groups',
        'members',
    ).order_by(
        'name',
    )
    serializer_class = ChapterSerializer
    resource_name = "chapter"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        'award',
        'contestscore',
    ).prefetch_related(
        'contestants',
    ).order_by(
        '-session__convention__year',
        'award',
        'session',
    )
    serializer_class = ContestSerializer
    resource_name = "contest"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class ContestScoreViewSet(viewsets.ModelViewSet):
    queryset = ContestScore.objects.select_related(
        'champion',
    )
    serializer_class = ContestScoreSerializer
    resource_name = "contestscore"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
        'contest',
    ).order_by(
        'contest',
    )
    serializer_class = ContestantSerializer
    filter_class = ContestantFilter
    resource_name = "contestant"
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class ContestantScoreViewSet(viewsets.ModelViewSet):
    queryset = ContestantScore.objects.order_by(
        'name',
    )
    serializer_class = ContestantScoreSerializer
    resource_name = "contestantscore"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class ConventionViewSet(
    get_viewset_transition_action_mixin(Convention),
    viewsets.ModelViewSet
):
    queryset = Convention.objects.select_related(
        'organization',
        'venue',
        'drcj',
    ).prefetch_related(
        'sessions',
    ).order_by(
        'start_date',
        'organization__name',
    )
    serializer_class = ConventionSerializer
    filter_class = ConventionFilter
    filter_backends = [
        ConventionFilterBackend,
    ]
    resource_name = "convention"
    pagination_class = None


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'chapter',
        'district',
        'division',
    ).prefetch_related(
        'performers',
        'roles',
    ).order_by(
        'name',
    )
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    resource_name = "group"
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.select_related(
        'convention',
        'organization',
    )
    serializer_class = HostSerializer
    resource_name = "host"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        'session',
        'judge',
    ).prefetch_related(
        'scores',
    ).order_by(
        'session',
        'category',
        'kind',
        'slot',
    )
    serializer_class = AssignmentSerializer
    resource_name = "assignment"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related(
        'chapter',
        'person',
    )
    serializer_class = MemberSerializer
    resource_name = "member"
    pagination_class = None


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.prefetch_related(
        'awards',
    ).order_by(
        'kind',
        'level',
        'name',
    )
    serializer_class = OrganizationSerializer
    resource_name = "organization"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class PerformanceViewSet(
    get_viewset_transition_action_mixin(Performance),
    viewsets.ModelViewSet,
):
    queryset = Performance.objects.select_related(
        'round',
        'performer',
        'slot',
        'performancescore',
    ).prefetch_related(
        'songs',
    ).order_by(
        'round',
        'num',
    )
    serializer_class = PerformanceSerializer
    resource_name = "performance"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class PerformanceScoreViewSet(viewsets.ModelViewSet):
    queryset = PerformanceScore.objects.order_by(
        'nomen',
    )
    serializer_class = PerformanceScoreSerializer
    resource_name = "performancescore"
    pagination_class = None
    filter_class = None
    filter_backends = [
        PerformanceScoreFilterBackend,
    ]


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.select_related(
        'session',
        'group',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'director',
        'codirector',
        'representing',
        'performerscore',
    ).prefetch_related(
        'submissions',
        'performances',
        'contestants',
    ).order_by(
        'session',
        'group',
    )
    serializer_class = PerformerSerializer
    filter_class = PerformerFilter
    resource_name = "performer"
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class PerformerScoreViewSet(viewsets.ModelViewSet):
    queryset = PerformerScore.objects.order_by(
        'nomen',
    )
    serializer_class = PerformerScoreSerializer
    filter_backends = [
        # CoalesceFilterBackend,
        PerformerScoreFilterBackend,
    ]
    resource_name = "performerscore"
    pagination_class = None
    filter_class = None


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'user',
    ).prefetch_related(
        'roles',
        'conventions',
        'judges',
    ).order_by(
        'name',
    )
    serializer_class = PersonSerializer
    filter_class = PersonFilter
    resource_name = "person"
    pagination_class = PersonPaginator
    filter_backends = [
        DjangoFilterBackend,
    ]

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


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related(
        'person',
        'group',
    ).order_by(
        '-nomen',
    )
    serializer_class = RoleSerializer
    resource_name = "role"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class RoundViewSet(
    get_viewset_transition_action_mixin(Round),
    viewsets.ModelViewSet
):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'performances',
        'slots',
    ).order_by(
        'session',
        'kind',
    )
    serializer_class = RoundSerializer
    filter_backends = [
        CoalesceFilterBackend,
    ]
    resource_name = "round"
    pagination_class = None
    filter_class = None


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'assignment',
        'song__performance__performer__session',
        'song__performance__round',
        'assignment__judge__person',
    ).prefetch_related(
        'song__performance__performer__group__roles',
        'song__performance__round__session__assignments',
    ).order_by(
        'song',
        'assignment',
    )
    filter_backends = [
        ScoreFilterBackend,
    ]
    serializer_class = ScoreSerializer
    resource_name = "score"
    pagination_class = None
    filter_class = None


class SessionViewSet(
    get_viewset_transition_action_mixin(Session),
    viewsets.ModelViewSet
):
    queryset = Session.objects.select_related(
        'convention',
    ).prefetch_related(
        'performers',
        'rounds',
        'assignments',
        'contests',
    ).order_by(
        '-start_date',
    )
    serializer_class = SessionSerializer
    filter_backends = [
        SessionFilterBackend,
    ]
    filter_class = SessionFilter
    resource_name = "session"
    pagination_class = None


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related(
        'performer',
    ).prefetch_related(
        'songs',
    )
    serializer_class = SubmissionSerializer
    filter_class = SubmissionFilter
    resource_name = "submission"
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'performance',
        'submission',
        'songscore',
    ).prefetch_related(
        'scores',
    ).order_by(
        'performance',
        'num',
    )
    serializer_class = SongSerializer
    resource_name = "song"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class SongScoreViewSet(viewsets.ModelViewSet):
    queryset = SongScore.objects.order_by(
        'nomen',
    )
    serializer_class = SongScoreSerializer
    resource_name = "songscore"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.select_related(
        'round',
    ).prefetch_related(
        'performance',
    ).order_by(
        'round',
        'num',
    )
    serializer_class = SlotSerializer
    resource_name = "slot"
    pagination_class = None
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.prefetch_related(
        'conventions',
    ).order_by(
        'name',
    )
    serializer_class = VenueSerializer
    filter_class = VenueFilter
    resource_name = "venue"
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (UserFilterBackend,)
    pagination_class = None
    filter_class = None

    @list_route(methods=['get'], permission_classes=[AllowAny])
    def me(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
