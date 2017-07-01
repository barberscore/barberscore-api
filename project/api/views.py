# Standard Libary
import logging

# Third-Party
from django_filters.rest_framework import DjangoFilterBackend
from django_fsm_log.models import StateLog
from drf_fsm_transitions.viewset_mixins import (
    get_viewset_transition_action_mixin,
)
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
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

# Django
from django.db.models import Q

# Local
from .backends import (
    CoalesceFilterBackend,
    ScoreFilterBackend,
)
from .filters import (
    AwardFilter,
    ChartFilter,
    ContestantFilter,
    ConventionFilter,
    EntityFilter,
    EntryFilter,
    MemberFilter,
    OfficeFilter,
    OfficerFilter,
    PanelistFilter,
    ParticipantFilter,
    PersonFilter,
    RoundFilter,
    ScoreFilter,
    SessionFilter,
    VenueFilter,
)
from .models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Entity,
    Entry,
    Member,
    Office,
    Officer,
    Panelist,
    Participant,
    Person,
    Repertory,
    Round,
    Score,
    Session,
    Slot,
    Song,
    User,
    Venue,
)
from .paginators import PageNumberPagination
from .serializers import (
    AppearanceSerializer,
    AssignmentSerializer,
    AwardSerializer,
    ChartSerializer,
    ContestantSerializer,
    ContestSerializer,
    ConventionSerializer,
    EntitySerializer,
    EntrySerializer,
    MemberSerializer,
    OfficeCSVSerializer,
    OfficerSerializer,
    OfficeSerializer,
    PanelistSerializer,
    ParticipantSerializer,
    PersonSerializer,
    RepertorySerializer,
    RoundSerializer,
    ScoreSerializer,
    SessionSerializer,
    SlotSerializer,
    SongSerializer,
    StateLogSerializer,
    UserSerializer,
    VenueSerializer,
)

log = logging.getLogger(__name__)


class AppearanceViewSet(
    get_viewset_transition_action_mixin(Appearance),
    viewsets.ModelViewSet,
):
    queryset = Appearance.objects.select_related(
        'round',
        'entry',
        'slot',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = AppearanceSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "appearance"


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        'convention',
        'person',
    ).prefetch_related(
    ).order_by('nomen')
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

    def get_queryset(self):
        queryset = Award.objects.select_related(
            'entity',
        ).prefetch_related(
            'contests',
        ).order_by(
            'nomen',
        )
        drcj = self.request.query_params.get('drcj', None)
        if drcj:
            try:
                user = User.objects.get(id=drcj)
            except User.DoesNotExist:
                queryset = Award.objects.none()
                return queryset
            queryset = Award.objects.filter(
                Q(entity__officers__person__user=user) |
                Q(entity__parent__officers__person__user=user)
            ).select_related(
                'entity',
            ).prefetch_related(
                'contests',
            ).order_by(
                'nomen',
            )
        convention = self.request.query_params.get('convention', None)
        if convention:
            try:
                convention = Convention.objects.get(id=convention)
            except Convention.DoesNotExist:
                queryset = Award.objects.none()
                return queryset
            queryset = Award.objects.filter(
                Q(entity=convention.entity.parent, season=convention.season, is_qualifier=True) |
                Q(entity=convention.entity, season=convention.season) |
                Q(entity__in=convention.entity.children.all(), season=convention.season)
            ).select_related(
                'entity',
            ).prefetch_related(
                'contests',
            ).order_by(
                'nomen',
            )
        return queryset


class ChartViewSet(
    get_viewset_transition_action_mixin(Chart),
    viewsets.ModelViewSet,
):
    queryset = Chart.objects.select_related(
    ).prefetch_related(
        'repertories',
        'songs',
    ).order_by('status', 'nomen')
    serializer_class = ChartSerializer
    filter_class = ChartFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "chart"

    @detail_route(methods=['POST'], permission_classes=[AllowAny])
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        print(request.data)
        if 'file' in request.data:
            obj = self.get_object()

            upload = request.data['file']
            obj.image.save(
                'foo.pdf',
                upload,
            )
            return Response(
                status=status.HTTP_201_CREATED,
                data={'image': obj.image.url},
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        'award',
    ).prefetch_related(
    ).order_by('nomen')
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


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'entry',
        'contest',
    ).prefetch_related(
    ).order_by('nomen')
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


