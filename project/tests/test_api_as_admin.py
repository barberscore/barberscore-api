
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_endpoint(admin_api_client, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('api-root')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_appearance_endpoint(admin_api_client, appearance, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('appearance-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('appearance-detail', args=(str(appearance.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_assignment_endpoint(admin_api_client, assignment, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('assignment-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('assignment-detail', args=(str(assignment.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


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


def test_competitor_endpoint(admin_api_client, competitor, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('competitor-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('competitor-detail', args=(str(competitor.id),))
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


def test_contestant_endpoint(admin_api_client, contestant, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('contestant-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('contestant-detail', args=(str(contestant.id),))
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


def test_entry_endpoint(admin_api_client, entry, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('entry-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('entry-detail', args=(str(entry.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_grid_endpoint(admin_api_client, grid, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('grid-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('grid-detail', args=(str(grid.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_group_endpoint(admin_api_client, group, django_assert_max_num_queries):
    with django_assert_max_num_queries(12):
        path = reverse('group-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('group-detail', args=(str(group.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_member_endpoint(admin_api_client, member, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('member-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('member-detail', args=(str(member.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_office_endpoint(admin_api_client, office, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('office-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('office-detail', args=(str(office.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint(admin_api_client, officer, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('officer-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('officer-detail', args=(str(officer.id),))
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


def test_person_endpoint(admin_api_client, person, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('person-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('person-detail', args=(str(person.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint(admin_api_client, repertory, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('repertory-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('repertory-detail', args=(str(repertory.id),))
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


def test_session_endpoint(admin_api_client, session, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('session-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('session-detail', args=(str(session.id),))
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


def test_venue_endpoint(admin_api_client, venue, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('venue-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('venue-detail', args=(str(venue.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_user_endpoint(admin_api_client, user, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('user-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('user-detail', args=(str(user.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
