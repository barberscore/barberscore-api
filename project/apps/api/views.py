# Standard Libary
import logging

# Third-Party
from drf_fsm_transitions.viewset_mixins import \
    get_viewset_transition_action_mixin
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets

# Local
from .filters import (
    CatalogFilter,
    CoalesceFilterBackend,
    ContestantFilter,
    ConventionFilter,
    GroupFilter,
    JudgeFilter,
    PerformerFilter,
    PerformerScoreFilterBackend,
    PersonFilter,
    RoundFilterBackend,
    SessionFilterBackend,
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
)

from .serializers import (
    AssignmentSerializer,
    AwardSerializer,
    CatalogSerializer,
    ChapterSerializer,
    ContestantSerializer,
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
    queryset = Contest.objects.select_related(
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


class PerformanceScoreViewSet(
    get_viewset_transition_action_mixin(PerformanceScore),
    viewsets.ModelViewSet,
):
    queryset = PerformanceScore.objects.select_related(
        'performance',
    ).order_by(
        'name',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = PerformanceScoreSerializer
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
        'district',
        'division',
    ).prefetch_related(
        'submissions',
        'performances',
        'contestants',
    ).order_by(
        'session',
        '-total_points',
        'group',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = PerformerSerializer
    filter_class = PerformerFilter
    resource_name = "performer"


class PerformerScoreViewSet(viewsets.ModelViewSet):
    queryset = PerformerScore.objects.select_related(
        'performer',
    ).order_by(
        'name',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = PerformerScoreSerializer
    # filter_backends = (
    #     CoalesceFilterBackend,
    #     PerformerScoreFilterBackend,
    # )
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


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related(
        'person',
        'group',
    ).order_by(
        '-name',
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
    # filter_backends = (
    #     CoalesceFilterBackend,
    #     RoundFilterBackend,
    # )
    resource_name = "round"


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'assignment',
    ).order_by(
        'song',
        'assignment',
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
    # filter_backends = (
    #     CoalesceFilterBackend,
    # )
    serializer_class = SessionSerializer
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
        'name',
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
