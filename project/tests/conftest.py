
# Third-Party
import pytest
from rest_framework.test import APIClient

# Django
from django.test.client import Client

# First-Party
from api.factories import AppearanceFactory
from api.factories import AssignmentFactory
from api.factories import AwardFactory
from api.factories import ChartFactory
from api.factories import CompetitorFactory
from api.factories import ContestantFactory
from api.factories import ContestFactory
from api.factories import ConventionFactory
from api.factories import EntryFactory
from api.factories import GrantorFactory
from api.factories import GridFactory
from api.factories import GroupFactory
from api.factories import MemberFactory
from api.factories import OfficeFactory
from api.factories import OfficerFactory
from api.factories import OutcomeFactory
from api.factories import PanelistFactory
from api.factories import PersonFactory
from api.factories import RepertoryFactory
from api.factories import RoundFactory
from api.factories import ScoreFactory
from api.factories import SessionFactory
from api.factories import SongFactory
from api.factories import UserFactory
from api.factories import VenueFactory

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
def contestant():
    return ContestantFactory()


@pytest.fixture
def convention():
    return ConventionFactory()


@pytest.fixture
def competitor():
    return CompetitorFactory()


@pytest.fixture
def entry():
    return EntryFactory()


@pytest.fixture
def grantor():
    return GrantorFactory()


@pytest.fixture
def grid():
    return GridFactory()


@pytest.fixture
def group():
    return GroupFactory()


@pytest.fixture
def member():
    return MemberFactory()


@pytest.fixture
def office():
    return OfficeFactory()


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
def venue():
    return VenueFactory()


@pytest.fixture
def user():
    return UserFactory()
