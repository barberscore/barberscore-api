
# Standard Library
import logging

# Third-Party
import pydf
from rest_framework_json_api.filters import OrderingFilter
from rest_framework_json_api.django_filters import DjangoFilterBackend
from django_fsm import TransitionNotAllowed
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Django
from django.core.files.base import ContentFile
from django.db.models import Sum, Q, Avg
from django.template.loader import render_to_string
from django.utils.text import slugify

# Local
from .filterbackends import AppearanceFilterBackend
from .filterbackends import OutcomeFilterBackend
from .filterbackends import RepertoryFilterBackend
from .filterbackends import ScoreFilterBackend
from .filterbackends import SongFilterBackend
from .filtersets import AssignmentFilterset
from .filtersets import ConventionFilterset
from .filtersets import MemberFilterset
from .filtersets import OfficerFilterset
from .filtersets import RoundFilterset
from .filtersets import ScoreFilterset
from .filtersets import SessionFilterset
from .filtersets import StateLogFilterset
from .filtersets import UserFilterset
from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Chart
from .models import Contest
from .models import Contender
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Outcome
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User
from .models import Venue
from .renderers import PDFRenderer
from .renderers import XLSXRenderer
from .responders import PDFResponse
from .responders import XLSXResponse
from .serializers import AppearanceSerializer
from .serializers import AssignmentSerializer
from .serializers import AwardSerializer
from .serializers import ChartSerializer
from .serializers import ContenderSerializer
from .serializers import ContestantSerializer
from .serializers import ContestSerializer
from .serializers import ConventionSerializer
from .serializers import EntrySerializer
from .serializers import GridSerializer
from .serializers import GroupSerializer
from .serializers import MemberSerializer
from .serializers import OfficerSerializer
from .serializers import OfficeSerializer
from .serializers import OutcomeSerializer
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


from rest_framework.negotiation import BaseContentNegotiation

class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)

