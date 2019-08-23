
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_assignment_endpoint(user_api_client, assignment):
    path = reverse('assignment-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint(user_api_client, contest):
    path = reverse('contest-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('contest-detail', args=(str(contest.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint(user_api_client, entry):
    path = reverse('entry-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('entry-detail', args=(str(entry.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint(user_api_client, repertory):
    path = reverse('repertory-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_session_endpoint(user_api_client, session):
    path = reverse('session-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('session-detail', args=(str(session.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
