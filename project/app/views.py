# Standard Libary
import logging

# Third-Party
from drf_fsm_transitions.viewset_mixins import (
    get_viewset_transition_action_mixin,
)
from dry_rest_permissions.generics import DRYPermissions
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
from .filters import (
    CatalogFilter,
    CoalesceFilterBackend,
    ContestantFilter,
    ConventionFilter,
    ConventionFilterBackend,
    OrganizationFilterBackend,
    GroupFilter,
    JudgeFilter,
    PerformerFilter,
    PerformanceScoreFilterBackend,
    PerformerScoreFilterBackend,
    PersonFilter,
    ScoreFilterBackend,
    SessionFilter,
    SessionFilterBackend,
    SubmissionFilter,
    VenueFilter,
    UserFilterBackend,
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
    permission_classes = (DRYPermissions,)
    serializer_class = AwardSerializer
    resource_name = "award"


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.prefetch_related(
        'submissions',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = CatalogSerializer
    filter_class = CatalogFilter
    resource_name = "catalog"


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'person',
    ).prefetch_related(
        'assignments',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = JudgeSerializer
    filter_class = JudgeFilter
    resource_name = "judge"
    pagination_class = None


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.select_related(
        'organization',
    ).prefetch_related(
        'groups',
        'members',
    ).order_by(
        'name',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = ChapterSerializer
    resource_name = "chapter"


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
    permission_classes = (DRYPermissions,)
    serializer_class = ContestSerializer
    resource_name = "contest"


class ContestScoreViewSet(viewsets.ModelViewSet):
    queryset = ContestScore.objects.select_related(
        'champion',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = ContestScoreSerializer
    resource_name = "contestscore"


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
        'contest',
    ).order_by(
        'contest',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = ContestantSerializer
    filter_class = ContestantFilter
    resource_name = "contestant"


class ContestantScoreViewSet(viewsets.ModelViewSet):
    queryset = ContestantScore.objects.order_by(
        'name',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = ContestantScoreSerializer
    resource_name = "contestantscore"


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
    permission_classes = (DRYPermissions,)
    serializer_class = ConventionSerializer
    filter_class = ConventionFilter
    filter_backends = (
        ConventionFilterBackend,
    )
    resource_name = "convention"


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
    permission_classes = (DRYPermissions,)
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    resource_name = "group"


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.select_related(
        'convention',
        'organization',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = HostSerializer
    resource_name = "host"


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
    permission_classes = (DRYPermissions,)
    serializer_class = AssignmentSerializer
    resource_name = "assignment"


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related(
        'chapter',
        'person',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = MemberSerializer
    resource_name = "member"


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.prefetch_related(
        'awards',
    ).order_by(
        'kind',
        'level',
        'name',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = OrganizationSerializer
    filter_backends = [
        OrganizationFilterBackend,
    ]
    resource_name = "organization"


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
    permission_classes = (DRYPermissions,)
    serializer_class = PerformanceSerializer
    resource_name = "performance"


class PerformanceScoreViewSet(viewsets.ModelViewSet):
    queryset = PerformanceScore.objects.order_by(
        'nomen',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = PerformanceScoreSerializer
    filter_backends = (
        PerformanceScoreFilterBackend,
    )
    resource_name = "performancescore"


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
    permission_classes = (DRYPermissions,)
    serializer_class = PerformerSerializer
    filter_class = PerformerFilter
    resource_name = "performer"


class PerformerScoreViewSet(viewsets.ModelViewSet):
    queryset = PerformerScore.objects.order_by(
        'nomen',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = PerformerScoreSerializer
    filter_backends = (
        # CoalesceFilterBackend,
        PerformerScoreFilterBackend,
    )
    resource_name = "performerscore"


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
    permission_classes = (DRYPermissions,)
    serializer_class = PersonSerializer
    filter_class = PersonFilter
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


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related(
        'person',
        'group',
    ).order_by(
        '-nomen',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = RoleSerializer
    resource_name = "role"


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
    permission_classes = (DRYPermissions,)
    serializer_class = RoundSerializer
    filter_backends = (
        CoalesceFilterBackend,
    )
    resource_name = "round"


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
    filter_backends = (
        # CoalesceFilterBackend,
        ScoreFilterBackend,
    )
    permission_classes = (DRYPermissions,)
    serializer_class = ScoreSerializer
    resource_name = "score"


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
    permission_classes = (DRYPermissions,)
    serializer_class = SessionSerializer
    filter_backends = (
        SessionFilterBackend,
    )
    filter_class = SessionFilter
    resource_name = "session"


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related(
        'performer',
    ).prefetch_related(
        'songs',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = SubmissionSerializer
    filter_class = SubmissionFilter
    resource_name = "submission"


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
    permission_classes = (DRYPermissions,)
    serializer_class = SongSerializer
    resource_name = "song"


class SongScoreViewSet(viewsets.ModelViewSet):
    queryset = SongScore.objects.order_by(
        'nomen',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = SongScoreSerializer
    resource_name = "songscore"


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.select_related(
        'round',
    ).prefetch_related(
        'performance',
    ).order_by(
        'round',
        'num',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = SlotSerializer
    resource_name = "slot"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.prefetch_related(
        'conventions',
    ).order_by(
        'name',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = VenueSerializer
    filter_class = VenueFilter
    resource_name = "venue"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (DRYPermissions,)
    filter_backends = (UserFilterBackend,)

    @list_route(methods=['get'], permission_classes=[AllowAny])
    def me(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
