import logging

from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import (
    viewsets,
    permissions,
    status,
)

from .filters import (
    ChartFilter,
    ConventionFilter,
    GroupFilter,
    PersonFilter,
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
    )
    serializer_class = AwardSerializer
    resource_name = "award"


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.select_related(
        'person',
    )
    serializer_class = CertificationSerializer
    resource_name = "certification"


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.select_related(
        'organization',
    ).prefetch_related(
        'groups',
        'members',
    )
    serializer_class = ChapterSerializer
    resource_name = "chapter"


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    filter_class = ChartFilter
    resource_name = "chart"


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        'award',
    ).prefetch_related(
        'contestants',
    )
    serializer_class = ContestSerializer
    resource_name = "contest"


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'performer',
        'contest',
    )
    serializer_class = ContestantSerializer
    resource_name = "contestant"


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'organization',
        'venue',
        'drcj',
    ).prefetch_related(
        'sessions',
    )
    serializer_class = ConventionSerializer
    filter_class = ConventionFilter
    resource_name = "convention"


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'chapter',
        'organization',
    ).prefetch_related(
        'performers',
        'roles',
    )
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    resource_name = "group"


class JudgeViewSet(viewsets.ModelViewSet):
    queryset = Judge.objects.select_related(
        'session',
        'person',
    ).prefetch_related(
        'scores',
    )
    serializer_class = JudgeSerializer
    resource_name = "judge"


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related(
        'chapter',
        'person',
    )
    serializer_class = MemberSerializer
    resource_name = "member"


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.exclude(level=2)
    serializer_class = OrganizationSerializer
    resource_name = "organization"


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'round',
        'performer',
    ).prefetch_related(
        'songs',
    )
    serializer_class = PerformanceSerializer
    resource_name = "performance"


class PerformerViewSet(viewsets.ModelViewSet):
    queryset = Performer.objects.select_related(
        'session',
        'organization',
        'group',
    ).prefetch_related(
        'performances',
        'contestants',
    )
    serializer_class = PerformerSerializer
    resource_name = "performer"


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'organization',
        'chapter',
    ).prefetch_related(
        'roles',
        'panels',
        'conventions',
    )
    serializer_class = PersonSerializer
    filter_class = PersonFilter
    resource_name = "person"


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.select_related(
        'person',
        'group',
    )
    serializer_class = RoleSerializer
    resource_name = "role"


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'performances',
    )
    serializer_class = RoundSerializer
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


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.select_related(
        'performer',
        'chart',
    )
    serializer_class = SubmissionSerializer
    permission_classes = [
        permissions.DjangoModelPermissions,
    ]
    resource_name = "submission"


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'performance',
        'chart',
    ).prefetch_related(
        'scores',
    )
    serializer_class = SongSerializer
    resource_name = "song"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.prefetch_related(
        'conventions',
    )
    serializer_class = VenueSerializer
    filter_class = VenueFilter
    resource_name = "venue"
