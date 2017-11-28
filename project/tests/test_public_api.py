# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_endpoint(bhs_member):
    path = reverse('api-root')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_endpoint_list(bhs_member, appearance):
    path = reverse('appearance-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_endpoint_list(bhs_member, assignment):
    path = reverse('assignment-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_endpoint_list(bhs_member, award):
    path = reverse('award-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint_list(bhs_member, chart):
    path = reverse('chart-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint_list(bhs_member, contest):
    path = reverse('contest-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_endpoint_list(bhs_member, contestant):
    path = reverse('contestant-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint_list(bhs_member, convention):
    path = reverse('convention-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint_list(bhs_member, entry):
    path = reverse('entry-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_endpoint_list(bhs_member, competitor):
    path = reverse('competitor-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_endpoint_list(bhs_member, grantor):
    path = reverse('grantor-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_endpoint_list(bhs_member, group):
    path = reverse('group-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_endpoint_list(bhs_member, member):
    path = reverse('member-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_endpoint_list(bhs_member, office):
    path = reverse('office-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint_list(bhs_member, officer):
    path = reverse('officer-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_organization_endpoint_list(bhs_member, organization):
    path = reverse('organization-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_endpoint_list(bhs_member, panelist):
    path = reverse('panelist-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_endpoint_list(bhs_member, participant):
    path = reverse('participant-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint_list(bhs_member, person):
    path = reverse('person-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_endpoint_list(bhs_member, round):
    path = reverse('round-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint_list(bhs_member, repertory):
    path = reverse('repertory-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_score_endpoint_list(bhs_member, score):
    path = reverse('score-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_endpoint_list(bhs_member, session):
    path = reverse('session-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_endpoint_list(bhs_member, song):
    path = reverse('song-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_endpoint_list(bhs_member, venue):
    path = reverse('venue-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_endpoint_list(bhs_member, user):
    path = reverse('user-list')
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


# Detail Views

def test_appearance_endpoint_detail(bhs_member, appearance):
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_endpoint_detail(bhs_member, assignment):
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_endpoint_detail(bhs_member, award):
    path = reverse('award-detail', args=(str(award.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_endpoint_detail(bhs_member, chart):
    path = reverse('chart-detail', args=(str(chart.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_endpoint_detail(bhs_member, contest):
    path = reverse('contest-detail', args=(str(contest.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_endpoint_detail(bhs_member, contestant):
    path = reverse('contestant-detail', args=(str(contestant.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_endpoint_detail(bhs_member, convention):
    path = reverse('convention-detail', args=(str(convention.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_endpoint_detail(bhs_member, competitor):
    path = reverse('competitor-detail', args=(str(competitor.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_endpoint_detail(bhs_member, entry):
    path = reverse('entry-detail', args=(str(entry.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_endpoint_detail(bhs_member, grantor):
    path = reverse('grantor-detail', args=(str(grantor.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_endpoint_detail(bhs_member, group):
    path = reverse('group-detail', args=(str(group.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_endpoint_detail(bhs_member, member):
    path = reverse('member-detail', args=(str(member.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_endpoint_detail(bhs_member, office):
    path = reverse('office-detail', args=(str(office.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_endpoint_detail(bhs_member, officer):
    path = reverse('officer-detail', args=(str(officer.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_organization_endpoint_detail(bhs_member, organization):
    path = reverse('organization-detail', args=(str(organization.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_endpoint_detail(bhs_member, panelist):
    path = reverse('panelist-detail', args=(str(panelist.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_endpoint_detail(bhs_member, participant):
    path = reverse('participant-detail', args=(str(participant.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint_detail(bhs_member, person):
    path = reverse('person-detail', args=(str(person.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_endpoint_detail(bhs_member, repertory):
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_round_endpoint_detail(bhs_member, round):
    path = reverse('round-detail', args=(str(round.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_endpoint_detail(bhs_member, score):
    path = reverse('score-detail', args=(str(score.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_session_endpoint_detail(bhs_member, session):
    path = reverse('session-detail', args=(str(session.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_endpoint_detail(bhs_member, song):
    path = reverse('song-detail', args=(str(song.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_endpoint_detail(bhs_member, venue):
    path = reverse('venue-detail', args=(str(venue.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_endpoint_detail(bhs_member, user):
    path = reverse('user-detail', args=(str(user.id),))
    response = bhs_member.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN
