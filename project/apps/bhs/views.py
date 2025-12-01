
# Standard Library
import logging
import os
import requests
from django.db import transaction

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
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.db.models import Sum, Q, Avg
from django.template.loader import render_to_string
from django.utils.text import slugify

# Local
from .filtersets import GroupFilterset
from .filtersets import PersonFilterset
from .filtersets import ChartFilterset
# from .filterbackends import RepertoryFilterBackend
from .models import Award
from .models import Group
from .models import Person
from .models import Chart

from .renderers import PDFRenderer
from .renderers import XLSXRenderer
from .renderers import DOCXRenderer
from .renderers import TXTRenderer
from .responders import PDFResponse
from .responders import XLSXResponse
from .responders import DOCXResponse
from .responders import TXTResponse

from .serializers import GroupSerializer
from .serializers import PersonSerializer
from .serializers import ChartSerializer
from .serializers import AwardSerializer

from .filtersets import ConventionFilterset
from .models import Convention
from .serializers import ConventionSerializer

# Cross-app imports for nested convention export
from apps.registration.models import Session, Assignment, Contest, Entry
from apps.registration.serializers import (
    SessionSerializer,
    AssignmentSerializer,
    ContestSerializer,
    EntrySerializer,
)
from apps.adjudication.models import Round, Panelist, Appearance, Outcome
from apps.adjudication.serializers import (
    RoundSerializer,
    PanelistSerializer,
    AppearanceSerializer,
    OutcomeSerializer,
)


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


class EnvTokenPermission(BasePermission):
    """Authorize requests using BARBERSCORE_AUTH_TOKEN from environment.

    Expects header: Authorization: Bearer <BARBERSCORE_AUTH_TOKEN>
    """
    def has_permission(self, request, view):
        expected = os.getenv('BARBERSCORE_AUTH_TOKEN', '')
        if not expected:
            return False
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return False
        provided = auth_header.split(' ', 1)[1].strip()
        return provided == expected

class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.all()
    serializer_class = ConventionSerializer
    filterset_class = ConventionFilterset
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "convention"

    @action(methods=['get', 'post'], detail=True)
    def default_owners(self, request, pk=None, **kwargs):
        convention = Convention.objects.get(pk=pk)
        default_owners = {}

        for owner in convention.organization.default_owners.all():
            default_owners[owner.id] = owner.email

        return JsonResponse(default_owners)

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
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
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
            TXTRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def bbstix(self, request, pk=None):
        convention = Convention.objects.select_related(
        ).get(pk=pk)

        # if convention.bbstix_report:
        #     txt = convention.bbstix_report.file
        # else:
        txt = convention.get_bbstix_report()

        ### Adjust File name
        file_name = '{0}{1}_BBStix'.format(
            convention.get_district_display(),
            convention.start_date.strftime("%Y%m%d")
        )

        return TXTResponse(
            txt,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=True,
        renderer_classes=[
            TXTRenderer,
        ],
        permission_classes=[DRYPermissions],
        content_negotiation_class=IgnoreClientContentNegotiation,
    )
    def bbstix_practice(self, request, pk=None):
        convention = Convention.objects.select_related(
        ).get(pk=pk)

        # if convention.bbstix_practice_report:
        #     txt = convention.bbstix_practice_report.file
        # else:
        txt = convention.get_bbstix_report(include_practice=True)

        ### Adjust File name
        file_name = '{0}{1}_BBStix2'.format(
            convention.get_district_display(),
            convention.start_date.strftime("%Y%m%d"),
        )

        return TXTResponse(
            txt,
            file_name=file_name,
            status=status.HTTP_200_OK
        )

