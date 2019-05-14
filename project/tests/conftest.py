
# Third-Party
import pytest
from rest_framework.test import APIClient
# from rest_framework.test import RequestsClient

# Django
from django.test.client import Client

# First-Party
from factories import AppearanceFactory
from factories import AssignmentFactory
from factories import AwardFactory
from factories import ChartFactory
from factories import ContenderFactory
from factories import ContestantFactory
from factories import ContestFactory
from factories import ConventionFactory
from factories import EntryFactory
from factories import GridFactory
from factories import GroupFactory
from factories import MemberFactory
from factories import OfficerFactory
from factories import OutcomeFactory
from factories import PanelistFactory
from factories import PersonFactory
from factories import RepertoryFactory
from factories import RoundFactory
from factories import ScoreFactory
from factories import SessionFactory
from factories import SongFactory
from factories import UserFactory
from factories import VenueFactory

# @pytest.fixture(scope='session')
# def django_db_modify_db_settings():
#     from django.conf import settings
#     settings.DATABASES.pop('bhs_db')


@pytest.fixture
def admin_django_client():
    admin = UserFactory(
        is_staff=True,
    )
    client = Client()
    client.force_login(admin)
    return client


@pytest.fixture
def admin_api_client():
    admin = UserFactory(
        is_staff=True,
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def user_api_client():
    person = PersonFactory()
    user = UserFactory(
        is_staff=False,
        person=person,
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def anon_api_client():
    client = APIClient()
    return client


@pytest.fixture
def appearance():
    return AppearanceFactory()


@pytest.fixture
def assignment():
    return AssignmentFactory()


@pytest.fixture
def award():
    return AwardFactory()


@pytest.fixture
def chart():
    return ChartFactory()


@pytest.fixture
def contest():
    return ContestFactory()


@pytest.fixture
def contender():
    return ContenderFactory()


@pytest.fixture
def contestant():
    return ContestantFactory()


@pytest.fixture
def convention():
    return ConventionFactory()


@pytest.fixture
def entry():
    return EntryFactory()


# @pytest.fixture
# def grid():
#     return GridFactory()


@pytest.fixture
def group():
    return GroupFactory()


@pytest.fixture
def member():
    return MemberFactory()


@pytest.fixture
def officer():
    return OfficerFactory()


@pytest.fixture
def outcome():
    return OutcomeFactory()


@pytest.fixture
def panelist():
    return PanelistFactory()


@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def repertory():
    return RepertoryFactory()


@pytest.fixture
def round():
    return RoundFactory()


@pytest.fixture
def score():
    return ScoreFactory()


@pytest.fixture
def session():
    return SessionFactory()


@pytest.fixture
def song():
    return SongFactory()

@pytest.fixture
def grid():
    return GridFactory()

@pytest.fixture
def venue():
    return VenueFactory()


# @pytest.fixture
# def venue():
#     return VenueFactory()


@pytest.fixture
def user():
    return UserFactory()
