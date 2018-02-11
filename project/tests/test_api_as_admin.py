# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_endpoint(admin_api_client):
    path = reverse('api-root')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_endpoint_list(admin_api_client, appearance):
    path = reverse('appearance-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_endpoint_list(admin_api_client, assignment):
    path = reverse('assignment-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_endpoint_list(admin_api_client, award):
    path = reverse('award-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint_list(admin_api_client, chart):
    path = reverse('chart-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_endpoint_list(admin_api_client, competitor):
    path = reverse('competitor-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint_list(admin_api_client, contest):
    path = reverse('contest-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_endpoint_list(admin_api_client, contestant):
    path = reverse('contestant-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint_list(admin_api_client, convention):
    path = reverse('convention-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint_list(admin_api_client, entry):
    path = reverse('entry-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_endpoint_list(admin_api_client, grantor):
    path = reverse('grantor-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grid_endpoint_list(admin_api_client, grid):
    path = reverse('grid-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_endpoint_list(admin_api_client, group):
    path = reverse('group-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_endpoint_list(admin_api_client, member):
    path = reverse('member-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_endpoint_list(admin_api_client, office):
    path = reverse('office-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint_list(admin_api_client, officer):
    path = reverse('officer-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_endpoint_list(admin_api_client, panelist):
    path = reverse('panelist-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint_list(admin_api_client, person):
    path = reverse('person-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint_list(admin_api_client, repertory):
    path = reverse('repertory-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_endpoint_list(admin_api_client, round):
    path = reverse('round-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_endpoint_list(admin_api_client, score):
    path = reverse('score-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_endpoint_list(admin_api_client, session):
    path = reverse('session-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_endpoint_list(admin_api_client, song):
    path = reverse('song-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_endpoint_list(admin_api_client, venue):
    path = reverse('venue-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_endpoint_list(admin_api_client, user):
    path = reverse('user-list')
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


# Detail Views

def test_appearance_endpoint_detail(admin_api_client, appearance):
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_endpoint_detail(admin_api_client, assignment):
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_endpoint_detail(admin_api_client, award):
    path = reverse('award-detail', args=(str(award.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint_detail(admin_api_client, chart):
    path = reverse('chart-detail', args=(str(chart.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_endpoint_detail(admin_api_client, competitor):
    path = reverse('competitor-detail', args=(str(competitor.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint_detail(admin_api_client, contest):
    path = reverse('contest-detail', args=(str(contest.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_endpoint_detail(admin_api_client, contestant):
    path = reverse('contestant-detail', args=(str(contestant.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint_detail(admin_api_client, convention):
    path = reverse('convention-detail', args=(str(convention.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint_detail(admin_api_client, entry):
    path = reverse('entry-detail', args=(str(entry.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_endpoint_detail(admin_api_client, grantor):
    path = reverse('grantor-detail', args=(str(grantor.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grid_endpoint_detail(admin_api_client, grid):
    path = reverse('grid-detail', args=(str(grid.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_endpoint_detail(admin_api_client, group):
    path = reverse('group-detail', args=(str(group.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_endpoint_detail(admin_api_client, member):
    path = reverse('member-detail', args=(str(member.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_endpoint_detail(admin_api_client, office):
    path = reverse('office-detail', args=(str(office.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint_detail(admin_api_client, officer):
    path = reverse('officer-detail', args=(str(officer.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_endpoint_detail(admin_api_client, panelist):
    path = reverse('panelist-detail', args=(str(panelist.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint_detail(admin_api_client, person):
    path = reverse('person-detail', args=(str(person.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint_detail(admin_api_client, repertory):
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_endpoint_detail(admin_api_client, round):
    path = reverse('round-detail', args=(str(round.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_endpoint_detail(admin_api_client, score):
    path = reverse('score-detail', args=(str(score.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_endpoint_detail(admin_api_client, session):
    path = reverse('session-detail', args=(str(session.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_endpoint_detail(admin_api_client, song):
    path = reverse('song-detail', args=(str(song.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_endpoint_detail(admin_api_client, venue):
    path = reverse('venue-detail', args=(str(venue.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_endpoint_detail(admin_api_client, user):
    path = reverse('user-detail', args=(str(user.id),))
    response = admin_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
