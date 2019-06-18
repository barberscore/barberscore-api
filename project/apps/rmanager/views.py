
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
from .filterbackends import ScoreFilterBackend
from .filterbackends import SongFilterBackend

from .filtersets import RoundFilterset
from .filtersets import ScoreFilterset

from .models import Appearance
from .models import Contender
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Song

from .renderers import PDFRenderer
from .renderers import XLSXRenderer
from .responders import PDFResponse
from .responders import XLSXResponse
from .renderers import DOCXRenderer
from .responders import DOCXResponse

from .serializers import AppearanceSerializer
from .serializers import ContenderSerializer
from .serializers import OutcomeSerializer
from .serializers import PanelistSerializer
from .serializers import RoundSerializer
from .serializers import ScoreSerializer
from .serializers import SongSerializer
from .serializers import StateLogSerializer


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
        'entry',
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
        """
        Mocks an Appearance using fake data.
        """
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
        file_name = '{0} Variance Report.pdf'.format(appearance)
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
        """
        Renders the Competitor Scoring Analysis in PDF
        """
        appearance = Appearance.objects.get(pk=pk)
        if appearance.csa:
            pdf = appearance.csa.file
        else:
            pdf = appearance.get_csa()
        file_name = '{0} CSA.pdf'.format(appearance)
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


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
        file_name = '{0} PSA.pdf'.format(panelist)
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


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
    def publish(self, request, pk=None, **kwargs):
        object = self.get_object()
        # try:
        #     object.publish(by=self.request.user)
        # except TransitionNotAllowed:
        #     return Response(
        #         {'status': 'Transition conditions not met.'},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        object.publish(by=self.request.user)
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
        file_name = '{0} OSS.pdf'.format(round)
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
    def legacy(self, request, pk=None):
        round = Round.objects.get(pk=pk)
        if round.legacy_oss:
            pdf = round.legacy_oss.file
        else:
            pdf = round.get_legacy_oss()
        file_name = '{0} Legacy OSS.pdf'.format(round)
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
        file_name = '{0} Legacy OSS.pdf'.format(round)
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
            round.session.convention,
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
            round.session.convention,
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
            DOCXRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def announcements(self, request, pk=None):
        round = Round.objects.select_related(
        ).get(pk=pk)
        docx = round.get_announcements()
        file_name = '{0} {1} {2} Announcements'.format(
            round.session.convention,
            round.session.get_kind_display(),
            round.get_kind_display(),
        )
        return DOCXResponse(
            docx,
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

