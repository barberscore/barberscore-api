import json

# Third-Party
from django_fsm import TransitionNotAllowed
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_json_api import views
from django.db.models import Prefetch

# Django
from django.apps import apps

# Local
from .filtersets import EntryFilterset
from .filtersets import SessionFilterset
from .models import Assignment
from .models import Contest
from .models import Entry
from .models import Session
from .negotiators import IgnoreClientContentNegotiation
from .renderers import XLSXRenderer
from .responders import XLSXResponse
from .serializers import AssignmentSerializer
from .serializers import ContestSerializer
from .serializers import EntrySerializer
from .serializers import SessionSerializer


class AssignmentViewSet(views.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    filterset_class = None
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "assignment"


class ContestViewSet(views.ModelViewSet):
    queryset = Contest.objects.prefetch_related(
            Prefetch('entries', queryset=Entry.objects.exclude(status=7)),
    )
    serializer_class = ContestSerializer
    filterset_class = None
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "contest"


class EntryViewSet(views.ModelViewSet):
    queryset = Entry.objects.all()
    prefetch_for_includes = {
        '__all__': [],
    }
    serializer_class = EntrySerializer
    filterset_class = EntryFilterset
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "entry"

    def partial_update(self, request, pk=None):
        # Current object
        object = self.get_object()

        Appearance = apps.get_model('adjudication.appearance')
        Round = apps.get_model('adjudication.round')
        appearances = Appearance.objects.filter(entry_id=object.id)

        if request.data['participants'] is not None or request.data['base'] is not None or request.data['is_private']:
            # Update Participant names for associated appearances
            for a in appearances:
                # Update is private
                a.is_private=request.data['is_private']

                # Update base score
                a.base=request.data['base']

                # Update paritcipant names
                a.participants=request.data['participants']
                a.save()

        # Recalculate Round outcomes
        for a in appearances:
            r = Round.objects.get(id=a.round_id)
            r.determine_winners()

        # Save Entry
        return super().partial_update(request, *pk)

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.build(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def contest(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.update_contests(by=self.request.user)
            entry = Entry.objects.get(pk=object.id)
            serializer = self.get_serializer(entry)
            return Response(serializer.data)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Unable to change contests incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def update_charts(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.update_charts(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

class SessionViewSet(views.ModelViewSet):
    queryset = Session.objects.prefetch_related(
            # Prefetch('entries', queryset=Entry.objects.exclude(status=7)),
            'entries',
            Prefetch('assignments', queryset=Assignment.objects.filter(kind__gte=0)),
            'contests',
            'statelogs',
            'owners',
        )
    prefetch_for_includes = {
        '__all__': [],
    }
    # queryset.filter(
    #     assignments__kind__gt=0
    # )
    serializer_class = SessionSerializer
    filterset_class = SessionFilterset
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "session"

    @action(methods=['post'], detail=True)
    def build(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.build(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[XLSXRenderer],
        # permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def legacy(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        # if session.legacy_report:
        #     xlsx = session.legacy_report.file
        # else:
        xlsx = session.get_legacy_report()
        file_name = '{0} Legacy Report'.format(
            session.nomen,
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
        # permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def drcj(self, request, pk=None):
        session = Session.objects.get(pk=pk)
        # if session.drcj_report:
        #     xlsx = session.drcj_report.file
        # else:
        xlsx = session.get_drcj_report()
        file_name = '{0} DRCJ Report'.format(
            session.nomen,
        )
        return XLSXResponse(
            xlsx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )
