
# Standard Library
import logging
import re
import uuid

# Third-Party
import pydf
import json
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
from rest_framework.parsers import JSONParser
from rest_framework.renderers import StaticHTMLRenderer
import django_rq

# Django
from django.apps import apps
from django.core.files.base import ContentFile
from django.db.models import Sum, Q, Avg
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.six import BytesIO
from collections.abc import Iterable
from django.contrib.auth import get_user_model

# Local
# from .filterbackends import AppearanceFilterBackend
# from .filterbackends import OutcomeFilterBackend
# from .filterbackends import ScoreFilterBackend
# from .filterbackends import SongFilterBackend

from .filtersets import RoundFilterset
from .filtersets import ScoreFilterset

from .models import Appearance
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Song
from apps.bhs.models import Convention

from .renderers import PDFRenderer
from .renderers import XLSXRenderer
from .renderers import DOCXRenderer
from .renderers import RTFRenderer
from .responders import PDFResponse
from .responders import XLSXResponse
from .responders import DOCXResponse
from .responders import RTFResponse

from .serializers import AppearanceSerializer
from .serializers import OutcomeSerializer
from .serializers import PanelistSerializer
from .serializers import RoundSerializer
from .serializers import ScoreSerializer
from .serializers import SongSerializer


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
        # 'group',
        # 'entry',
    ).prefetch_related(
        'owners',
        'songs',
        # 'statelogs',
    ).order_by('id')
    serializer_class = AppearanceSerializer
    filterset_class = None
    filter_backends = [
        DjangoFilterBackend,
        # AppearanceFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "appearance"

    def perform_create(self, serializer):
        Entry = apps.get_model('registration.entry')
        Chart = apps.get_model('bhs.chart')
        group_id = serializer.initial_data['group_id']
        charts_raw = Chart.objects.filter(
            groups__id=group_id,
        ).values(
            'id',
            'title',
            'arrangers',
        ).order_by('title')
        for c in charts_raw:
            c['pk'] = str(c.pop('id'))
        charts = [json.dumps(x) for x in charts_raw]

        # print(serializer.initial_data['round']['id'])

        parent_round = Round.objects.get(id=serializer.initial_data['round']['id'])

        try:
            entry = Entry.objects.get(
                session_id=parent_round.session_id,
                group_id=group_id
            )

            # print("add participants...")
            serializer.save(
                charts=charts,
                participants=entry.participants,
                entry_id=entry.id,
            )            
        except Entry.DoesNotExist:
            serializer.save(charts=charts)

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

    @action(methods=['post'], detail=True)
    def verify(self, request, pk=None, **kwargs):
        Song = apps.get_model('adjudication.song')
        object = self.get_object()

        # For Choruses, ensure a valid number of participants on stage has been entered.
        if object.kind == object.KIND.chorus and (object.pos is None or object.pos < 8):
            return Response(
                {'status': 'Please enter a valid number of Participants on stage.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure both songs have valid selections.
        appearanceSongs = Song.objects.filter(appearance_id=object).values_list('title', flat=True)
        songs = []
        for title in appearanceSongs:
            if len(title) > 0:
                songs.append(title)
        if songs is None or len(songs) < 2:
            return Response(
                {'status': 'Please select two song titles for this appearance.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            object.verify(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete. Unable to verify appearance. Check entered scores.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
        # if appearance.variance_report:
        #     pdf = appearance.variance_report.file
        # else:
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
        # if appearance.csa_report:
        #     pdf = appearance.csa_report.file
        # else:
        pdf = appearance.get_csa()

        file_name = '{0} CSA.pdf'.format(appearance)
        file_name = re.sub('[^a-zA-Z0-9_ ]', '', file_name)
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.select_related(
        'round',
        # 'award',
    ).prefetch_related(
        'statelogs',
    ).order_by('id')
    serializer_class = OutcomeSerializer
    filter_backends = [
        DjangoFilterBackend,
        # OutcomeFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "outcome"

    def partial_update(self, request, pk=None):
        # Current object
        object = self.get_object()

        # Get current state of Outcome
        o = Outcome.objects.get(pk=request.data['id'])

        # If Print on Finals OSS has been set, deselect the "Printed" option        
        if request.data['print_on_finals_oss'] and o.print_on_finals_oss is False:
            request.data['printed'] = False

        try:
            # Update Outcome
            return super().partial_update(request, *pk)

        except ValueError as e:
            return Response(
                {'status': 'Unable to change outcome'},
                status=status.HTTP_400_BAD_REQUEST,
            )

class PanelistViewSet(viewsets.ModelViewSet):
    queryset = Panelist.objects.select_related(
        'round',
        # 'user',
    ).prefetch_related(
        'scores',
    ).order_by('id')
    serializer_class = PanelistSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "panelist"

    def perform_create(self, serializer):
        person_id = serializer.initial_data['person_id']
        Person = apps.get_model('bhs.person')
        person = Person.objects.get(pk=person_id)

        if serializer.initial_data['category'] in [Panelist.CATEGORY.adm, Panelist.CATEGORY.pc]:
            #
            # Add PC or ADM as owner of Round, Session, and Convention
            #
            User = get_user_model()
            owner = User.objects.filter(email=person.email).first()

            # Parent round to access session ID
            parent_round = Round.objects.get(pk=serializer.initial_data['round']['id'])

            # Session
            Session = apps.get_model('registration.session')
            session = Session.objects.get(pk=parent_round.session_id)
            session.owners.add(owner.id)

            # Rounds under session
            rounds = Round.objects.filter(
                    session_id=session.id
                )
            for round in rounds:
                round.owners.add(owner.id)

            # Convention
            convention = Convention.objects.get(pk=session.convention_id)
            convention.owners.add(owner.id)

        # Save Panelist record
        serializer.save(
            email=person.email
        )

    def partial_update(self, request, pk=None):
        # Current object
        object = self.get_object()

        if type(request.data['airports']) == str:
            print("airports is string")
            request.data.pop('airports')

        try:
            # Submitted number...
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()

            ## See if the submitted number already exists
            if (request.data['num'] is not object.num and Panelist.objects.filter(
                    num=request.data['num'],
                    round_id=object.round_id,
                ).count()):
                raise ValueError()

            # Update Panelist
            return super().partial_update(request, *pk)

        except ValueError as e:
            return Response(
                {'status': 'Number is already in use by another judge.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_destroy(self, instance):
        # print("perform_destroy function", instance.id)

        if instance.category in [Panelist.CATEGORY.adm, Panelist.CATEGORY.pc]:
            #
            # Remove PC or ADM as owner of Round, Session, and Convention
            #
            Person = apps.get_model('bhs.person')
            person = Person.objects.get(pk=instance.person_id)

            User = get_user_model()
            owner = User.objects.filter(email=person.email).first()

            # Round
            parent_round = Round.objects.get(pk=instance.round_id)

            # Session
            Session = apps.get_model('registration.session')
            session = Session.objects.get(pk=parent_round.session_id)
            session.owners.remove(owner.id)

            # Parent round to access session ID
            rounds = Round.objects.filter(
                    session_id=session.id
                )
            for round in rounds:
                round.owners.remove(owner.id)

            # Convention
            convention = Convention.objects.get(pk=session.convention_id)
            convention.owners.remove(owner.id)

            # print("CA removed as owner")

        # Remove Panelist record
        return super().perform_destroy(instance)

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
        # if panelist.psa_report:
        #     pdf = panelist.psa_report.file
        # else:
        pdf = panelist.get_psa()
        file_name = '{0} PSA.pdf'.format(panelist)
        return PDFResponse(
            pdf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.select_related(
        # 'session',
    ).prefetch_related(
        'owners',
        'appearances',
        # 'appearances__owners',
        # 'appearances__songs',
        # 'panelists__scores',
        # 'outcomes__award',
    ).order_by('id')
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def finalize(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.finalize(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Unable to Finalize round.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None, **kwargs):
        # Confirm queue is empty...
        queue = django_rq.get_queue('high')
        if (not queue.is_empty()):
            return Response(
                {'status': 'This Round cannot publish yet because there are tasks still in progress. Please wait and try again in 2-5 minutes.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object = self.get_object()
        try:
            object.publish(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Unable to Publish round.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)

    @action(
        methods=['get', 'post'],
        detail=True,
        renderer_classes=[
            PDFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def oss(self, request, pk=None):
        round = Round.objects.select_related(
            # 'session',
            # 'session__convention',
        ).get(pk=pk)
        # if round.oss_report:
        #     pdf = round.oss_report.file
        # else:

        # Allow selectable paper size        
        paper_size = None
        if len(request._request.body):
            content = BytesIO(request._request.body)
            data = JSONParser().parse(content)
            if data['paperSize']:
                paper_size = data['paperSize'].strip()
                
        pdf = round.get_oss(request.user.name, paper_size)
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
        # if round.legacy_oss:
        #     pdf = round.legacy_oss.file
        # else:
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
        file_name = '{0} Titles Report'.format(
            round.nomen,
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
            PDFRenderer
            # StaticHTMLRenderer
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def sa(self, request, pk=None):
        round = Round.objects.select_related(
            # 'session',
            # 'session__convention',
        ).get(pk=pk)
        # if round.sa_report:
        #     pdf = round.sa_report.file
        # else:
        pdf = round.get_sa(request.user.name)

        # return Response(pdf)
        file_name = '{0} SA'.format(
            round.nomen,
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
        file_name = '{0} Announcements'.format(
            round.nomen,
        )
        return DOCXResponse(
            docx,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['post'],
        detail=True,
        renderer_classes=[
            RTFRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def labels(self, request, pk=None, **kwargs):
        round = self.get_object()

        # Parse inbound request
        if len(request._request.body):
            content = BytesIO(request._request.body)
            data = JSONParser().parse(content)
        else:
            data = {}

        convention = Convention.objects.filter(
            id=round.convention_id
        ).first()

        # File name postfix
        postfix = ""
        if len(data):
            postfix = "_" + data['postfix'].strip()

        rtf = round.get_labels(request, data)

        ### Concatenate File name
        file_name = '{0}_Lbls{1}'.format(
            convention.base_filename(),
            postfix
        )

        return RTFResponse(
            rtf,
            file_name=file_name,
            status=status.HTTP_200_OK
        )


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related(
        'song',
        'song__appearance',
        'song__appearance__round',
        'panelist',
    ).prefetch_related(
    ).order_by('id')
    serializer_class = ScoreSerializer
    filterset_class = ScoreFilterset
    filter_backends = [
        DjangoFilterBackend,
        # ScoreFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "score"

    def partial_update(self, request, pk=None):
        object = self.get_object()

        # Update Score
        super().partial_update(request, *pk)

        # Reset appearance status???
        appearance = Appearance.objects.filter(
                id=object.song.appearance.id
            )

        if appearance[0].status <= Appearance.STATUS.finished:
            # Update appearance stats
            stats = appearance[0].get_stats()

            appearance.update(
                status=Appearance.STATUS.finished,
                stats=stats
            )
        else:
            appearance.update(
                status=Appearance.STATUS.finished,
            )

        # Resave score for return
        return super().partial_update(request, *pk)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related(
        'appearance',
    ).prefetch_related(
        'scores',
        'scores__panelist',
    ).order_by('id')
    serializer_class = SongSerializer
    filterset_class = None
    filter_backends = [
        DjangoFilterBackend,
        # SongFilterBackend,
    ]
    permission_classes = [
        DRYPermissions,
    ]
    resource_name = "song"
