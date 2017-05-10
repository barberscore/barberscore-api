# Third-Party
import pytest
from rest_framework.test import APIClient

# Django
from django.apps import apps as api_apps
from django.test.client import Client
from django.urls import reverse

# First-Party
from api.factories import (
    AdminFactory,
    AssignmentFactory,
    AwardFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    DistrictFactory,
    MemberFactory,
    OfficeFactory,
    OfficerFactory,
    InternationalFactory,
    AppearanceFactory,
    EntryFactory,
    PersonFactory,
    QuartetFactory,
    RepertoryFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SlotFactory,
    SongFactory,
    SubmissionFactory,
    UserFactory,
    VenueFactory,
)

config = api_apps.get_app_config('api')


def ok(response):
    return response.status_code == 200


@pytest.fixture
def admin_client():
    admin = AdminFactory()
    client = Client()
    client.force_login(admin)
    return client


@pytest.fixture
def api_client():
    admin = AdminFactory()
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def assignment():
    return AssignmentFactory()


@pytest.fixture
def award():
    return AwardFactory()


@pytest.fixture
def chart():
    return ChartFactory()


@pytest.fixture
def contest():
    return ContestFactory()


@pytest.fixture
def contestant():
    return ContestantFactory()


@pytest.fixture
def convention():
    return ConventionFactory()


@pytest.fixture
def international():
    return InternationalFactory()


@pytest.fixture
def district():
    return DistrictFactory()


@pytest.fixture
def quartet():
    return QuartetFactory()


@pytest.fixture
def member():
    return MemberFactory()


@pytest.fixture
def office():
    return OfficeFactory()


@pytest.fixture
def officer():
    return OfficerFactory()


@pytest.fixture
def appearance():
    return AppearanceFactory()


@pytest.fixture
def entry():
    return EntryFactory()


@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def repertory():
    return RepertoryFactory()


@pytest.fixture
def round():
    return RoundFactory()


@pytest.fixture
def score():
    return ScoreFactory()


@pytest.fixture
def session():
    return SessionFactory()


@pytest.fixture
def slot():
    return SlotFactory()


@pytest.fixture
def song():
    return SongFactory()


@pytest.fixture
def submission():
    return SubmissionFactory()


@pytest.fixture
def venue():
    return VenueFactory()


@pytest.fixture
def user():
    return UserFactory()

def test_tautologic():
    assert True


