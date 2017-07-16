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
    EntityFilterBackend,
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

from rest_framework.pagination import PageNumberPagination

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
        'songs',
        'songs__scores',
        'songs__chart',
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

    @detail_route(methods=['POST'], permission_classes=[AllowAny])
    @parser_classes((FormParser, MultiPartParser,))
    def print_var(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.print_var()
        # return Response(
        #     status=status.HTTP_200_OK,
        #     data={'var_pdf': obj.var_pdf.url},
        # )
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


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


class AwardViewSet(
    get_viewset_transition_action_mixin(Award),
    viewsets.ModelViewSet
):
    queryset = Award.objects.select_related(
        'entity',
        'parent',
    ).prefetch_related(
        'children',
        'contests',
    ).order_by('status', 'nomen')
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

    # def get_queryset(self):
    #     queryset = Award.objects.select_related(
    #         'entity',
    #     ).prefetch_related(
    #         'contests',
    #     ).order_by(
    #         'nomen',
    #     )
    #     drcj = self.request.query_params.get('drcj', None)
    #     if drcj:
    #         try:
    #             user = User.objects.get(id=drcj)
    #         except User.DoesNotExist:
    #             queryset = Award.objects.none()
    #             return queryset
    #         queryset = Award.objects.filter(
    #             Q(entity__officers__person__user=user) |
    #             Q(entity__parent__officers__person__user=user)
    #         ).select_related(
    #             'entity',
    #         ).prefetch_related(
    #             'contests',
    #         ).order_by(
    #             'nomen',
    #         )
    #     convention = self.request.query_params.get('convention', None)
    #     if convention:
    #         try:
    #             convention = Convention.objects.get(id=convention)
    #         except Convention.DoesNotExist:
    #             queryset = Award.objects.none()
    #             return queryset
    #         queryset = Award.objects.filter(
    #             Q(entity=convention.entity.parent, season=convention.season, is_qualifier=True) |
    #             Q(entity=convention.entity, season=convention.season) |
    #             Q(entity__in=convention.entity.children.all(), season=convention.season)
    #         ).select_related(
    #             'entity',
    #         ).prefetch_related(
    #             'contests',
    #         ).order_by(
    #             'nomen',
    #         )
    #     return queryset


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
        'contestants',
        'contestants__entry',
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
        'sessions',
        'sessions__rounds',
        'sessions__contests',
        'sessions__entries',
        'assignments',
        'assignments__person',
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
    get_viewset_transition_action_mixin(Entity),
    viewsets.ModelViewSet
):
    queryset = Entity.objects.select_related(
        'parent',
    ).prefetch_related(
        'children',
        'awards',
        'awards__contests',
        'awards__parent',
        'awards__children',
        'conventions',
        'conventions__sessions',
        'conventions__assignments',
        'conventions__venue',
        'entries',
        'entries__appearances',
        'entries__contestants',
        'entries__session',
        'entries__participants',
        'members__participants',
        'members__person',
        'officers',
        'officers__person',
        'officers__office',
        'repertories',
        'repertories__chart',
        'children__members',
        'children__entries',
        'children__officers',
        'children__repertories',
        'children__awards',
        'children__conventions',
        'children__children',
    ).order_by(
        'nomen',
    )
    serializer_class = EntitySerializer
    filter_class = EntityFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
        # EntityFilterBackend,
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
        'appearances',
        'appearances__songs',
        'appearances__round',
        'appearances__slot',
        'contestants',
        'contestants__contest',
        'participants',
        'participants__member',
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
        'participants__entry',
        'person__representing',
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
        'officers__entity',
        'officers__person',
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
        'scores__song',
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
        'officers__office',
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
        'appearances__songs',
        'appearances__entry',
        'appearances__slot',
        'slots',
        'slots__round',
        'slots__appearance',
        'panelists',
        'panelists__person',
        'panelists__scores',
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

    @detail_route(methods=['POST'], permission_classes=[AllowAny])
    @parser_classes((FormParser, MultiPartParser,))
    def print_ann(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.print_ann()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


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
        'contests__contestants',
        'contests__award',
        'entries',
        'entries__participants',
        'entries__contestants',
        'entries__appearances',
        'entries__entity',
        'entries__representing',
        'rounds__appearances',
        'rounds__slots',
        'rounds__panelists',
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
        'scores__panelist',
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
        'conventions__sessions',
        'conventions__assignments',
        'conventions__entity',
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
        'person__assignments',
        'person__members',
        'person__officers',
        'person__panelists',
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


# from django.shortcuts import render
# from django.db.models import Avg
# def variance(request):
#     appearance = Appearance.objects.get(id='a88b7462-0ede-4427-a35c-41bec4e1ab21')
#     song_one = appearance.songs.all().order_by('num').first()
#     song_two = appearance.songs.all().order_by('num').last()
#     scores_one = song_one.scores.all().order_by('panelist__num')
#     scores_two = song_two.scores.all().order_by('panelist__num')
#     scores_one_avg = scores_one.aggregate(a=Avg('points'))['a']
#     scores_two_avg = scores_two.aggregate(a=Avg('points'))['a']
#     return render(request, 'variance.html', {
#         'appearance': appearance,
#         'song_one': song_one,
#         'song_two': song_two,
#         'scores_one' : scores_one,
#         'scores_two' : scores_two,
#         'scores_one_avg' : scores_one_avg,
#         'scores_two_avg' : scores_two_avg,
#     })
#
#
# def ann(request):
#     self = Round.objects.get(id='b3b64b4a-f48f-440a-a6be-5727ef729e4e')
#     primary = self.session.contests.get(is_primary=True)
#     contests = self.session.contests.filter(is_primary=False)
#     winners = []
#     for contest in contests:
#         winner = contest.contestants.get(rank=1)
#         winners.append(winner)
#     medalists = []
#     for contestant in primary.contestants.order_by('-rank'):
#         medalists.append(contestant)
#     medalists = medalists[-5:]
#
#     return render(request, 'ann.html', {
#         'primary': primary,
#         'contests': contests,
#         'winners': winners,
#         'medalists': medalists,
#     })
