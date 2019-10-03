
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db




def test_appearance_endpoint(user_api_client, appearance):
    path = reverse('appearance-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN




def test_outcome_endpoint(user_api_client, outcome):
    path = reverse('outcome-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('outcome-detail', args=(str(outcome.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_panelist_endpoint(user_api_client, panelist):
    path = reverse('panelist-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('panelist-detail', args=(str(panelist.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK



def test_round_endpoint(user_api_client, round):
    path = reverse('round-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('round-detail', args=(str(round.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_endpoint(user_api_client, score):
    path = reverse('score-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('score-detail', args=(str(score.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_song_endpoint(user_api_client, song):
    path = reverse('song-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('song-detail', args=(str(song.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN

