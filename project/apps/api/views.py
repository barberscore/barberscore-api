import logging

from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import (
    viewsets,
    permissions,
    status,
)

from .filters import (
    # CoalesceFilterBackend,
    ChartFilter,
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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.select_related(
        'person',
    )
    serializer_class = CertificationSerializer
    resource_name = "certification"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    filter_class = ChartFilter
    resource_name = "chart"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
        'contest',
    ).order_by(
        'contest',
        '-total_points',
    )
    serializer_class = ContestantSerializer
    resource_name = "contestant"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class ConventionViewSet(viewsets.ModelViewSet):
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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'session',
        'person',
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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related(
        'chapter',
        'person',
    )
    serializer_class = MemberSerializer
    resource_name = "member"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.order_by(
        'tree_id',
    )
    serializer_class = OrganizationSerializer
    resource_name = "organization"


class PerformanceViewSet(viewsets.ModelViewSet):
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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


    @detail_route(methods=['put'])
    def move_top(self, request, pk=None):
        performance = self.get_object()
        response = performance.move_top()
        if response:
            return Response(response)
        else:
            return Response(
                {'error': 'did not move'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @detail_route(methods=['put'])
    def move_bottom(self, request, pk=None):
        performance = self.get_object()
        response = performance.move_bottom()
        if response:
            return Response(response)
        else:
            return Response(
                {'error': 'did not move'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @detail_route(methods=['put'])
    def scratch(self, request, pk=None):
        performance = self.get_object()
        response = performance.scratch()
        if response:
            return Response(response)
        else:
            return Response(
                {'error': 'did not scratch'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @detail_route(methods=['put'])
    def dixon(self, request, pk=None):
        performance = self.get_object()
        response = performance.dixon()
        if response:
            return Response(response)
        else:
            return Response(
                {'error': 'did not test'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.select_related(
        'session',
        'organization',
        'group',
    ).prefetch_related(
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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]

    @detail_route(methods=['put'])
    def add_performance(self, request, pk=None):
        performer = self.get_object()
        response = performer.add_performance()
        return Response(response)

    @detail_route(methods=['put'])
    def scratch(self, request, pk=None):
        performer = self.get_object()
        response = performer.scratch()
        return Response(response)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'organization',
        'chapter',
    ).prefetch_related(
        'roles',
        'panels',
        'conventions',
        'certifications',
    ).order_by(
        'name',
    )
    serializer_class = PersonSerializer
    filter_class = PersonFilter
    resource_name = "person"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related(
        'person',
        'group',
    ).order_by(
        '-name',
    )
    serializer_class = RoleSerializer
    resource_name = "role"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class RoundViewSet(viewsets.ModelViewSet):
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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]

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

    @detail_route(methods=['put'])
    def rank(self, request, pk=None):
        round = self.get_object()
        response = round.rank()
        if response:
            return Response(response)
        else:
            return Response(response)


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
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related(
        'convention',
        'administrator',
        'aca',
    ).prefetch_related(
        'performers',
        'rounds',
        'judges',
        'contests',
    )
    serializer_class = SessionSerializer
    resource_name = "session"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related(
        'performer',
        'chart',
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
        'chart',
    ).prefetch_related(
        'scores',
    ).order_by(
        'performance',
        'order',
    )
    serializer_class = SongSerializer
    resource_name = "song"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.prefetch_related(
        'conventions',
    ).order_by(
        'name',
    )
    serializer_class = VenueSerializer
    filter_class = VenueFilter
    resource_name = "venue"
    # filter_backends = [
    #     CoalesceFilterBackend,
    # ]
