
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

from .filtersets import StateLogFilterset
from .filtersets import UserFilterset

from .models import User

from .renderers import PDFRenderer
from .renderers import XLSXRenderer
from .responders import PDFResponse
from .responders import XLSXResponse

from .serializers import StateLogSerializer
from .serializers import UserSerializer


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



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related(
        'person',
    ).order_by('id')
    serializer_class = UserSerializer
    filterset_class = UserFilterset
    filter_backends = [
        DjangoFilterBackend,
    ]
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
