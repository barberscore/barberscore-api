# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_admin(admin_django_client):
    path = reverse('admin:index')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_admin_list(admin_django_client, appearance):
    path = reverse('admin:api_appearance_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_admin_list(admin_django_client, assignment):
    path = reverse('admin:api_assignment_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_admin_list(admin_django_client, award):
    path = reverse('admin:api_award_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_admin_list(admin_django_client, chart):
    path = reverse('admin:api_chart_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_admin_list(admin_django_client, contest):
    path = reverse('admin:api_contest_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_admin_list(admin_django_client, contestant):
    path = reverse('admin:api_contestant_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_admin_list(admin_django_client, convention):
    path = reverse('admin:api_convention_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_admin_list(admin_django_client, competitor):
    path = reverse('admin:api_competitor_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_admin_list(admin_django_client, entry):
    path = reverse('admin:api_entry_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_admin_list(admin_django_client, grantor):
    path = reverse('admin:api_grantor_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grid_admin_list(admin_django_client, grid):
    path = reverse('admin:api_grid_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_admin_list(admin_django_client, group):
    path = reverse('admin:api_group_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_admin_list(admin_django_client, member):
    path = reverse('admin:api_member_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_admin_list(admin_django_client, office):
    path = reverse('admin:api_office_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_admin_list(admin_django_client, officer):
    path = reverse('admin:api_officer_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_organization_admin_list(admin_django_client, organization):
    path = reverse('admin:api_organization_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_admin_list(admin_django_client, panelist):
    path = reverse('admin:api_panelist_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_admin_list(admin_django_client, participant):
    path = reverse('admin:api_participant_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_admin_list(admin_django_client, person):
    path = reverse('admin:api_person_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_admin_list(admin_django_client, repertory):
    path = reverse('admin:api_repertory_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_admin_list(admin_django_client, round):
    path = reverse('admin:api_round_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_admin_list(admin_django_client, score):
    path = reverse('admin:api_score_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_admin_list(admin_django_client, session):
    path = reverse('admin:api_session_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_admin_list(admin_django_client, song):
    path = reverse('admin:api_song_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_admin_list(admin_django_client, venue):
    path = reverse('admin:api_venue_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_admin_list(admin_django_client, user):
    path = reverse('admin:api_user_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_admin_detail(admin_django_client, appearance):
    path = reverse('admin:api_appearance_change', args=(str(appearance.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_admin_detail(admin_django_client, assignment):
    path = reverse('admin:api_assignment_change', args=(str(assignment.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_admin_detail(admin_django_client, award):
    path = reverse('admin:api_award_change', args=(str(award.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_admin_detail(admin_django_client, chart):
    path = reverse('admin:api_chart_change', args=(str(chart.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_admin_detail(admin_django_client, contest):
    path = reverse('admin:api_contest_change', args=(str(contest.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_admin_detail(admin_django_client, contestant):
    path = reverse('admin:api_contestant_change', args=(str(contestant.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_admin_detail(admin_django_client, convention):
    path = reverse('admin:api_convention_change', args=(str(convention.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_competitor_admin_detail(admin_django_client, competitor):
    path = reverse('admin:api_competitor_change', args=(str(competitor.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_admin_detail(admin_django_client, entry):
    path = reverse('admin:api_entry_change', args=(str(entry.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grantor_admin_detail(admin_django_client, grantor):
    path = reverse('admin:api_grantor_change', args=(str(grantor.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_grid_admin_detail(admin_django_client, grid):
    path = reverse('admin:api_grid_change', args=(str(grid.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_admin_detail(admin_django_client, group):
    path = reverse('admin:api_group_change', args=(str(group.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_admin_detail(admin_django_client, member):
    path = reverse('admin:api_member_change', args=(str(member.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_admin_detail(admin_django_client, office):
    path = reverse('admin:api_office_change', args=(str(office.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_admin_detail(admin_django_client, officer):
    path = reverse('admin:api_officer_change', args=(str(officer.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_organization_admin_detail(admin_django_client, organization):
    path = reverse('admin:api_organization_change', args=(str(organization.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_admin_detail(admin_django_client, panelist):
    path = reverse('admin:api_panelist_change', args=(str(panelist.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_admin_detail(admin_django_client, participant):
    path = reverse('admin:api_participant_change', args=(str(participant.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_admin_detail(admin_django_client, person):
    path = reverse('admin:api_person_change', args=(str(person.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_admin_detail(admin_django_client, repertory):
    path = reverse('admin:api_repertory_change', args=(str(repertory.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_admin_detail(admin_django_client, round):
    path = reverse('admin:api_round_change', args=(str(round.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_admin_detail(admin_django_client, score):
    path = reverse('admin:api_score_change', args=(str(score.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_admin_detail(admin_django_client, session):
    path = reverse('admin:api_session_change', args=(str(session.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_admin_detail(admin_django_client, song):
    path = reverse('admin:api_song_change', args=(str(song.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_admin_detail(admin_django_client, venue):
    path = reverse('admin:api_venue_change', args=(str(venue.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_admin_detail(admin_django_client, user):
    path = reverse('admin:api_user_change', args=(str(user.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
