# Standard Libary
import logging

# Third-Party
from cloudinary.uploader import upload_resource
from django_filters.rest_framework import DjangoFilterBackend
from django_fsm_log.models import StateLog
from drf_fsm_transitions.viewset_mixins import \
    get_viewset_transition_action_mixin
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer
# Local
from .backends import CoalesceFilterBackend
# from .backends import GroupFilterBackend
from .backends import MemberFilterBackend
from .filters import AwardFilter
from .filters import ChartFilter
from .filters import CompetitorFilter
from .filters import ContestantFilter
from .filters import ConventionFilter
from .filters import EntryFilter
from .filters import GrantorFilter
from .filters import GroupFilter
from .filters import MemberFilter
from .filters import OfficeFilter
from .filters import OfficerFilter
from .filters import PanelistFilter
from .filters import PersonFilter
from .filters import RoundFilter
from .filters import ScoreFilter
from .filters import SessionFilter
from .filters import VenueFilter
from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Chart
from .models import Competitor
from .models import Contest
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grantor
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User
from .models import Venue
from .serializers import AppearanceSerializer
from .serializers import AssignmentSerializer
from .serializers import AwardSerializer
from .serializers import ChartSerializer
from .serializers import CompetitorSerializer
from .serializers import ContestantSerializer
from .serializers import ContestSerializer
from .serializers import ConventionSerializer
from .serializers import EntrySerializer
from .serializers import GrantorSerializer
from .serializers import GridSerializer
from .serializers import GroupSerializer
from .serializers import MemberSerializer
from .serializers import OfficeCSVSerializer
from .serializers import OfficerSerializer
from .serializers import OfficeSerializer
from .serializers import PanelistSerializer
from .serializers import PersonSerializer
from .serializers import RepertorySerializer
from .serializers import RoundSerializer
from .serializers import ScoreSerializer
from .serializers import SessionSerializer
from .serializers import SongSerializer
from .serializers import StateLogSerializer
from .serializers import UserSerializer
from .serializers import VenueSerializer

log = logging.getLogger(__name__)


class AppearanceViewSet(
    get_viewset_transition_action_mixin(Appearance),
    viewsets.ModelViewSet,
):
    queryset = Appearance.objects.select_related(
        'round',
        'competitor',
    ).prefetch_related(
        'songs',
    ).order_by('nomen')
    serializer_class = AppearanceSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "appearance"


class AssignmentViewSet(
        get_viewset_transition_action_mixin(Assignment),
        viewsets.ModelViewSet,
):
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
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "assignment"


class AwardViewSet(
    get_viewset_transition_action_mixin(Award),
    viewsets.ModelViewSet
):
    queryset = Award.objects.select_related(
        'group',
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
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "award"


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
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "chart"

    # @detail_route(methods=['POST'], permission_classes=[AllowAny])
    # @parser_classes((FormParser, MultiPartParser,))
    # def img(self, request, *args, **kwargs):
    #     if 'file' in request.data:
    #         obj = self.get_object()
    #         file = request.data['file']
    #         public_id = str(obj.id)
    #         folder = obj._meta.model_name
    #         obj.img = upload_resource(
    #             file,
    #             public_id=public_id,
    #             folder=folder,
    #             overwrite=True,
    #             invalidate=True,
    #             format='png',
    #         )
    #         obj.save()
    #         return Response(
    #             status=status.HTTP_201_CREATED,
    #             data={'image': obj.img.url},
    #         )
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class ContestViewSet(
    get_viewset_transition_action_mixin(Contest),
    viewsets.ModelViewSet,
):
    queryset = Contest.objects.select_related(
        'session',
        'award',
    ).prefetch_related(
        'contestants',
    ).order_by('nomen')
    serializer_class = ContestSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contest"


class ContestantViewSet(
    get_viewset_transition_action_mixin(Contestant),
    viewsets.ModelViewSet
):
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
        'group',
    ).prefetch_related(
        'sessions',
        'assignments',
        'grantors',
    ).order_by('nomen')
    serializer_class = ConventionSerializer
    filter_class = ConventionFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "convention"


class CompetitorViewSet(
    get_viewset_transition_action_mixin(Competitor),
    viewsets.ModelViewSet
):
    queryset = Competitor.objects.select_related(
        'session',
        'group',
        'entry',
    ).prefetch_related(
        'appearances',
    ).order_by('nomen')
    serializer_class = CompetitorSerializer
    filter_class = CompetitorFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "competitor"