class AppearanceViewSet(viewsets.ModelViewSet):
    queryset = Appearance.objects.select_related(
        'round',
        'group',
        # 'grid',
    ).prefetch_related(
        'songs',
        # 'contenders',
        'statelogs',
    ).order_by('id')
    serializer_class = AppearanceSerializer
    filterset_class = None
    filter_backends = [
        DjangoFilterBackend,
        AppearanceFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "appearance"

    @action(methods=['get'], detail=True)
    def mock(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.mock()
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def start(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.start(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finish(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.finish(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def verify(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.verify(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def complete(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.complete(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def advance(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.advance(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def scratch(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.scratch(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def disqualify(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.disqualify(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def variance(self, request, pk=None):
        appearance = Appearance.objects.get(pk=pk)
        if appearance.variance_report:
            pdf = appearance.variance_report.file
        else:
            pdf = appearance.get_variance()
        file_name = '{0}-oss'.format(
            slugify("{0} Variance Report".format(appearance))
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def csa(self, request, pk=None):
        appearance = Appearance.objects.get(pk=pk)
        if appearance.csa:
            pdf = appearance.csa.file
        else:
            pdf = appearance.get_csa()
        file_name = '{0} {1} Session {2} CSA'.format(
            appearance.round.session.convention.name,
            appearance.round.session.get_kind_display(),
            appearance.group.name,
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )



class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        'convention',
        'person',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = AssignmentSerializer
    filterset_class = AssignmentFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "assignment"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.select_related(
        'group',
        'parent',
    ).prefetch_related(
        'children',
        'contests',
    ).order_by('status', 'name')
    serializer_class = AwardSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "award"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.select_related(
    ).prefetch_related(
        'repertories',
        'songs',
        'statelogs',
    ).order_by('status', 'title')
    serializer_class = ChartSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "chart"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def report(self, request):
        xlsx = Chart.objects.get_report()
        file_name = 'chart-report'
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        'award',
        'group',
    ).prefetch_related(
        'contestants',
        'statelogs',
    ).order_by('id')
    serializer_class = ContestSerializer
    filterset_class = None
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contest"

    @action(methods=['post'], detail=True)
    def include(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.include(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def exclude(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.exclude(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ContenderViewSet(viewsets.ModelViewSet):
    queryset = Contender.objects.select_related(
        'appearance',
        'outcome',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = ContenderSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contender"

    @action(methods=['post'], detail=True)
    def include(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.include(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def exclude(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.exclude(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'entry',
        'contest',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = ContestantSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "contestant"

    @action(methods=['post'], detail=True)
    def include(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.include(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def exclude(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.exclude(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'venue',
        'group',
    ).prefetch_related(
        'sessions',
        'assignments',
        'statelogs',
    ).distinct().order_by('id')
    serializer_class = ConventionSerializer
    filterset_class = ConventionFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "convention"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.select_related(
        'session',
        'group',
    ).prefetch_related(
        'contestants',
        'statelogs',
    ).order_by('id')
    serializer_class = EntrySerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "entry"

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.build(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def invite(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.invite(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def withdraw(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.withdraw(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def submit(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.submit(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def approve(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.approve(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class GridViewSet(viewsets.ModelViewSet):
    queryset = Grid.objects.select_related(
        'round',
        'venue',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = GridSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "grid"


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'parent',
    ).prefetch_related(
        'children',
        'awards',
        'appearances',
        'conventions',
        'entries',
        'members',
        'officers',
        'repertories',
        'statelogs',
    ).distinct()
    serializer_class = GroupSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "group"

    @action(methods=['get'], detail=True)
    def refresh(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.refresh()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[XLSXRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def roster(self, request, pk=None):
        group = Group.objects.get(pk=pk)
        xlsx = group.get_roster()
        file_name = '{0}-roster'.format(
            slugify(
                "{0}".format(
                    group.name,
                )
            )
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def quartets(self, request):
        xlsx = Group.objects.get_quartets()
        file_name = 'quartets-report'
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related(
        'group',
        'person',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = MemberSerializer
    filterset_class = MemberFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "member"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.select_related(
    ).prefetch_related(
        'officers',
    ).order_by('id')
    serializer_class = OfficeSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "office"


class OfficerViewSet(viewsets.ModelViewSet):
    queryset = Officer.objects.select_related(
        'office',
        'person',
        'group',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = OfficerSerializer
    filterset_class = OfficerFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "officer"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.select_related(
        'round',
        'award',
    ).prefetch_related(
        # 'contenders',
        'statelogs',
    ).order_by('id')
    serializer_class = OutcomeSerializer
    filter_backends = [
        DjangoFilterBackend,
        OutcomeFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "outcome"


class PanelistViewSet(viewsets.ModelViewSet):
    queryset = Panelist.objects.select_related(
        'round',
        'person',
    ).prefetch_related(
        'scores',
        'statelogs',
    ).order_by('id')
    serializer_class = PanelistSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "panelist"

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def psa(self, request, pk=None):
        panelist = Panelist.objects.get(pk=pk)
        if panelist.psa:
            pdf = panelist.psa.file
        else:
            pdf = panelist.get_psa()
        file_name = '{0} {1} {2} {3} PSA'.format(
            panelist.round.session.convention.name,
            panelist.round.session.get_kind_display(),
            panelist.round.get_kind_display(),
            panelist.person.common_name,
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )



class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        'user',
    ).prefetch_related(
        'assignments',
        'members',
        'officers',
        'panelists',
        'statelogs',
    ).order_by('id')
    serializer_class = PersonSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "person"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class RepertoryViewSet(viewsets.ModelViewSet):
    queryset = Repertory.objects.select_related(
        'group',
        'chart',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = RepertorySerializer
    filter_backends = [
        DjangoFilterBackend,
        RepertoryFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "repertory"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.deactivate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.select_related(
        'session',
    ).prefetch_related(
        'appearances',
        'panelists',
        'grids',
        'outcomes',
        'statelogs',
    ).distinct().order_by('id')
    serializer_class = RoundSerializer
    filterset_class = RoundFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "round"

    @action(methods=['get'], detail=True)
    def mock(self, request, pk=None, **kwargs):
        object = self.get_object()
        object.mock()
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def reset(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.reset(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.build(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def start(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.start(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def review(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.review(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def verify(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.verify(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finish(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.finish(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def oss(self, request, pk=None):
        round = Round.objects.select_related(
            'session',
            'session__convention',
            'session__convention__venue',
        ).get(pk=pk)
        if round.oss:
            pdf = round.oss.file
        else:
            pdf = round.get_oss()
        file_name = '{0} {1} {2} OSS'.format(
            round.session.convention.name,
            round.session.get_kind_display(),
            round.get_kind_display(),
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def legacyoss(self, request, pk=None):
        round = Round.objects.select_related(
        ).get(pk=pk)
        if round.legacy_oss:
            pdf = round.legacy_oss.file
        else:
            pdf = round.get_legacy_oss()
        file_name = '{0} {1} {2} Legacy OSS'.format(
            round.session.convention.name,
            round.session.get_kind_display(),
            round.get_kind_display(),
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def titles(self, request, pk=None):
        round = Round.objects.prefetch_related(
            'appearances',
        ).get(pk=pk)
        pdf = round.get_titles()
        file_name = '{0} {1} {2} Titles Report'.format(
            round.session.convention.name,
            round.session.get_kind_display(),
            round.get_kind_display(),
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[PDFRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def sa(self, request, pk=None):
        round = Round.objects.select_related(
            'session',
            'session__convention',
            'session__convention__venue',
        ).get(pk=pk)
        if round.sa:
            pdf = round.sa.file
        else:
            pdf = round.get_sa()
        file_name = '{0} {1} {2} SA'.format(
            round.session.convention.name,
            round.session.get_kind_display(),
            round.get_kind_display(),
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def announcements(self, request, pk=None):
        round = Round.objects.select_related(
        ).get(pk=pk)
        pdf = round.get_announcements()
        file_name = '{0} {1} {2} Announcements'.format(
            round.session.convention.name,
            round.session.get_kind_display(),
            round.get_kind_display(),
        )
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'panelist',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = ScoreSerializer
    filterset_class = ScoreFilterset
    filter_backends = [
        DjangoFilterBackend,
        ScoreFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "score"


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related(
        'convention',
    ).prefetch_related(
        'contests',
        'entries',
        'rounds',
        'statelogs',
    ).distinct().order_by('id')
    serializer_class = SessionSerializer
    filterset_class = SessionFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "session"

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.build(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def open(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.open(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def close(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.close(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def verify(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.verify(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def package(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.package(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finish(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.finish(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Transition conditions not met.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[XLSXRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def legacy(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        if session.legacy_report:
            xlsx = session.legacy_report.file
        else:
            xlsx = session.get_legacy()
        file_name = '{0} {1} Session Legacy Report'.format(
            session.convention.name,
            session.get_kind_display(),
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[XLSXRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def drcj(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        if session.drcj_report:
            xlsx = session.drcj_report.file
        else:
            xlsx = session.get_drcj()
        file_name = '{0} {1} Session DRCJ Report'.format(
            session.convention.name,
            session.get_kind_display(),
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[XLSXRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def contact(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        if session.contact_report:
            xlsx = session.contact_report.file
        else:
            xlsx = session.get_contact()
        file_name = '{0} {1} Session Contact Report'.format(
            session.convention.name,
            session.get_kind_display()
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'appearance',
        'chart',
    ).prefetch_related(
        'scores',
    ).order_by('id')
    serializer_class = SongSerializer
    filterset_class = None
    filter_backends = [
        DjangoFilterBackend,
        SongFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "song"


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.select_related(
    ).prefetch_related(
        'conventions',
        'grids',
        'statelogs',
    ).order_by('name')
    serializer_class = VenueSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "venue"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related(
        'person',
    ).order_by('id')
    serializer_class = UserSerializer
    filterset_class = UserFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    # filterset_fields = {
    #         'username': [
    #             'exact',
    #         ],
    #     }

    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "user"


class StateLogViewSet(viewsets.ModelViewSet):
    queryset = StateLog.objects.select_related(
        'content_type',
        'by',
    ).prefetch_related(
    )
    serializer_class = StateLogSerializer
    filterset_class = StateLogFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        IsAuthenticated,
    ]
    resource_name = "statelog"
