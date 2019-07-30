
# Standard Library
import logging

# Third-Party
import pydf
from rest_framework_json_api.filters import OrderingFilter
from rest_framework_json_api.django_filters import DjangoFilterBackend
from django_fsm import TransitionNotAllowed
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
from .filtersets import EntryFilterset
from .filtersets import SessionFilterset

from .models import Contest
from .models import Entry
from .models import Session
from .renderers import PDFRenderer
from .renderers import XLSXRenderer
from .responders import PDFResponse
from .responders import XLSXResponse
from .serializers import ContestSerializer
from .serializers import EntrySerializer
from .serializers import SessionSerializer
# from .filtersets import AssignmentFilterset
from .models import Assignment
from .serializers import AssignmentSerializer
from .serializers import RepertorySerializer


log = logging.getLogger(__name__)


from rest_framework.negotiation import BaseContentNegotiation

from .models import Repertory

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


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related(
        # 'user',
        # 'convention',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = AssignmentSerializer
    # filterset_class = AssignmentFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "assignment"

    # @action(methods=['post'], detail=True)
    # def activate(self, request, pk=None, **kwargs):
    #     object = self.get_object()
    #     try:
    #         object.activate(by=self.request.user)
    #     except TransitionNotAllowed:
    #         return Response(
    #             {'status': 'Transition conditions not met.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     object.save()
    #     serializer = self.get_serializer(object)
    #     return Response(serializer.data)

    # @action(methods=['post'], detail=True)
    # def deactivate(self, request, pk=None, **kwargs):
    #     object = self.get_object()
    #     try:
    #         object.deactivate(by=self.request.user)
    #     except TransitionNotAllowed:
    #         return Response(
    #             {'status': 'Transition conditions not met.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     object.save()
    #     serializer = self.get_serializer(object)
    #     return Response(serializer.data)


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'session',
        # 'award',
    ).prefetch_related(
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

    # @action(methods=['post'], detail=True)
    # def include(self, request, pk=None, **kwargs):
    #     object = self.get_object()
    #     try:
    #         object.include(by=self.request.user)
    #     except TransitionNotAllowed:
    #         return Response(
    #             {'status': 'Transition conditions not met.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     object.save()
    #     serializer = self.get_serializer(object)
    #     return Response(serializer.data)

    # @action(methods=['post'], detail=True)
    # def exclude(self, request, pk=None, **kwargs):
    #     object = self.get_object()
    #     try:
    #         object.exclude(by=self.request.user)
    #     except TransitionNotAllowed:
    #         return Response(
    #             {'status': 'Transition conditions not met.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     object.save()
    #     serializer = self.get_serializer(object)
    #     return Response(serializer.data)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.select_related(
        'session',
        # 'group',
    ).prefetch_related(
        'statelogs',
        'owners',
    ).order_by('id')
    serializer_class = EntrySerializer
    filterset_class = EntryFilterset
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


class RepertoryViewSet(viewsets.ModelViewSet):
    queryset = Repertory.objects.select_related(
        # 'group',
        # 'chart',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = RepertorySerializer
    filter_backends = [
        DjangoFilterBackend,
        # RepertoryFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "repertory"

    # @action(methods=['post'], detail=True)
    # def activate(self, request, pk=None, **kwargs):
    #     object = self.get_object()
    #     try:
    #         object.activate(by=self.request.user)
    #     except TransitionNotAllowed:
    #         return Response(
    #             {'status': 'Transition conditions not met.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     object.save()
    #     serializer = self.get_serializer(object)
    #     return Response(serializer.data)

    # @action(methods=['post'], detail=True)
    # def deactivate(self, request, pk=None, **kwargs):
    #     object = self.get_object()
    #     try:
    #         object.deactivate(by=self.request.user)
    #     except TransitionNotAllowed:
    #         return Response(
    #             {'status': 'Transition conditions not met.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
    #     object.save()
    #     serializer = self.get_serializer(object)
    #     return Response(serializer.data)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related(
        # 'convention',
        'target',
    ).prefetch_related(
        'owners',
        'contests',
        'entries',
    ).order_by('id')
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
            xlsx = session.get_legacy_report()
        file_name = '{0} {1} Session Legacy Report'.format(
            # session.convention,
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
            xlsx = session.get_drcj_report()
        file_name = '{0} {1} Session DRCJ Report'.format(
            session.convention,
            session.get_kind_display(),
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )
