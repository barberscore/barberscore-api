
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


def test_assignment_endpoint(anon_api_client, assignment):
    # List
    path = reverse('assignment-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Detail
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Actions
    path = reverse('assignment-activate', args=(str(assignment.id),))
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('assignment-deactivate', args=(str(assignment.id),))
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_award_endpoint(anon_api_client, award):
    path = reverse('award-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('award-detail', args=(str(award.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_chart_endpoint(anon_api_client, chart):
    # List
    path = reverse('chart-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Detail
    path = reverse('chart-detail', args=(str(chart.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contest_endpoint(anon_api_client, contest):
    path = reverse('contest-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('contest-detail', args=(str(contest.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contestant_endpoint(anon_api_client, contestant):
    path = reverse('contestant-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('contestant-detail', args=(str(contestant.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_contender_endpoint(anon_api_client, contender):
    path = reverse('contender-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('contender-detail', args=(str(contender.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_convention_endpoint(anon_api_client, convention):
    path = reverse('convention-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('convention-detail', args=(str(convention.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_entry_endpoint(anon_api_client, entry):
    path = reverse('entry-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('entry-detail', args=(str(entry.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_grid_endpoint(anon_api_client, grid):
    path = reverse('grid-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('grid-detail', args=(str(grid.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_group_endpoint(anon_api_client, group):
    path = reverse('group-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('group-detail', args=(str(group.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_member_endpoint(anon_api_client, member):
    path = reverse('member-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('member-detail', args=(str(member.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_office_endpoint(anon_api_client, office):
    path = reverse('office-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('office-detail', args=(str(office.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_officer_endpoint(anon_api_client, officer):
    path = reverse('officer-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('officer-detail', args=(str(officer.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
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


def test_person_endpoint(anon_api_client, person):
    path = reverse('person-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('person-detail', args=(str(person.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_repertory_endpoint(anon_api_client, repertory):
    path = reverse('repertory-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('repertory-detail', args=(str(repertory.id),))
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


def test_session_endpoint(anon_api_client, session):
    path = reverse('session-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('session-detail', args=(str(session.id),))
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


def test_venue_endpoint(anon_api_client, venue):
    path = reverse('venue-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('venue-detail', args=(str(venue.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_endpoint(anon_api_client, user):
    path = reverse('user-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('user-detail', args=(str(user.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