@pytest.mark.django_db()
def test_api_endpoint(api_client):
    path = reverse('api-root')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_assignment_endpoint_list(api_client, assignment):
    path = reverse('assignment-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_award_endpoint_list(api_client, award):
    path = reverse('award-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_chart_endpoint_list(api_client, chart):
    path = reverse('chart-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_endpoint_list(api_client, contest):
    path = reverse('contest-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestant_endpoint_list(api_client, contestant):
    path = reverse('contestant-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_convention_endpoint_list(api_client, convention):
    path = reverse('convention-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_endpoint_list(api_client, international):
    path = reverse('entity-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_member_endpoint_list(api_client, member):
    path = reverse('member-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_office_endpoint_list(api_client, office):
    path = reverse('office-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_officer_endpoint_list(api_client, officer):
    path = reverse('officer-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_appearance_endpoint_list(api_client, appearance):
    path = reverse('appearance-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entry_endpoint_list(api_client, entry):
    path = reverse('entry-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_person_endpoint_list(api_client, person):
    path = reverse('person-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_endpoint_list(api_client, round):
    path = reverse('round-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_repertory_endpoint_list(api_client, repertory):
    path = reverse('repertory-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_endpoint_list(api_client, score):
    path = reverse('score-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_endpoint_list(api_client, session):
    path = reverse('session-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_endpoint_list(api_client, slot):
    path = reverse('slot-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_endpoint_list(api_client, song):
    path = reverse('song-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_submission_endpoint_list(api_client, submission):
    path = reverse('submission-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_endpoint_list(api_client, venue):
    path = reverse('venue-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_endpoint_list(api_client, user):
    path = reverse('user-list')
    response = api_client.get(path)
    assert ok(response)


# Detail Views

@pytest.mark.django_db()
def test_assignment_endpoint_detail(api_client, assignment):
    path = reverse('assignment-detail', args=(str(assignment.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_award_endpoint_detail(api_client, award):
    path = reverse('award-detail', args=(str(award.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_chart_endpoint_detail(api_client, chart):
    path = reverse('chart-detail', args=(str(chart.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_endpoint_detail(api_client, contest):
    path = reverse('contest-detail', args=(str(contest.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestant_endpoint_detail(api_client, contestant):
    path = reverse('contestant-detail', args=(str(contestant.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_convention_endpoint_detail(api_client, convention):
    path = reverse('convention-detail', args=(str(convention.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_endpoint_detail(api_client, international):
    path = reverse('entity-detail', args=(str(international.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_member_endpoint_detail(api_client, member):
    path = reverse('member-detail', args=(str(member.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_office_endpoint_detail(api_client, office):
    path = reverse('office-detail', args=(str(office.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_officer_endpoint_detail(api_client, officer):
    path = reverse('officer-detail', args=(str(officer.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_appearance_endpoint_detail(api_client, appearance):
    path = reverse('appearance-detail', args=(str(appearance.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entry_endpoint_detail(api_client, entry):
    path = reverse('entry-detail', args=(str(entry.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_person_endpoint_detail(api_client, person):
    path = reverse('person-detail', args=(str(person.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_repertory_endpoint_detail(api_client, repertory):
    path = reverse('repertory-detail', args=(str(repertory.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_endpoint_detail(api_client, round):
    path = reverse('round-detail', args=(str(round.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_endpoint_detail(api_client, score):
    path = reverse('score-detail', args=(str(score.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_endpoint_detail(api_client, session):
    path = reverse('session-detail', args=(str(session.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_endpoint_detail(api_client, slot):
    path = reverse('slot-detail', args=(str(slot.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_endpoint_detail(api_client, song):
    path = reverse('song-detail', args=(str(song.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_submission_endpoint_detail(api_client, submission):
    path = reverse('submission-detail', args=(str(submission.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_endpoint_detail(api_client, venue):
    path = reverse('venue-detail', args=(str(venue.id),))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_endpoint_detail(api_client, user):
    path = reverse('user-detail', args=(str(user.id),))
    response = api_client.get(path)
    assert ok(response)


# Admin Views

@pytest.mark.django_db()
def test_api_admin(admin_client):
    path = reverse('admin:index')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_assignment_admin_list(admin_client, assignment):
    path = reverse('admin:app_assignment_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_award_admin_list(admin_client, award):
    path = reverse('admin:app_award_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_chart_admin_list(admin_client, chart):
    path = reverse('admin:app_chart_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_admin_list(admin_client, contest):
    path = reverse('admin:app_contest_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestant_admin_list(admin_client, contestant):
    path = reverse('admin:app_contestant_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_convention_admin_list(admin_client, convention):
    path = reverse('admin:app_convention_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_admin_list(admin_client, international):
    path = reverse('admin:app_entity_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_member_admin_list(admin_client, member):
    path = reverse('admin:app_member_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_office_admin_list(admin_client, office):
    path = reverse('admin:app_office_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_officer_admin_list(admin_client, officer):
    path = reverse('admin:app_officer_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_appearance_admin_list(admin_client, appearance):
    path = reverse('admin:app_appearance_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entry_admin_list(admin_client, entry):
    path = reverse('admin:app_entry_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_person_admin_list(admin_client, person):
    path = reverse('admin:app_person_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_repertory_admin_list(admin_client, repertory):
    path = reverse('admin:app_repertory_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_admin_list(admin_client, round):
    path = reverse('admin:app_round_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_admin_list(admin_client, score):
    path = reverse('admin:app_score_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_admin_list(admin_client, session):
    path = reverse('admin:app_session_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_admin_list(admin_client, slot):
    path = reverse('admin:app_slot_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_admin_list(admin_client, song):
    path = reverse('admin:app_song_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_submission_admin_list(admin_client, submission):
    path = reverse('admin:app_submission_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_admin_list(admin_client, venue):
    path = reverse('admin:app_venue_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_admin_list(admin_client, user):
    path = reverse('admin:app_user_changelist')
    response = admin_client.get(path)
    assert ok(response)


# Detail Views

@pytest.mark.django_db()
def test_assignment_admin_detail(admin_client, assignment):
    path = reverse('admin:app_assignment_change', args=(str(assignment.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_award_admin_detail(admin_client, award):
    path = reverse('admin:app_award_change', args=(str(award.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_chart_admin_detail(admin_client, chart):
    path = reverse('admin:app_chart_change', args=(str(chart.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_admin_detail(admin_client, contest):
    path = reverse('admin:app_contest_change', args=(str(contest.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestant_admin_detail(admin_client, contestant):
    path = reverse('admin:app_contestant_change', args=(str(contestant.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_convention_admin_detail(admin_client, convention):
    path = reverse('admin:app_convention_change', args=(str(convention.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_admin_detail(admin_client, international):
    path = reverse('admin:app_entity_change', args=(str(international.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_member_admin_detail(admin_client, member):
    path = reverse('admin:app_member_change', args=(str(member.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_office_admin_detail(admin_client, office):
    path = reverse('admin:app_office_change', args=(str(office.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_officer_admin_detail(admin_client, officer):
    path = reverse('admin:app_officer_change', args=(str(officer.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_appearance_admin_detail(admin_client, appearance):
    path = reverse('admin:app_appearance_change', args=(str(appearance.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entry_admin_detail(admin_client, entry):
    path = reverse('admin:app_entry_change', args=(str(entry.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_person_admin_detail(admin_client, person):
    path = reverse('admin:app_person_change', args=(str(person.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_repertory_admin_detail(admin_client, repertory):
    path = reverse('admin:app_repertory_change', args=(str(repertory.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_admin_detail(admin_client, round):
    path = reverse('admin:app_round_change', args=(str(round.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_admin_detail(admin_client, score):
    path = reverse('admin:app_score_change', args=(str(score.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_admin_detail(admin_client, session):
    path = reverse('admin:app_session_change', args=(str(session.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_admin_detail(admin_client, slot):
    path = reverse('admin:app_slot_change', args=(str(slot.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_admin_detail(admin_client, song):
    path = reverse('admin:app_song_change', args=(str(song.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_submission_admin_detail(admin_client, submission):
    path = reverse('admin:app_submission_change', args=(str(submission.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_admin_detail(admin_client, venue):
    path = reverse('admin:app_venue_change', args=(str(venue.id),))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_admin_detail(admin_client, user):
    path = reverse('admin:app_user_change', args=(str(user.id),))
    response = admin_client.get(path)
    assert ok(response)
