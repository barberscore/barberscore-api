
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


def test_appearance_admin(admin_django_client, appearance):
    path = reverse('admin:adjudication_appearance_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:adjudication_appearance_change', args=(str(appearance.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_outcome_admin(admin_django_client, outcome):
    path = reverse('admin:adjudication_outcome_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:adjudication_outcome_change', args=(str(outcome.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_admin(admin_django_client, panelist):
    path = reverse('admin:adjudication_panelist_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:adjudication_panelist_change', args=(str(panelist.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_admin(admin_django_client, round):
    # path = reverse('admin:adjudication_round_changelist')
    # response = admin_django_client.get(path)
    # assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:adjudication_round_change', args=(str(round.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_admin(admin_django_client, score):
    path = reverse('admin:adjudication_score_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:adjudication_score_change', args=(str(score.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_admin(admin_django_client, song):
    path = reverse('admin:adjudication_song_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:adjudication_song_change', args=(str(song.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK

