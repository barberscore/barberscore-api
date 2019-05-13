
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
# from .filtersets import MemberFilterset
# from .filtersets import OfficerFilterset
from .filterbackends import RepertoryFilterBackend
from .models import Group
from .models import Member
from .models import Officer
from .models import Person
from .models import Chart
from .models import Repertory
from .renderers import PDFRenderer
from .renderers import XLSXRenderer
from .responders import PDFResponse
from .responders import XLSXResponse
from .serializers import GroupSerializer
from .serializers import MemberSerializer
from .serializers import OfficerSerializer
from .serializers import PersonSerializer
from .serializers import ChartSerializer
from .serializers import RepertorySerializer


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


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'parent',
    ).prefetch_related(
        'children',
        # 'awards',
        # 'appearances',
        # 'conventions',
        # 'entries',
        'members',
        'officers',
        # 'repertories',
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
    # filterset_class = MemberFilterset
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


class OfficerViewSet(viewsets.ModelViewSet):
    queryset = Officer.objects.select_related(
        'person',
        'group',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = OfficerSerializer
    # filterset_class = OfficerFilterset
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


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.select_related(
        # 'user',
    ).prefetch_related(
        # 'assignments',
        'members',
        'officers',
        # 'panelists',
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


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.select_related(
    ).prefetch_related(
        'repertories',
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


