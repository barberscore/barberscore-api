
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_admin(admin_django_client):
    path = reverse('admin:index')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_admin(admin_django_client, assignment):
    path = reverse('admin:registration_assignment_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:registration_assignment_change', args=(str(assignment.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_admin(admin_django_client, contest):
    path = reverse('admin:registration_contest_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:registration_contest_change', args=(str(contest.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_admin(admin_django_client, entry):
    path = reverse('admin:registration_entry_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:registration_entry_change', args=(str(entry.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_admin(admin_django_client, session):
    path = reverse('admin:registration_session_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:registration_session_change', args=(str(session.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
