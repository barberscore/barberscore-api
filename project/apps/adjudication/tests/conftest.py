
# Third-Party
import pytest
from rest_framework.test import APIClient
# from rest_framework.test import RequestsClient

# Django
from django.test.client import Client

# First-Party
from .factories import AppearanceFactory
from .factories import OutcomeFactory
from .factories import PanelistFactory
from .factories import RoundFactory
from .factories import ScoreFactory
from .factories import SongFactory
from .factories import UserFactory



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
    # person = PersonFactory()
    user = UserFactory(
        is_staff=False,
        # person=person,
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
def outcome():
    return OutcomeFactory()


@pytest.fixture
def panelist():
    return PanelistFactory()


@pytest.fixture
def round():
    return RoundFactory()


@pytest.fixture
def score():
    return ScoreFactory()


@pytest.fixture
def song():
    return SongFactory()


@pytest.fixture
def user():
    return UserFactory()
