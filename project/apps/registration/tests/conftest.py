
# Third-Party
import pytest
from rest_framework.test import APIClient
# from rest_framework.test import RequestsClient

# Django
from django.test.client import Client

# First-Party
from .factories import AssignmentFactory
from .factories import ContestFactory
from .factories import EntryFactory
from .factories import SessionFactory
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
def assignment():
    return AssignmentFactory()



@pytest.fixture
def contest():
    return ContestFactory()



@pytest.fixture
def entry():
    return EntryFactory()



@pytest.fixture
def session():
    return SessionFactory()



@pytest.fixture
def user():
    return UserFactory()
