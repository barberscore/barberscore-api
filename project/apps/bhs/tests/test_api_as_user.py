
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_award_endpoint(user_api_client, award):
    path = reverse('award-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('award-detail', args=(str(award.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint(user_api_client, chart):
    path = reverse('chart-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('chart-detail', args=(str(chart.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint(user_api_client, convention):
    path = reverse('convention-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('convention-detail', args=(str(convention.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_endpoint(user_api_client, group):
    path = reverse('group-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('group-detail', args=(str(group.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint(user_api_client, person):
    path = reverse('person-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('person-detail', args=(str(person.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK

