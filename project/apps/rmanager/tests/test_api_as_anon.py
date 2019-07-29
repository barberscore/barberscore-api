
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db




def test_appearance_endpoint(anon_api_client, appearance):
    # List
    path = reverse('appearance-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Detail
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Actions
    path = reverse('appearance-start', args=(str(appearance.id),))
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('appearance-finish', args=(str(appearance.id),))
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('appearance-verify', args=(str(appearance.id),))
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_outcome_endpoint(anon_api_client, outcome):
    path = reverse('outcome-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('outcome-detail', args=(str(outcome.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_panelist_endpoint(anon_api_client, panelist):
    path = reverse('panelist-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('panelist-detail', args=(str(panelist.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_round_endpoint(anon_api_client, round):
    path = reverse('round-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('round-detail', args=(str(round.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_score_endpoint(anon_api_client, score):
    path = reverse('score-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('score-detail', args=(str(score.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_song_endpoint(anon_api_client, song):
    path = reverse('song-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('song-detail', args=(str(song.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

