# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_endpoint(api_client):
    path = reverse('api-root')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_endpoint_list(api_client, appearance):
    path = reverse('appearance-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_endpoint_list(api_client, assignment):
    path = reverse('assignment-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_endpoint_list(api_client, award):
    path = reverse('award-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint_list(api_client, chart):
    path = reverse('chart-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint_list(api_client, contest):
    path = reverse('contest-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_endpoint_list(api_client, contestant):
    path = reverse('contestant-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint_list(api_client, convention):
    path = reverse('convention-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_endpoint_list(api_client, competitor):
    path = reverse('competitor-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint_list(api_client, entry):
    path = reverse('entry-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_endpoint_list(api_client, grantor):
    path = reverse('grantor-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_endpoint_list(api_client, group):
    path = reverse('group-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_endpoint_list(api_client, member):
    path = reverse('member-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_endpoint_list(api_client, office):
    path = reverse('office-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint_list(api_client, officer):
    path = reverse('officer-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_organization_endpoint_list(api_client, organization):
    path = reverse('organization-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_endpoint_list(api_client, panelist):
    path = reverse('panelist-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_endpoint_list(api_client, participant):
    path = reverse('participant-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint_list(api_client, person):
    path = reverse('person-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_endpoint_list(api_client, round):
    path = reverse('round-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint_list(api_client, repertory):
    path = reverse('repertory-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_endpoint_list(api_client, score):
    path = reverse('score-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_endpoint_list(api_client, session):
    path = reverse('session-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_slot_endpoint_list(api_client, slot):
    path = reverse('slot-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_endpoint_list(api_client, song):
    path = reverse('song-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_endpoint_list(api_client, venue):
    path = reverse('venue-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_endpoint_list(api_client, user):
    path = reverse('user-list')
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


# Detail Views

def test_appearance_endpoint_detail(api_client, appearance):
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_endpoint_detail(api_client, assignment):
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_endpoint_detail(api_client, award):
    path = reverse('award-detail', args=(str(award.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint_detail(api_client, chart):
    path = reverse('chart-detail', args=(str(chart.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint_detail(api_client, contest):
    path = reverse('contest-detail', args=(str(contest.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_endpoint_detail(api_client, contestant):
    path = reverse('contestant-detail', args=(str(contestant.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint_detail(api_client, convention):
    path = reverse('convention-detail', args=(str(convention.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_endpoint_detail(api_client, competitor):
    path = reverse('competitor-detail', args=(str(competitor.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint_detail(api_client, entry):
    path = reverse('entry-detail', args=(str(entry.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_endpoint_detail(api_client, grantor):
    path = reverse('grantor-detail', args=(str(grantor.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_endpoint_detail(api_client, group):
    path = reverse('group-detail', args=(str(group.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_endpoint_detail(api_client, member):
    path = reverse('member-detail', args=(str(member.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_endpoint_detail(api_client, office):
    path = reverse('office-detail', args=(str(office.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint_detail(api_client, officer):
    path = reverse('officer-detail', args=(str(officer.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_organization_endpoint_detail(api_client, organization):
    path = reverse('organization-detail', args=(str(organization.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_endpoint_detail(api_client, panelist):
    path = reverse('panelist-detail', args=(str(panelist.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_endpoint_detail(api_client, participant):
    path = reverse('participant-detail', args=(str(participant.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint_detail(api_client, person):
    path = reverse('person-detail', args=(str(person.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint_detail(api_client, repertory):
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_endpoint_detail(api_client, round):
    path = reverse('round-detail', args=(str(round.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_endpoint_detail(api_client, score):
    path = reverse('score-detail', args=(str(score.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_endpoint_detail(api_client, session):
    path = reverse('session-detail', args=(str(session.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_slot_endpoint_detail(api_client, slot):
    path = reverse('slot-detail', args=(str(slot.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_endpoint_detail(api_client, song):
    path = reverse('song-detail', args=(str(song.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_endpoint_detail(api_client, venue):
    path = reverse('venue-detail', args=(str(venue.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_endpoint_detail(api_client, user):
    path = reverse('user-detail', args=(str(user.id),))
    response = api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
