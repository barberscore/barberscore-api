
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_appearance_endpoint(admin_api_client, appearance, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('appearance-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('appearance-detail', args=(str(appearance.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_outcome_endpoint(admin_api_client, outcome, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('outcome-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('outcome-detail', args=(str(outcome.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_panelist_endpoint(admin_api_client, panelist, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('panelist-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('panelist-detail', args=(str(panelist.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_round_endpoint(admin_api_client, round, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('round-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('round-detail', args=(str(round.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_score_endpoint(admin_api_client, score, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('score-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('score-detail', args=(str(score.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_song_endpoint(admin_api_client, song, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('song-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('song-detail', args=(str(song.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
