import logging
log = logging.getLogger(__name__)

from rest_framework import (
    viewsets,
)

from drf_haystack.viewsets import HaystackViewSet

# from rest_framework.pagination import (
#     PageNumberPagination,
# )

from django.contrib.auth import get_user_model

from .models import (
    Convention,
    Contest,
    Group,
    Contestant,
    Singer,
    Director,
    District,
    Song,
    Person,
)

from .serializers import (
    ConventionSerializer,
    ContestSerializer,
    GroupSerializer,
    ContestantSerializer,
    NoteSerializer,
    UserSerializer,
    SingerSerializer,
    DirectorSerializer,
    DistrictSerializer,
    SongSerializer,
    PersonSerializer,
    SearchSerializer,
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
    ).filter(
        level=Contest.INTERNATIONAL,
        is_active=True,
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
        'P_director',
        'P_district',
        'P_lead',
        'P_tenor',
        'P_baritone',
        'P_bass',
    ).prefetch_related(
        'performances',
    )
    serializer_class = ContestantSerializer
    # pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().prefetch_related(
        'contestants',
    )
    serializer_class = GroupSerializer
    lookup_field = 'slug'


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


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.prefetch_related(
        'contestants_P_director',
        'contestants_P_lead',
        'contestants_P_tenor',
        'contestants_P_baritone',
        'contestants_P_bass',
    )
    serializer_class = PersonSerializer
    lookup_field = 'slug'


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.prefetch_related(
        'contestants',
    )
    serializer_class = DistrictSerializer
    # pagination_class = PageNumberPagination
    lookup_field = 'slug'


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_field = 'slug'


class SearchViewSet(HaystackViewSet):
    serializer_class = SearchSerializer
