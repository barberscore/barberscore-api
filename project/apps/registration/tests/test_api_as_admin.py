
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db



def test_assignment_endpoint(admin_api_client, assignment, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('assignment-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('assignment-detail', args=(str(assignment.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint(admin_api_client, contest, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('contest-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('contest-detail', args=(str(contest.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint(admin_api_client, entry, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('entry-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('entry-detail', args=(str(entry.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


# def test_repertory_endpoint(admin_api_client, repertory, django_assert_max_num_queries):
#     with django_assert_max_num_queries(10):
#         path = reverse('repertory-list')
#         response = admin_api_client.get(path)
#         assert response.status_code == status.HTTP_200_OK
#     with django_assert_max_num_queries(10):
#         path = reverse('repertory-detail', args=(str(repertory.id),))
#         response = admin_api_client.get(path)
#         assert response.status_code == status.HTTP_200_OK


def test_session_endpoint(admin_api_client, session, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('session-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('session-detail', args=(str(session.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
