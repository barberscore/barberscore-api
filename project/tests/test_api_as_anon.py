# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_endpoint(anon_api_client):
    path = reverse('api-root')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_endpoint_list(anon_api_client, appearance):
    path = reverse('appearance-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_assignment_endpoint_list(anon_api_client, assignment):
    path = reverse('assignment-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_award_endpoint_list(anon_api_client, award):
    path = reverse('award-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_chart_endpoint_list(anon_api_client, chart):
    path = reverse('chart-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_competitor_endpoint_list(anon_api_client, competitor):
    path = reverse('competitor-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contest_endpoint_list(anon_api_client, contest):
    path = reverse('contest-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contestant_endpoint_list(anon_api_client, contestant):
    path = reverse('contestant-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_convention_endpoint_list(anon_api_client, convention):
    path = reverse('convention-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_entry_endpoint_list(anon_api_client, entry):
    path = reverse('entry-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_grantor_endpoint_list(anon_api_client, grantor):
    path = reverse('grantor-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_grid_endpoint_list(anon_api_client, grid):
    path = reverse('grid-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_group_endpoint_list(anon_api_client, group):
    path = reverse('group-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_member_endpoint_list(anon_api_client, member):
    path = reverse('member-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_office_endpoint_list(anon_api_client, office):
    path = reverse('office-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_officer_endpoint_list(anon_api_client, officer):
    path = reverse('officer-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_panelist_endpoint_list(anon_api_client, panelist):
    path = reverse('panelist-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_person_endpoint_list(anon_api_client, person):
    path = reverse('person-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_repertory_endpoint_list(anon_api_client, repertory):
    path = reverse('repertory-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_round_endpoint_list(anon_api_client, round):
    path = reverse('round-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_score_endpoint_list(anon_api_client, score):
    path = reverse('score-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_session_endpoint_list(anon_api_client, session):
    path = reverse('session-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_song_endpoint_list(anon_api_client, song):
    path = reverse('song-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_venue_endpoint_list(anon_api_client, venue):
    path = reverse('venue-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_endpoint_list(anon_api_client, user):
    path = reverse('user-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Detail Views

def test_appearance_endpoint_detail(anon_api_client, appearance):
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_assignment_endpoint_detail(anon_api_client, assignment):
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_award_endpoint_detail(anon_api_client, award):
    path = reverse('award-detail', args=(str(award.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_chart_endpoint_detail(anon_api_client, chart):
    path = reverse('chart-detail', args=(str(chart.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_competitor_endpoint_detail(anon_api_client, competitor):
    path = reverse('competitor-detail', args=(str(competitor.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contest_endpoint_detail(anon_api_client, contest):
    path = reverse('contest-detail', args=(str(contest.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contestant_endpoint_detail(anon_api_client, contestant):
    path = reverse('contestant-detail', args=(str(contestant.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_convention_endpoint_detail(anon_api_client, convention):
    path = reverse('convention-detail', args=(str(convention.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_entry_endpoint_detail(anon_api_client, entry):
    path = reverse('entry-detail', args=(str(entry.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_grantor_endpoint_detail(anon_api_client, grantor):
    path = reverse('grantor-detail', args=(str(grantor.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_grid_endpoint_detail(anon_api_client, grid):
    path = reverse('grid-detail', args=(str(grid.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_group_endpoint_detail(anon_api_client, group):
    path = reverse('group-detail', args=(str(group.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_member_endpoint_detail(anon_api_client, member):
    path = reverse('member-detail', args=(str(member.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_office_endpoint_detail(anon_api_client, office):
    path = reverse('office-detail', args=(str(office.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_officer_endpoint_detail(anon_api_client, officer):
    path = reverse('officer-detail', args=(str(officer.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_panelist_endpoint_detail(anon_api_client, panelist):
    path = reverse('panelist-detail', args=(str(panelist.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_person_endpoint_detail(anon_api_client, person):
    path = reverse('person-detail', args=(str(person.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_repertory_endpoint_detail(anon_api_client, repertory):
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_round_endpoint_detail(anon_api_client, round):
    path = reverse('round-detail', args=(str(round.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_score_endpoint_detail(anon_api_client, score):
    path = reverse('score-detail', args=(str(score.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_session_endpoint_detail(anon_api_client, session):
    path = reverse('session-detail', args=(str(session.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_song_endpoint_detail(anon_api_client, song):
    path = reverse('song-detail', args=(str(song.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_venue_endpoint_detail(anon_api_client, venue):
    path = reverse('venue-detail', args=(str(venue.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_endpoint_detail(anon_api_client, user):
    path = reverse('user-detail', args=(str(user.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
