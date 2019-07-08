
# Standard Library
import logging

# Third-Party
from rest_framework_json_api.django_filters import DjangoFilterBackend
from django_fsm import TransitionNotAllowed
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .renderers import XLSXRenderer
from .responders import XLSXResponse

# Local
from .filtersets import AssignmentFilterset
from .filtersets import ConventionFilterset
from .models import Assignment
from .models import Award
from .models import Convention
from .serializers import AssignmentSerializer
from .serializers import AwardSerializer
from .serializers import ConventionSerializer


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

    @action(
        methods=['get'],
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def portfolio(self, request):
        xlsx = Award.objects.get_awards()
        file_name = 'awards-report'
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'group',
    ).prefetch_related(
        'sessions',
        'assignments',
        'statelogs',
    ).order_by('id')
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
