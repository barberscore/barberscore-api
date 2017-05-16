# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse
pytestmark = pytest.mark.django_db


def test_api_admin(admin_client):
    path = reverse('admin:index')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_admin_list(admin_client, user_client, appearance):
    path = reverse('admin:api_appearance_changelist')
    response = admin_client.get(path)
    u_response = user_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    assert u_response.status_code == status.HTTP_302_FOUND


def test_assignment_admin_list(admin_client, assignment):
    path = reverse('admin:api_assignment_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_admin_list(admin_client, award):
    path = reverse('admin:api_award_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_admin_list(admin_client, chart):
    path = reverse('admin:api_chart_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_admin_list(admin_client, contest):
    path = reverse('admin:api_contest_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_admin_list(admin_client, contestant):
    path = reverse('admin:api_contestant_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_admin_list(admin_client, convention):
    path = reverse('admin:api_convention_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entity_admin_list(admin_client, entity):
    path = reverse('admin:api_entity_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_admin_list(admin_client, entry):
    path = reverse('admin:api_entry_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_admin_list(admin_client, member):
    path = reverse('admin:api_member_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_admin_list(admin_client, office):
    path = reverse('admin:api_office_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_admin_list(admin_client, officer):
    path = reverse('admin:api_officer_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_admin_list(admin_client, participant):
    path = reverse('admin:api_participant_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_admin_list(admin_client, person):
    path = reverse('admin:api_person_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_admin_list(admin_client, repertory):
    path = reverse('admin:api_repertory_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_admin_list(admin_client, round):
    path = reverse('admin:api_round_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_admin_list(admin_client, score):
    path = reverse('admin:api_score_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_admin_list(admin_client, session):
    path = reverse('admin:api_session_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_slot_admin_list(admin_client, slot):
    path = reverse('admin:api_slot_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_admin_list(admin_client, song):
    path = reverse('admin:api_song_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_submission_admin_list(admin_client, submission):
    path = reverse('admin:api_submission_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_admin_list(admin_client, venue):
    path = reverse('admin:api_venue_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_admin_list(admin_client, user):
    path = reverse('admin:api_user_changelist')
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_appearance_admin_detail(admin_client, appearance):
    path = reverse('admin:api_appearance_change', args=(str(appearance.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_admin_detail(admin_client, assignment):
    path = reverse('admin:api_assignment_change', args=(str(assignment.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_admin_detail(admin_client, award):
    path = reverse('admin:api_award_change', args=(str(award.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_admin_detail(admin_client, chart):
    path = reverse('admin:api_chart_change', args=(str(chart.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_admin_detail(admin_client, contest):
    path = reverse('admin:api_contest_change', args=(str(contest.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_admin_detail(admin_client, contestant):
    path = reverse('admin:api_contestant_change', args=(str(contestant.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_admin_detail(admin_client, convention):
    path = reverse('admin:api_convention_change', args=(str(convention.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entity_admin_detail(admin_client, entity):
    path = reverse('admin:api_entity_change', args=(str(entity.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_admin_detail(admin_client, entry):
    path = reverse('admin:api_entry_change', args=(str(entry.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_admin_detail(admin_client, member):
    path = reverse('admin:api_member_change', args=(str(member.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_office_admin_detail(admin_client, office):
    path = reverse('admin:api_office_change', args=(str(office.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_admin_detail(admin_client, officer):
    path = reverse('admin:api_officer_change', args=(str(officer.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_participant_admin_detail(admin_client, participant):
    path = reverse('admin:api_participant_change', args=(str(participant.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_admin_detail(admin_client, person):
    path = reverse('admin:api_person_change', args=(str(person.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_admin_detail(admin_client, repertory):
    path = reverse('admin:api_repertory_change', args=(str(repertory.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_admin_detail(admin_client, round):
    path = reverse('admin:api_round_change', args=(str(round.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_admin_detail(admin_client, score):
    path = reverse('admin:api_score_change', args=(str(score.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_admin_detail(admin_client, session):
    path = reverse('admin:api_session_change', args=(str(session.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_slot_admin_detail(admin_client, slot):
    path = reverse('admin:api_slot_change', args=(str(slot.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_admin_detail(admin_client, song):
    path = reverse('admin:api_song_change', args=(str(song.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_submission_admin_detail(admin_client, submission):
    path = reverse('admin:api_submission_change', args=(str(submission.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_venue_admin_detail(admin_client, venue):
    path = reverse('admin:api_venue_change', args=(str(venue.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_admin_detail(admin_client, user):
    path = reverse('admin:api_user_change', args=(str(user.id),))
    response = admin_client.get(path)
    assert response.status_code == status.HTTP_200_OK
