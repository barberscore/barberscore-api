import logging
log = logging.getLogger(__name__)

from rest_framework import (
    viewsets,
)

from django.contrib.auth import get_user_model

from .models import (
    Convention,
    Contest,
    Group,
    Contestant,
    Performance,
    Singer,
    Director,
)

from .filters import (
    PerformanceFilter,
    GroupFilter,
)


from .serializers import (
    ConventionSerializer,
    ContestSerializer,
    GroupSerializer,
    ContestantSerializer,
    PerformanceSerializer,
    NoteSerializer,
    UserSerializer,
    SingerSerializer,
    DirectorSerializer,
)

User = get_user_model()


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.select_related(
        'district',
    ).filter(
        is_active=True,
    ).prefetch_related(
        'contests',
    )
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.select_related(
        'district',
        'convention',
    ).prefetch_related(
        'district',
        'contestants',
    )
    serializer_class = ContestSerializer
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'group',
        'contest',
        'director',
        'district',
        'lead',
        'tenor',
        'baritone',
        'bass',
    ).prefetch_related(
        'performances',
    )
    serializer_class = ContestantSerializer
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        'contestants',
    )
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related(
        'contestant',
        'contestant__contest',
        'contestant__group',
    )
    serializer_class = PerformanceSerializer
    filter_class = PerformanceFilter


class NoteViewSet(viewsets.ModelViewSet):
    # queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.request.user.notes


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.prefetch_related(
        'contestants_lead',
        'contestants_tenor',
        'contestants_baritone',
        'contestants_bass',
    )
    serializer_class = SingerSerializer
    lookup_field = 'slug'


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.prefetch_related(
        'contestants',
    )
    serializer_class = DirectorSerializer
    lookup_field = 'slug'
