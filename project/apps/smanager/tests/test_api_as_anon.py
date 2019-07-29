
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_assignment_endpoint(anon_api_client, assignment):
    # List
    path = reverse('assignment-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Detail
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Actions
    path = reverse('assignment-activate', args=(str(assignment.id),))
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('assignment-deactivate', args=(str(assignment.id),))
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contest_endpoint(anon_api_client, contest):
    path = reverse('contest-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('contest-detail', args=(str(contest.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_entry_endpoint(anon_api_client, entry):
    path = reverse('entry-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('entry-detail', args=(str(entry.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_repertory_endpoint(anon_api_client, repertory):
    path = reverse('repertory-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_session_endpoint(anon_api_client, session):
    path = reverse('session-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('session-detail', args=(str(session.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