class ConventionCompleteView(APIView):
    permission_classes = [EnvTokenPermission]

    def get(self, request, pk, format=None):
        """Return a complete JSON representation of a convention.

        Includes sessions and, for each session: details, assignments, contests,
        entries, draws and rounds. For each round includes panelists, appearances,
        outcomes, standings, and draw information.
        """
        convention = Convention.objects.get(pk=pk)

        # Base convention payload
        convention_data = ConventionSerializer(convention, context={'request': request}).data

        # Gather sessions for this convention
        sessions = Session.objects.filter(convention_id=convention.id).prefetch_related(
            'assignments',
            'contests',
            'entries',
        )

        # Build nested sessions payload
        sessions_payload = []
        for session in sessions:
            session_data = SessionSerializer(session, context={'request': request}).data

            # Assignments
            assignments_qs = session.assignments.all()
            session_data['assignments'] = AssignmentSerializer(assignments_qs, many=True, context={'request': request}).data

            # Contests (with entries)
            contests_qs = session.contests.prefetch_related('entries').all()
            session_data['contests'] = ContestSerializer(contests_qs, many=True, context={'request': request}).data

            # Entries (includes initial draw field on the entry)
            entries_qs = session.entries.all()
            session_data['entries'] = EntrySerializer(entries_qs, many=True, context={'request': request}).data

            # Session-level draw summary (initial draw numbers per entry)
            session_data['draws'] = [
                {
                    'entry_id': str(entry.id),
                    'group_id': entry.group_id,
                    'draw': entry.draw,
                }
                for entry in entries_qs
                if entry.draw is not None
            ]

            # Rounds for this session
            rounds_qs = Round.objects.filter(session_id=session.id).prefetch_related(
                'panelists',
                'appearances',
                'outcomes',
            ).order_by('num')

            rounds_payload = []
            for rnd in rounds_qs:
                round_data = RoundSerializer(rnd, context={'request': request}).data

                # Panelists
                round_data['panelists'] = PanelistSerializer(rnd.panelists.all(), many=True, context={'request': request}).data

                # Appearances (contains per-appearance draw for next round)
                appearances_qs = rnd.appearances.all().order_by('num')
                round_data['appearances'] = AppearanceSerializer(appearances_qs, many=True, context={'request': request}).data

                # Outcomes
                round_data['outcomes'] = OutcomeSerializer(rnd.outcomes.all(), many=True, context={'request': request}).data

                # Round draw summary (next-round draw numbers from appearances)
                round_data['draw'] = [
                    {
                        'appearance_id': str(app.id),
                        'group_id': app.group_id,
                        'num': app.num,
                        'draw': app.draw,
                    }
                    for app in appearances_qs if app.draw is not None
                ]

                # Simple standings calculation based on tot_points in appearance stats
                try:
                    appearances_for_rank = list(appearances_qs)
                    appearances_for_rank.sort(
                        key=lambda a: (a.stats or {}).get('tot_points', 0),
                        reverse=True,
                    )
                    round_data['standings'] = [
                        {
                            'appearance_id': str(app.id),
                            'group_id': app.group_id,
                            'tot_points': (app.stats or {}).get('tot_points', 0),
                        }
                        for app in appearances_for_rank
                    ]
                except Exception:
                    round_data['standings'] = []

                rounds_payload.append(round_data)

            session_data['rounds'] = rounds_payload

            sessions_payload.append(session_data)

        convention_data['sessions'] = sessions_payload

        return Response(convention_data)