class ConventionViewSet(
    get_viewset_transition_action_mixin(Convention),
    viewsets.ModelViewSet
):
    queryset = Convention.objects.select_related(
        'venue',
        'entity',
    ).prefetch_related(
        'assignments',
    ).order_by('nomen')
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


class EntityViewSet(
    get_viewset_transition_action_mixin(Entry),
    viewsets.ModelViewSet
):
    queryset = Entity.objects.select_related(
        'parent',
    ).prefetch_related(
        'children',
        'awards',
        'conventions',
        'entries',
        'members',
        'officers',
        'repertories',
    ).order_by(
        'nomen',
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

    @detail_route(methods=['POST'], permission_classes=[AllowAny])
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        print(request.data)
        if 'file' in request.data:
            obj = self.get_object()

            upload = request.data['file']
            obj.image.save(
                'foo.jpg',
                upload,
            )
            return Response(
                status=status.HTTP_201_CREATED,
                data={'image': obj.image.url},
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EntryViewSet(
    get_viewset_transition_action_mixin(Entry),
    viewsets.ModelViewSet
):
    queryset = Entry.objects.select_related(
        'session',
        'entity',
        'representing',
    ).prefetch_related(
        'participants',
        'contestants',
        'appearances',
    ).order_by('nomen')
    serializer_class = EntrySerializer
    filter_class = EntryFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "entry"


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related(
        'entity',
        'person',
    ).prefetch_related(
        'participants',
    ).order_by('nomen')
    serializer_class = MemberSerializer
    filter_class = MemberFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "member"


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.select_related(
    ).prefetch_related(
        'officers',
    ).order_by('nomen')
    serializer_class = OfficeSerializer
    filter_class = OfficeFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "office"


class OfficerViewSet(
    get_viewset_transition_action_mixin(Officer),
    viewsets.ModelViewSet
):
    queryset = Officer.objects.select_related(
        'office',
        'person',
        'entity',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = OfficerSerializer
    filter_class = OfficerFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "officer"


class PanelistViewSet(viewsets.ModelViewSet):
    queryset = Panelist.objects.select_related(
        'round',
        'person',
    ).prefetch_related(
        'scores',
    ).order_by('nomen')
    serializer_class = PanelistSerializer
    filter_class = PanelistFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "panelist"


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.select_related(
        'entry',
        'member'
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = ParticipantSerializer
    filter_class = ParticipantFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "participant"


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'user',
        'representing',
    ).prefetch_related(
        'assignments',
        'members',
        'officers',
        'panelists',
    ).order_by('nomen')
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
    def image(self, request, *args, **kwargs):
        print(request.data)
        if 'file' in request.data:
            person = self.get_object()

            upload = request.data['file']
            person.image.save(
                'foo.jpg',
                upload,
            )
            return Response(
                status=status.HTTP_201_CREATED,
                data={'image': person.image.url},
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RepertoryViewSet(
    get_viewset_transition_action_mixin(Repertory),
    viewsets.ModelViewSet
):
    queryset = Repertory.objects.select_related(
        'entity',
        'chart',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = RepertorySerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "repertory"


class RoundViewSet(
    get_viewset_transition_action_mixin(Round),
    viewsets.ModelViewSet
):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'appearances',
        'slots',
        'panelists',
    ).order_by('nomen')
    serializer_class = RoundSerializer
    filter_class = RoundFilter
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
        'panelist',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = ScoreSerializer
    filter_class = ScoreFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
        # ScoreFilterBackend,
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
        'entries',
        'rounds',
    ).order_by('nomen')
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


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.select_related(
        'round',
        'appearance',
    ).prefetch_related(
    ).order_by('nomen')
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


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'appearance',
        'chart',
    ).prefetch_related(
        'scores',
    ).order_by('nomen')
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


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.select_related(
    ).prefetch_related(
        'conventions',
    ).order_by('nomen')
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
    ).order_by('id')
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

    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class StateLogViewSet(viewsets.ModelViewSet):
    queryset = StateLog.objects.all()
    serializer_class = StateLogSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    pagination_class = PageNumberPagination
    # permission_classes = [
    #     DRYPermissions,
    # ]
    resource_name = "statelog"

    # @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    # def me(self, request):
    #     serializer = self.get_serializer(request.user)
    #     return Response(serializer.data)



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
    ).order_by('nomen')
    serializer_class = OfficeCSVSerializer
    filter_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]
    pagination_class = None
    renderer_classes = [
        OfficeRendererCSV,
    ]
