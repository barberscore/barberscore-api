import logging

# from rest_framework.response import Response
# from rest_framework.decorators import detail_route

from drf_fsm_transitions.viewset_mixins import (
    get_viewset_transition_action_mixin,
)

from rest_framework import (
    viewsets,
    permissions,
)

from .filters import (
    CoalesceFilterBackend,
    CertificationFilter,
    ChartFilter,
    ContestantFilter,
    ConventionFilter,
    GroupFilter,
    PerformerFilter,
    PersonFilter,
    SubmissionFilter,
    VenueFilter,
)


from .models import (
    Award,
    Certification,
    Chapter,
    Chart,
    Contest,
    Contestant,
    Convention,
    Group,
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
    Submission,
    Song,
    Venue,
)

from .serializers import (
    AwardSerializer,
    CertificationSerializer,
    ChapterSerializer,
    ChartSerializer,
    ContestSerializer,
    ContestantSerializer,
    ConventionSerializer,
    GroupSerializer,
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
    SubmissionSerializer,
    SongSerializer,
    VenueSerializer,
)

log = logging.getLogger(__name__)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'organization',
    ).prefetch_related(
        'contests',
    ).order_by(
        'level',
        'organization',
        '-is_primary',
        'kind',
        'size',
        'scope',
    )
    serializer_class = AwardSerializer
    resource_name = "award"


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.select_related(
        'person',
    ).prefetch_related(
        'judges',
        'sessions_ca',
        'sessions_aca',
    )
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
    serializer_class = ChapterSerializer
    resource_name = "chapter"


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.prefetch_related(
        'submissions',
    )
    serializer_class = ChartSerializer
    filter_class = ChartFilter
    resource_name = "chart"


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
    serializer_class = ContestSerializer
    resource_name = "contest"


    # @detail_route(methods=['put'])
    # def build(self, request, pk=None):
    #     performance = self.get_object()
    #     response = performance.build()
    #     return Response(response)


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
        'contest',
    ).order_by(
        'contest',
        '-total_points',
    )
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
        'date',
        'organization__name',
    )
    serializer_class = ConventionSerializer
    filter_class = ConventionFilter
    resource_name = "convention"


    # @detail_route(methods=['put'])
    # def start(self, request, pk=None):
    #     convention = self.get_object()
    #     response = convention.start()
    #     return Response(response)

    # @detail_route(methods=['put'])
    # def finish(self, request, pk=None):
    #     convention = self.get_object()
    #     response = convention.finish()
    #     return Response(response)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'chapter',
        'organization',
    ).prefetch_related(
        'performers',
        'roles',
    ).order_by(
        'name',
    )
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    resource_name = "group"


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
    serializer_class = MemberSerializer
    resource_name = "member"


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.order_by(
        'kind',
        'level',
        'name',
    )
    serializer_class = OrganizationSerializer
    resource_name = "organization"


class PerformanceViewSet(
    get_viewset_transition_action_mixin(Performance),
    viewsets.ModelViewSet,
):
    queryset = Performance.objects.select_related(
        'round',
        'performer',
    ).prefetch_related(
        'songs',
    ).order_by(
        'round',
        'slot',
    )
    serializer_class = PerformanceSerializer
    resource_name = "performance"


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.select_related(
        'session',
        'representing',
        'group',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'director',
        'codirector',
    ).prefetch_related(
        'submissions',
        'performances',
        'contestants',
    ).order_by(
        'session',
        '-total_points',
        'group',
    )
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
        'organization',
        'chapter',
    ).prefetch_related(
        'roles',
        'conventions',
        'certifications',
    ).order_by(
        'name',
    )
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
    ).order_by(
        'session',
        'kind',
    )
    serializer_class = RoundSerializer
    resource_name = "round"


    # @detail_route(methods=['put'])
    # def draw(self, request, pk=None):
    #     round = self.get_object()
    #     response = round.draw()
    #     return Response(response)

    # @detail_route(methods=['put'])
    # def promote(self, request, pk=None):
    #     round = self.get_object()
    #     response = round.promote()
    #     return Response(response)

    # @detail_route(methods=['put'])
    # def resort(self, request, pk=None):
    #     round = self.get_object()
    #     response = round.resort()
    #     return Response(response)

    # @detail_route(methods=['put'])
    # def start(self, request, pk=None):
    #     round = self.get_object()
    #     response = round.start()
    #     return Response(response)

    # @detail_route(methods=['put'])
    # def finish(self, request, pk=None):
    #     round = self.get_object()
    #     response = round.finish()
    #     return Response(response)


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'judge',
    ).order_by(
        'song',
        'judge',
    )
    serializer_class = ScoreSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]
    resource_name = "score"


class SessionViewSet(
    get_viewset_transition_action_mixin(Session),
    viewsets.ModelViewSet
):
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
    resource_name = "session"


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related(
        'performer',
        'chart',
    ).prefetch_related(
        'songs',
    )
    serializer_class = SubmissionSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]
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
        'order',
    )
    serializer_class = SongSerializer
    resource_name = "song"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.prefetch_related(
        'conventions',
    ).order_by(
        'name',
    )
    serializer_class = VenueSerializer
    filter_class = VenueFilter
    resource_name = "venue"