class ConventionSyncView(APIView):
    """Sync a convention from production to staging environment.
    
    When called from production: fetches convention data from prod DB and pushes to staging.
    When called from staging: accepts convention data and syncs it to staging database.
    """
    permission_classes = [IsAuthenticated]
    
    def _is_production(self, request):
        """Check if we're running in production environment by checking request host."""
        host = request.get_host().lower()
        # If 'staging' is in the host, we're in staging; otherwise, we're in production
        return 'staging' not in host
    
    def post(self, request, pk, format=None):
        """Sync convention data from production to staging.
        
        POST /bhs/convention/<uuid>/sync
        
        If called from production:
        - Gets convention data from current (prod) database
        - POSTs it to staging environment
        
        If called from staging:
        - Accepts convention data in request body (from prod)
        - Syncs it to staging database
        """
        if self._is_production(request):
            # We're in prod - get data from prod DB and push to staging
            return self._sync_from_prod(request, pk)
        else:
            # We're in staging - accept data and sync it
            return self._sync_to_staging(request, pk)
    
    def _sync_from_prod(self, request, pk):
        """Get convention data from prod DB and push to staging."""
        # Get staging URL from environment
        staging_url = os.getenv('BARBERSCORE_STAGING_API_URL')
        if not staging_url:
            return Response(
                {'error': 'BARBERSCORE_STAGING_API_URL not configured'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get auth token from environment
        auth_token = os.getenv('BARBERSCORE_AUTH_TOKEN')
        if not auth_token:
            return Response(
                {'error': 'BARBERSCORE_AUTH_TOKEN not configured'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get convention data from current (prod) database
        try:
            convention = Convention.objects.get(pk=pk)
            convention_data = self._get_convention_complete_data(convention, request)
        except Convention.DoesNotExist:
            return Response(
                {'error': f'Convention {pk} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to get convention data: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # POST data to staging
        staging_endpoint = f"{staging_url.rstrip('/')}/bhs/convention/{pk}/sync"
        try:
            headers = {
                'Authorization': f'Bearer {auth_token}',
                'Content-Type': 'application/json'
            }
            response = requests.post(
                staging_endpoint,
                json=convention_data,
                headers=headers,
                timeout=60
            )
            response.raise_for_status()
            
            return Response({
                'message': 'Convention synced successfully to staging',
                'convention_id': pk,
                'staging_response': response.json()
            })
            
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Failed to push to staging: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )
    
    def _sync_to_staging(self, request, pk):
        """Accept convention data and sync it to staging database."""
        # Get convention data from request body
        if request.data:
            convention_data = request.data
        else:
            # Fallback: fetch from production (backward compatibility)
            production_url = os.getenv('BARBERSCORE_PROD_API_URL')
            if not production_url:
                return Response(
                    {'error': 'BARBERSCORE_PROD_API_URL not configured'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Get auth token from environment
            auth_token = os.getenv('BARBERSCORE_AUTH_TOKEN')
            if not auth_token:
                return Response(
                    {'error': 'BARBERSCORE_AUTH_TOKEN not configured'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Construct production endpoint URL
            prod_endpoint = f"{production_url.rstrip('/')}/bhs/convention/{pk}/complete"
            
            try:
                # Call production endpoint
                headers = {
                    'Authorization': f'Bearer {auth_token}',
                    'Content-Type': 'application/json'
                }
                response = requests.get(prod_endpoint, headers=headers, timeout=30)
                response.raise_for_status()
                
                convention_data = response.json()
                
            except requests.exceptions.RequestException as e:
                return Response(
                    {'error': f'Failed to fetch from production: {str(e)}'},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            except ValueError as e:
                return Response(
                    {'error': f'Invalid JSON response from production: {str(e)}'},
                    status=status.HTTP_502_BAD_GATEWAY
                )
        
        # Sync data to staging
        try:
            with transaction.atomic():
                sync_result = self._sync_convention_data(convention_data)
                
            return Response({
                'message': 'Convention synced successfully',
                'convention_id': pk,
                'sync_result': sync_result
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to sync data: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_convention_complete_data(self, convention, request):
        """Get complete convention data (same logic as ConventionCompleteView)."""
        # Base convention payload
        convention_data = ConventionSerializer(convention, context={'request': request}).data

        # Gather sessions for this convention
        sessions = Session.objects.filter(convention_id=convention.id).prefetch_related(
            'assignments',
            'contests',
            'entries',
        )

        # Build nested sessions payload
        sessions_payload = []
        for session in sessions:
            session_data = SessionSerializer(session, context={'request': request}).data

            # Assignments
            assignments_qs = session.assignments.all()
            session_data['assignments'] = AssignmentSerializer(assignments_qs, many=True, context={'request': request}).data

            # Contests (with entries)
            contests_qs = session.contests.prefetch_related('entries').all()
            session_data['contests'] = ContestSerializer(contests_qs, many=True, context={'request': request}).data

            # Entries (includes initial draw field on the entry)
            entries_qs = session.entries.all()
            session_data['entries'] = EntrySerializer(entries_qs, many=True, context={'request': request}).data

            # Session-level draw summary (initial draw numbers per entry)
            session_data['draws'] = [
                {
                    'entry_id': str(entry.id),
                    'group_id': entry.group_id,
                    'draw': entry.draw,
                }
                for entry in entries_qs
                if entry.draw is not None
            ]

            # Rounds for this session
            rounds_qs = Round.objects.filter(session_id=session.id).prefetch_related(
                'panelists',
                'appearances',
                'outcomes',
            ).order_by('num')

            rounds_payload = []
            for rnd in rounds_qs:
                round_data = RoundSerializer(rnd, context={'request': request}).data

                # Panelists
                round_data['panelists'] = PanelistSerializer(rnd.panelists.all(), many=True, context={'request': request}).data

                # Appearances (contains per-appearance draw for next round)
                appearances_qs = rnd.appearances.all().order_by('num')
                round_data['appearances'] = AppearanceSerializer(appearances_qs, many=True, context={'request': request}).data

                # Outcomes
                round_data['outcomes'] = OutcomeSerializer(rnd.outcomes.all(), many=True, context={'request': request}).data

                # Round draw summary (next-round draw numbers from appearances)
                round_data['draw'] = [
                    {
                        'appearance_id': str(app.id),
                        'group_id': app.group_id,
                        'num': app.num,
                        'draw': app.draw,
                    }
                    for app in appearances_qs if app.draw is not None
                ]

                # Simple standings calculation based on tot_points in appearance stats
                try:
                    appearances_for_rank = list(appearances_qs)
                    appearances_for_rank.sort(
                        key=lambda a: (a.stats or {}).get('tot_points', 0),
                        reverse=True,
                    )
                    round_data['standings'] = [
                        {
                            'appearance_id': str(app.id),
                            'group_id': app.group_id,
                            'tot_points': (app.stats or {}).get('tot_points', 0),
                        }
                        for app in appearances_for_rank
                    ]
                except Exception:
                    round_data['standings'] = []

                rounds_payload.append(round_data)

            session_data['rounds'] = rounds_payload

            sessions_payload.append(session_data)

        convention_data['sessions'] = sessions_payload

        return convention_data
    
    def _sync_convention_data(self, convention_data):
        """Sync convention data from production to staging database."""
        from apps.bhs.models import Convention
        from apps.registration.models import Session, Assignment, Contest, Entry
        from apps.adjudication.models import Round, Panelist, Appearance, Outcome
        
        sync_result = {
            'convention_updated': False,
            'sessions_synced': 0,
            'assignments_synced': 0,
            'contests_synced': 0,
            'entries_synced': 0,
            'rounds_synced': 0,
            'panelists_synced': 0,
            'appearances_synced': 0,
            'outcomes_synced': 0,
        }
        
        # Sync convention
        convention_id = convention_data['id']
        convention, created = Convention.objects.update_or_create(
            id=convention_id,
            defaults={
                'name': convention_data.get('name', ''),
                'district': convention_data.get('district'),
                'season': convention_data.get('season'),
                'panel': convention_data.get('panel'),
                'year': convention_data.get('year'),
                'open_date': convention_data.get('open_date'),
                'close_date': convention_data.get('close_date'),
                'start_date': convention_data.get('start_date'),
                'end_date': convention_data.get('end_date'),
                'venue_name': convention_data.get('venue_name', ''),
                'location': convention_data.get('location', ''),
                'description': convention_data.get('description', ''),
                'divisions': convention_data.get('divisions', []),
                'kinds': convention_data.get('kinds', []),
            }
        )
        sync_result['convention_updated'] = True
        
        # Sync sessions
        for session_data in convention_data.get('sessions', []):
            session_id = session_data['id']
            session, created = Session.objects.update_or_create(
                id=session_id,
                defaults={
                    'convention_id': convention_id,
                    'name': session_data.get('name', ''),
                    'district': session_data.get('district'),
                    'season': session_data.get('season'),
                    'panel': session_data.get('panel'),
                    'year': session_data.get('year'),
                    'kind': session_data.get('kind'),
                    'status': session_data.get('status'),
                    'num_rounds': session_data.get('num_rounds', 1),
                    'is_invitational': session_data.get('is_invitational', False),
                    'description': session_data.get('description', ''),
                    'notes': session_data.get('notes', ''),
                    'divisions': session_data.get('divisions', []),
                }
            )
            sync_result['sessions_synced'] += 1
            
            # Sync assignments
            for assignment_data in session_data.get('assignments', []):
                assignment_id = assignment_data['id']
                Assignment.objects.update_or_create(
                    id=assignment_id,
                    defaults={
                        'session_id': session_id,
                        'kind': assignment_data.get('kind'),
                        'category': assignment_data.get('category'),
                        'person_id': assignment_data.get('person_id'),
                        'name': assignment_data.get('name', ''),
                        'first_name': assignment_data.get('first_name', ''),
                        'last_name': assignment_data.get('last_name', ''),
                        'district': assignment_data.get('district'),
                        'email': assignment_data.get('email', ''),
                        'cell_phone': assignment_data.get('cell_phone', ''),
                    }
                )
                sync_result['assignments_synced'] += 1
            
            # Sync contests
            for contest_data in session_data.get('contests', []):
                contest_id = contest_data['id']
                Contest.objects.update_or_create(
                    id=contest_id,
                    defaults={
                        'session_id': session_id,
                        'award_id': contest_data.get('award_id'),
                        'name': contest_data.get('name', ''),
                        'kind': contest_data.get('kind'),
                        'gender': contest_data.get('gender'),
                        'level': contest_data.get('level'),
                        'season': contest_data.get('season'),
                        'description': contest_data.get('description', ''),
                        'district': contest_data.get('district'),
                        'division': contest_data.get('division'),
                    }
                )
                sync_result['contests_synced'] += 1
            
            # Sync entries
            for entry_data in session_data.get('entries', []):
                entry_id = entry_data['id']
                Entry.objects.update_or_create(
                    id=entry_id,
                    defaults={
                        'session_id': session_id,
                        'status': entry_data.get('status'),
                        'is_evaluation': entry_data.get('is_evaluation', True),
                        'is_private': entry_data.get('is_private', False),
                        'notes': entry_data.get('notes', ''),
                        'group_id': entry_data.get('group_id'),
                        'name': entry_data.get('name', ''),
                        'kind': entry_data.get('kind'),
                        'gender': entry_data.get('gender'),
                        'district': entry_data.get('district'),
                        'division': entry_data.get('division'),
                        'draw': entry_data.get('draw'),
                        'prelim': entry_data.get('prelim'),
                        'base': entry_data.get('base'),
                    }
                )
                sync_result['entries_synced'] += 1
            
            # Sync rounds
            for round_data in session_data.get('rounds', []):
                round_id = round_data['id']
                round_obj, created = Round.objects.update_or_create(
                    id=round_id,
                    defaults={
                        'session_id': session_id,
                        'status': round_data.get('status'),
                        'kind': round_data.get('kind'),
                        'num': round_data.get('num', 1),
                        'spots': round_data.get('spots', 10),
                        'date': round_data.get('date'),
                        'footnotes': round_data.get('footnotes', ''),
                    }
                )
                sync_result['rounds_synced'] += 1
                
                # Sync panelists
                for panelist_data in round_data.get('panelists', []):
                    panelist_id = panelist_data['id']
                    Panelist.objects.update_or_create(
                        id=panelist_id,
                        defaults={
                            'round_id': round_id,
                            'status': panelist_data.get('status'),
                            'num': panelist_data.get('num'),
                            'kind': panelist_data.get('kind'),
                            'category': panelist_data.get('category'),
                            'person_id': panelist_data.get('person_id'),
                            'name': panelist_data.get('name', ''),
                            'first_name': panelist_data.get('first_name', ''),
                            'last_name': panelist_data.get('last_name', ''),
                            'district': panelist_data.get('district'),
                        }
                    )
                    sync_result['panelists_synced'] += 1
                
                # Sync appearances
                for appearance_data in round_data.get('appearances', []):
                    appearance_id = appearance_data['id']
                    Appearance.objects.update_or_create(
                        id=appearance_id,
                        defaults={
                            'round_id': round_id,
                            'status': appearance_data.get('status'),
                            'num': appearance_data.get('num'),
                            'draw': appearance_data.get('draw'),
                            'is_private': appearance_data.get('is_private', False),
                            'is_single': appearance_data.get('is_single', False),
                            'participants': appearance_data.get('participants', ''),
                            'area': appearance_data.get('area', ''),
                            'onstage': appearance_data.get('onstage'),
                            'actual_start': appearance_data.get('actual_start'),
                            'actual_finish': appearance_data.get('actual_finish'),
                            'pos': appearance_data.get('pos'),
                            'stats': appearance_data.get('stats'),
                            'base': appearance_data.get('base'),
                            'group_id': appearance_data.get('group_id'),
                            'entry_id': appearance_data.get('entry_id'),
                            'name': appearance_data.get('name', ''),
                            'kind': appearance_data.get('kind'),
                            'gender': appearance_data.get('gender'),
                            'district': appearance_data.get('district'),
                            'division': appearance_data.get('division'),
                        }
                    )
                    sync_result['appearances_synced'] += 1
                
                # Sync outcomes
                for outcome_data in round_data.get('outcomes', []):
                    outcome_id = outcome_data['id']
                    Outcome.objects.update_or_create(
                        id=outcome_id,
                        defaults={
                            'round_id': round_id,
                            'status': outcome_data.get('status'),
                            'num': outcome_data.get('num'),
                            'winner': outcome_data.get('winner'),
                            'award_id': outcome_data.get('award_id'),
                            'name': outcome_data.get('name', ''),
                            'kind': outcome_data.get('kind'),
                            'gender': outcome_data.get('gender'),
                            'level': outcome_data.get('level'),
                            'season': outcome_data.get('season'),
                            'description': outcome_data.get('description', ''),
                            'district': outcome_data.get('district'),
                            'division': outcome_data.get('division'),
                        }
                    )
                    sync_result['outcomes_synced'] += 1
        
        return sync_result

class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    filterset_class = None
    ordering_fields = '__all__'
    ordering = [
        'status',
        'name',
    ]
    resource_name = "award"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_class = GroupFilterset
    ordering_fields = '__all__'
    page_size = 10
    ordering = [
        'kind',
        'name',
    ]
    resource_name = "group"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
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


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filterset_class = PersonFilterset
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "person"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        object.save()
        serializer = self.get_serializer(object)
        return Response(serializer.data)


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    filterset_class = ChartFilterset
    ordering_fields = '__all__'
    ordering = [
        'status',
        'title',
    ]
    resource_name = "chart"

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None, **kwargs):
        object = self.get_object()
        try:
            object.activate(by=self.request.user)
        except TransitionNotAllowed:
            return Response(
                {'status': 'Information incomplete.'},
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
                {'status': 'Information incomplete.'},
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