class EntryViewSet(
    get_viewset_transition_action_mixin(Entry),
    viewsets.ModelViewSet
):
    queryset = Entry.objects.select_related(
        'session',
        'group',
    ).prefetch_related(
        'contestants',
    ).order_by('nomen')
    serializer_class = EntrySerializer
    filter_class = EntryFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "entry"


class GridViewSet(viewsets.ModelViewSet):
    queryset = Grid.objects.select_related(
        'round',
        'competitor',
        'appearance',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = GridSerializer
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "grid"


class GrantorViewSet(viewsets.ModelViewSet):
    queryset = Grantor.objects.select_related(
        'group',
        'convention',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = GrantorSerializer
    filter_class = GrantorFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "grantor"


class GroupViewSet(
    get_viewset_transition_action_mixin(Group),
    viewsets.ModelViewSet
):
    queryset = Group.objects.select_related(
        'parent',
    ).prefetch_related(
        'children',
        # 'members',
        'entries',
        'repertories',
        'officers',
    ).order_by(
        'nomen',
    )
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "group"

    # @detail_route(methods=['POST'], permission_classes=[AllowAny])
    # @parser_classes((FormParser, MultiPartParser,))
    # def image(self, request, *args, **kwargs):
    #     if 'file' in request.data:
    #         obj = self.get_object()

    #         upload = request.data['file']
    #         obj.image.save(
    #             'foo.jpg',
    #             upload,
    #         )
    #         return Response(
    #             status=status.HTTP_201_CREATED,
    #             data={'image': obj.image.url},
    #         )
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    # @detail_route(methods=['POST'], permission_classes=[AllowAny])
    # @parser_classes((FormParser, MultiPartParser,))
    # def img(self, request, *args, **kwargs):
    #     if 'file' in request.data:
    #         obj = self.get_object()
    #         file = request.data['file']
    #         public_id = str(obj.id)
    #         folder = obj._meta.model_name
    #         obj.img = upload_resource(
    #             file,
    #             public_id=public_id,
    #             folder=folder,
    #             overwrite=True,
    #             invalidate=True,
    #             format='png',
    #         )
    #         obj.save()
    #         return Response(
    #             status=status.HTTP_201_CREATED,
    #             data={'image': obj.img.url},
    #         )
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class MemberViewSet(
    get_viewset_transition_action_mixin(Member),
    viewsets.ModelViewSet
):
    queryset = Member.objects.exclude(
        group__kind__lte=30,
    ).select_related(
        'group',
        'person',
    ).order_by('id')
    serializer_class = MemberSerializer
    filter_class = MemberFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
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
        'group',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = OfficerSerializer
    filter_class = OfficerFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
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
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "panelist"


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        # 'user',
    ).prefetch_related(
        'assignments',
        # 'members',
        'officers',
        'panelists',
    ).order_by('nomen')
    serializer_class = PersonSerializer
    filter_class = PersonFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "person"

    # @detail_route(methods=['POST'], permission_classes=[AllowAny])
    # @parser_classes((FormParser, MultiPartParser,))
    # def img(self, request, *args, **kwargs):
    #     if 'file' in request.data:
    #         obj = self.get_object()
    #         file = request.data['file']
    #         public_id = str(obj.id)
    #         folder = obj._meta.model_name
    #         obj.img = upload_resource(
    #             file,
    #             public_id=public_id,
    #             folder=folder,
    #             overwrite=True,
    #             invalidate=True,
    #             format='png',
    #         )
    #         obj.save()
    #         return Response(
    #             status=status.HTTP_201_CREATED,
    #             data={'image': obj.img.url},
    #         )
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class RepertoryViewSet(
    get_viewset_transition_action_mixin(Repertory),
    viewsets.ModelViewSet
):
    queryset = Repertory.objects.select_related(
        'group',
        'chart',
    ).prefetch_related(
    ).order_by('nomen')
    serializer_class = RepertorySerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
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
        'panelists',
    ).order_by('nomen')
    serializer_class = RoundSerializer
    filter_class = RoundFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
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
    ]
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
        'competitors',
        'rounds',
    ).order_by('nomen')
    serializer_class = SessionSerializer
    filter_class = SessionFilter
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "session"


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
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "venue"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related(
        # 'person',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = UserSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "user"


class StateLogViewSet(viewsets.ModelViewSet):
    queryset = StateLog.objects.all()
    serializer_class = StateLogSerializer
    filter_class = None
    filter_backends = [
        CoalesceFilterBackend,
        DjangoFilterBackend,
    ]
    resource_name = "statelog"


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
    renderer_classes = [
        OfficeRendererCSV,
    ]
