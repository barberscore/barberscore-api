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
    CertificationFilter,
    CoalesceFilterBackend,
    ContestantFilter,
    ConventionFilter,
    GroupFilter,
    PerformerFilter,
    PersonFilter,
    RoundFilterBackend,
    SessionFilterBackend,
    SubmissionFilter,
    VenueFilter,
)
from .models import (
    Award,
    Catalog,
    Certification,
    Chapter,
    Contest,
    Contestant,
    Convention,
    Group,
    Host,
    Judge,
    Member,
    Organization,
    Performance,
    Performer,
    Person,
    Role,
    Round,
    Score,
    Session,
    Slot,
    Song,
    Submission,
    Venue,
)
from .serializers import (
    AwardSerializer,
    CatalogSerializer,
    CertificationSerializer,
    ChapterSerializer,
    ContestantSerializer,
    ContestSerializer,
    ConventionSerializer,
    GroupSerializer,
    HostSerializer,
    JudgeSerializer,
    MemberSerializer,
    OrganizationSerializer,
    PerformanceSerializer,
    PerformerSerializer,
    PersonSerializer,
    RoleSerializer,
    RoundSerializer,
    ScoreSerializer,
    SessionSerializer,
    SlotSerializer,
    SongSerializer,
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


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.select_related(
        'person',
    ).prefetch_related(
        'judges',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = CertificationSerializer
    filter_class = CertificationFilter
    resource_name = "certification"


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


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'session',
        'certification',
    ).prefetch_related(
        'scores',
    ).order_by(
        'session',
        'category',
        'kind',
        'slot',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = JudgeSerializer
    resource_name = "judge"
    filter_backends = [
        CoalesceFilterBackend,
    ]


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
    ).prefetch_related(
        'songs',
    ).order_by(
        'round',
        'num',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = PerformanceSerializer
    resource_name = "performance"


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
        'chapter',
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

    # @detail_route(methods=['put'])
    # def add_performance(self, request, pk=None):
    #     performer = self.get_object()
    #     response = performer.add_performance()
    #     return Response(response)

    # @detail_route(methods=['put'])
    # def scratch(self, request, pk=None):
    #     performer = self.get_object()
    #     response = performer.scratch()
    #     return Response(response)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'user',
    ).prefetch_related(
        'roles',
        'conventions',
        'certifications',
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
    filter_backends = (RoundFilterBackend,)
    resource_name = "round"


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'judge',
    ).order_by(
        'song',
        'judge',
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
        'judges',
        'contests',
    )
    permission_classes = (DRYPermissions,)
    filter_backends = (SessionFilterBackend,)
    serializer_class = SessionSerializer
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
    ).prefetch_related(
        'scores',
    ).order_by(
        'performance',
        'num',
    )
    permission_classes = (DRYPermissions,)
    serializer_class = SongSerializer
    resource_name = "song"


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
