import logging
log = logging.getLogger(__name__)

from rest_framework import (
    # mixins,
    viewsets,
    # filters,
)

from django.contrib.auth import get_user_model

from .models import (
    Convention,
    Contest,
    Group,
    Contestant,
    Performance,
    # Note,
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
)

User = get_user_model()


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.filter(
        is_active=True,
    ).prefetch_related(
        'contests',
        # 'contests__contestants__group',
        # 'contests__contestants__group__contestants',
        # 'contests__contestants__performances',
        # 'contests__contestants__group__lead',
        # 'contests__contestants__group__tenor',
        # 'contests__contestants__group__baritone',
        # 'contests__contestants__group__bass',
    )
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all(
        # is_active=True,
    ).prefetch_related(
        'district',
        'contestants',
        'contestants__group',
        'contestants__performances',
        # 'contestants__group__contestants',
        'contestants__group__lead',
        'contestants__group__tenor',
        'contestants__group__baritone',
        'contestants__group__bass',
    )
    serializer_class = ContestSerializer
    # filter_class = ChorusFilter
    lookup_field = 'slug'


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = Contestant.objects.select_related(
        'group',
        # 'group__contestants',
        'group__lead',
        'group__tenor',
        'group__baritone',
        'group__bass',
    ).prefetch_related(
        'performances',
        'contest',
        # 'group__contestants',
    )
    serializer_class = ContestantSerializer
    # filter_class = QuartetFilter
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related(
        'lead', 'tenor', 'baritone', 'bass'
    ).all().prefetch_related('contestants', 'district')
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    # queryset = Performance.objects.all()
    queryset = Performance.objects.select_related(
        'contestant__contest',
        'contestant__group',
    )
    # .filter(
    #     contestant__contest__convention__name='Pittsburgh 2015'
    # )
    serializer_class = PerformanceSerializer
    filter_class = PerformanceFilter
    lookup_field = 'slug'


class NoteViewSet(viewsets.ModelViewSet):
    # queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.request.user.notes


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
