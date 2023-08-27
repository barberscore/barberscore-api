
# Standard Library
import logging

# Third-Party
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
from django.core import serializers
from django.http import JsonResponse

# from django.core.files.base import ContentFile
# from django.db.models import Sum, Q, Avg
# from django.template.loader import render_to_string
# from django.utils.text import slugify

# Local
from .models import Organization
from .models import District
from .models import Division

from .serializers import OrganizationSerializer



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


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # filterset_class = ConventionFilterset
    ordering_fields = '__all__'
    ordering = [
        'name',
    ]
    resource_name = "organization"

    @action(methods=['get', 'post'], detail=True)
    def default_owners(self, request, pk=None, **kwargs):
        organization = Organization.objects.get(pk=pk)
        default_owners = {}

        for owner in organization.default_owners.all():
            default_owners[owner.id] = owner.email

        return JsonResponse(default_owners)
