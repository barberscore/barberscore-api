
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_award_endpoint(admin_api_client, award, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('award-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('award-detail', args=(str(award.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint(admin_api_client, chart, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('chart-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('chart-detail', args=(str(chart.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint(admin_api_client, convention, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('convention-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('convention-detail', args=(str(convention.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_group_endpoint(admin_api_client, group, django_assert_max_num_queries):
    with django_assert_max_num_queries(14):
        path = reverse('group-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(14):
        path = reverse('group-detail', args=(str(group.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_person_endpoint(admin_api_client, person, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('person-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('person-detail', args=(str(person.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK

