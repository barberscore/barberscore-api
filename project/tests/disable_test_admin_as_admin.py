
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


def test_appearance_admin(admin_django_client, appearance):
    path = reverse('admin:rmanager_appearance_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:rmanager_appearance_change', args=(str(appearance.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_assignment_admin(admin_django_client, assignment):
    path = reverse('admin:cmanager_assignment_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:cmanager_assignment_change', args=(str(assignment.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_award_admin(admin_django_client, award):
    path = reverse('admin:cmanager_award_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:cmanager_award_change', args=(str(award.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_chart_admin(admin_django_client, chart):
    path = reverse('admin:bhs_chart_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_chart_change', args=(str(chart.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contest_admin(admin_django_client, contest):
    path = reverse('admin:smanager_contest_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:smanager_contest_change', args=(str(contest.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contestant_admin(admin_django_client, contestant):
    path = reverse('admin:smanager_contestant_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:smanager_contestant_change', args=(str(contestant.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_contender_admin(admin_django_client, contender):
    path = reverse('admin:rmanager_contender_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:rmanager_contender_change', args=(str(contender.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_convention_admin(admin_django_client, convention):
    path = reverse('admin:cmanager_convention_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:cmanager_convention_change', args=(str(convention.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_entry_admin(admin_django_client, entry):
    path = reverse('admin:smanager_entry_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:smanager_entry_change', args=(str(entry.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_admin(admin_django_client, group):
    path = reverse('admin:bhs_group_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_group_change', args=(str(group.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_member_admin(admin_django_client, member):
    path = reverse('admin:bhs_member_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_member_change', args=(str(member.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_officer_admin(admin_django_client, officer):
    path = reverse('admin:bhs_officer_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_officer_change', args=(str(officer.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_outcome_admin(admin_django_client, outcome):
    path = reverse('admin:rmanager_outcome_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:rmanager_outcome_change', args=(str(outcome.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_panelist_admin(admin_django_client, panelist):
    path = reverse('admin:rmanager_panelist_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:rmanager_panelist_change', args=(str(panelist.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_admin(admin_django_client, person):
    path = reverse('admin:bhs_person_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_person_change', args=(str(person.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_repertory_admin(admin_django_client, repertory):
    path = reverse('admin:bhs_repertory_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_repertory_change', args=(str(repertory.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_round_admin(admin_django_client, round):
    # path = reverse('admin:rmanager_round_changelist')
    # response = admin_django_client.get(path)
    # assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:rmanager_round_change', args=(str(round.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_score_admin(admin_django_client, score):
    path = reverse('admin:rmanager_score_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:rmanager_score_change', args=(str(score.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_session_admin(admin_django_client, session):
    path = reverse('admin:smanager_session_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:smanager_session_change', args=(str(session.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_song_admin(admin_django_client, song):
    path = reverse('admin:rmanager_song_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:rmanager_song_change', args=(str(song.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_user_admin(admin_django_client, user):
    path = reverse('admin:api_user_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:api_user_change', args=(str(user.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
