
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_endpoint(user_api_client):
    path = reverse('api-root')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_endpoint(user_api_client, appearance):
    path = reverse('appearance-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_assignment_endpoint(user_api_client, assignment):
    path = reverse('assignment-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


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


def test_contest_endpoint(user_api_client, contest):
    path = reverse('contest-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('contest-detail', args=(str(contest.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_endpoint(user_api_client, contestant):
    path = reverse('contestant-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('contestant-detail', args=(str(contestant.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contender_endpoint(user_api_client, contender):
    path = reverse('contender-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('contender-detail', args=(str(contender.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint(user_api_client, convention):
    path = reverse('convention-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('convention-detail', args=(str(convention.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint(user_api_client, entry):
    path = reverse('entry-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('entry-detail', args=(str(entry.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


# def test_grid_endpoint(user_api_client, grid):
#     path = reverse('grid-list')
#     response = user_api_client.get(path)
#     assert response.status_code == status.HTTP_200_OK
#     path = reverse('grid-detail', args=(str(grid.id),))
#     response = user_api_client.get(path)
#     assert response.status_code == status.HTTP_200_OK


def test_group_endpoint(user_api_client, group):
    path = reverse('group-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('group-detail', args=(str(group.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_endpoint(user_api_client, member):
    path = reverse('member-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('member-detail', args=(str(member.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_endpoint(user_api_client, office):
    path = reverse('office-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('office-detail', args=(str(office.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint(user_api_client, officer):
    path = reverse('officer-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('officer-detail', args=(str(officer.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


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


def test_person_endpoint(user_api_client, person):
    path = reverse('person-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('person-detail', args=(str(person.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint(user_api_client, repertory):
    path = reverse('repertory-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


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


def test_session_endpoint(user_api_client, session):
    path = reverse('session-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('session-detail', args=(str(session.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_endpoint(user_api_client, song):
    path = reverse('song-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('song-detail', args=(str(song.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


# def test_venue_endpoint(user_api_client, venue):
#     path = reverse('venue-list')
#     response = user_api_client.get(path)
#     assert response.status_code == status.HTTP_200_OK
#     path = reverse('venue-detail', args=(str(venue.id),))
#     response = user_api_client.get(path)
#     assert response.status_code == status.HTTP_200_OK


def test_user_endpoint(user_api_client, user):
    path = reverse('user-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('user-detail', args=(str(user.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
