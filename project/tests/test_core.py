# Third-Party
import pytest
from rest_framework.test import APIClient

# Django
from django.apps import apps as api_apps
from django.test.client import Client
from django.urls import reverse

# First-Party
from app.factories import (
    AdminFactory,
    AssignmentFactory,
    AwardFactory,
    CatalogFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    DistrictFactory,
    HostFactory,
    MembershipFactory,
    OfficeFactory,
    OfficerFactory,
    OrganizationFactory,
    PerformanceFactory,
    PerformerFactory,
    PersonFactory,
    QuartetFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SlotFactory,
    SongFactory,
    SubmissionFactory,
    UserFactory,
    VenueFactory,
)

config = api_apps.get_app_config('app')


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
def catalog():
    return CatalogFactory()


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
def host():
    return HostFactory()


@pytest.fixture
def organization():
    return OrganizationFactory()


@pytest.fixture
def district():
    return DistrictFactory()


@pytest.fixture
def quartet():
    return QuartetFactory()


@pytest.fixture
def membership():
    return MembershipFactory()


@pytest.fixture
def office():
    return OfficeFactory()


@pytest.fixture
def officer():
    return OfficerFactory()


@pytest.fixture
def performance():
    return PerformanceFactory()


@pytest.fixture
def performer():
    return PerformerFactory()


@pytest.fixture
def person():
    return PersonFactory()


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
def test_catalog_endpoint_list(api_client, catalog):
    path = reverse('catalog-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_endpoint_list(api_client, contest):
    path = reverse('contest-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestprivate_endpoint_list(api_client, contest):
    path = reverse('contestprivate-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestant_endpoint_list(api_client, contestant):
    path = reverse('contestant-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestantprivate_endpoint_list(api_client, contestant):
    path = reverse('contestantprivate-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_convention_endpoint_list(api_client, convention):
    path = reverse('convention-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_endpoint_list(api_client, organization):
    path = reverse('entity-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_host_endpoint_list(api_client, host):
    path = reverse('host-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_membership_endpoint_list(api_client, membership):
    path = reverse('membership-list')
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
def test_performance_endpoint_list(api_client, performance):
    path = reverse('performance-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performanceprivate_endpoint_list(api_client, performance):
    path = reverse('performanceprivate-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performer_endpoint_list(api_client, performer):
    path = reverse('performer-list')
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performerprivate_endpoint_list(api_client, performer):
    path = reverse('performerprivate-list')
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
def test_songprivate_endpoint_list(api_client, song):
    path = reverse('songprivate-list')
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
    path = reverse('assignment-detail', args=(assignment.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_award_endpoint_detail(api_client, award):
    path = reverse('award-detail', args=(award.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_catalog_endpoint_detail(api_client, catalog):
    path = reverse('catalog-detail', args=(catalog.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_endpoint_detail(api_client, contest):
    public = reverse('contest-detail', args=(contest.id.hex,))
    private = reverse('contestprivate-detail', args=(contest.contestprivate.pk,))
    public_response = api_client.get(public)
    private_response = api_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_contestant_endpoint_detail(api_client, contestant):
    path = reverse('contestant-detail', args=(contestant.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestantprivate_endpoint_detail(api_client, contestant):
    public = reverse('contestant-detail', args=(contestant.id.hex,))
    private = reverse('contestantprivate-detail', args=(contestant.contestantprivate.pk,))
    public_response = api_client.get(public)
    private_response = api_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_convention_endpoint_detail(api_client, convention):
    path = reverse('convention-detail', args=(convention.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_endpoint_detail(api_client, organization):
    path = reverse('entity-detail', args=(organization.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_host_endpoint_detail(api_client, host):
    path = reverse('host-detail', args=(host.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_membership_endpoint_detail(api_client, membership):
    path = reverse('membership-detail', args=(membership.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_office_endpoint_detail(api_client, office):
    path = reverse('office-detail', args=(office.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_officer_endpoint_detail(api_client, officer):
    path = reverse('officer-detail', args=(officer.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performance_endpoint_detail(api_client, performance):
    path = reverse('performance-detail', args=(performance.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performanceprivate_endpoint_detail(api_client, performance):
    public = reverse('performance-detail', args=(performance.id.hex,))
    private = reverse('performanceprivate-detail', args=(performance.performanceprivate.pk,))
    public_response = api_client.get(public)
    private_response = api_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_performer_endpoint_detail(api_client, performer):
    path = reverse('performer-detail', args=(performer.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performerprivate_endpoint_detail(api_client, performer):
    public = reverse('performer-detail', args=(performer.id.hex,))
    private = reverse('performerprivate-detail', args=(performer.performerprivate.pk,))
    public_response = api_client.get(public)
    private_response = api_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_person_endpoint_detail(api_client, person):
    path = reverse('person-detail', args=(person.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_endpoint_detail(api_client, round):
    path = reverse('round-detail', args=(round.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_endpoint_detail(api_client, score):
    path = reverse('score-detail', args=(score.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_endpoint_detail(api_client, session):
    path = reverse('session-detail', args=(session.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_endpoint_detail(api_client, slot):
    path = reverse('slot-detail', args=(slot.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_endpoint_detail(api_client, song):
    path = reverse('song-detail', args=(song.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_songprivate_endpoint_detail(api_client, song):
    public = reverse('song-detail', args=(song.id.hex,))
    private = reverse('songprivate-detail', args=(song.songprivate.pk,))
    public_response = api_client.get(public)
    private_response = api_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_submission_endpoint_detail(api_client, submission):
    path = reverse('submission-detail', args=(submission.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_endpoint_detail(api_client, venue):
    path = reverse('venue-detail', args=(venue.id.hex,))
    response = api_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_endpoint_detail(api_client, user):
    path = reverse('user-detail', args=(user.id.hex,))
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
def test_catalog_admin_list(admin_client, catalog):
    path = reverse('admin:app_catalog_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_admin_list(admin_client, contest):
    path = reverse('admin:app_contest_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestprivate_admin_list(admin_client, contest):
    path = reverse('admin:app_contestprivate_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestant_admin_list(admin_client, contestant):
    path = reverse('admin:app_contestant_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestantprivate_admin_list(admin_client, contestant):
    path = reverse('admin:app_contestantprivate_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_convention_admin_list(admin_client, convention):
    path = reverse('admin:app_convention_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_admin_list(admin_client, organization):
    path = reverse('admin:app_entity_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_host_admin_list(admin_client, host):
    path = reverse('admin:app_host_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_membership_admin_list(admin_client, membership):
    path = reverse('admin:app_membership_changelist')
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
def test_performance_admin_list(admin_client, performance):
    path = reverse('admin:app_performance_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performanceprivate_admin_list(admin_client, performance):
    path = reverse('admin:app_performanceprivate_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performer_admin_list(admin_client, performer):
    path = reverse('admin:app_performer_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performerprivate_admin_list(admin_client, performer):
    path = reverse('admin:app_performerprivate_changelist')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_person_admin_list(admin_client, person):
    path = reverse('admin:app_person_changelist')
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
def test_songprivate_admin_list(admin_client, song):
    path = reverse('admin:app_songprivate_changelist')
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
    path = reverse('admin:app_assignment_change', args=(assignment.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_award_admin_detail(admin_client, award):
    path = reverse('admin:app_award_change', args=(award.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_catalog_admin_detail(admin_client, catalog):
    path = reverse('admin:app_catalog_change', args=(catalog.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_admin_detail(admin_client, contest):
    public = reverse('admin:app_contest_change', args=(contest.id.hex,))
    private = reverse('admin:app_contestprivate_change', args=(contest.contestprivate.pk,))
    public_response = admin_client.get(public)
    private_response = admin_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_contestant_admin_detail(admin_client, contestant):
    path = reverse('admin:app_contestant_change', args=(contestant.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestantprivate_admin_detail(admin_client, contestant):
    public = reverse('admin:app_contestant_change', args=(contestant.id.hex,))
    private = reverse('admin:app_contestantprivate_change', args=(contestant.contestantprivate.pk,))
    public_response = admin_client.get(public)
    private_response = admin_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_convention_admin_detail(admin_client, convention):
    path = reverse('admin:app_convention_change', args=(convention.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_admin_detail(admin_client, organization):
    path = reverse('admin:app_entity_change', args=(organization.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_host_admin_detail(admin_client, host):
    path = reverse('admin:app_host_change', args=(host.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_membership_admin_detail(admin_client, membership):
    path = reverse('admin:app_membership_change', args=(membership.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_office_admin_detail(admin_client, office):
    path = reverse('admin:app_office_change', args=(office.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_officer_admin_detail(admin_client, officer):
    path = reverse('admin:app_officer_change', args=(officer.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performance_admin_detail(admin_client, performance):
    path = reverse('admin:app_performance_change', args=(performance.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performanceprivate_admin_detail(admin_client, performance):
    public = reverse('admin:app_performance_change', args=(performance.id.hex,))
    private = reverse('admin:app_performanceprivate_change', args=(performance.performanceprivate.pk,))
    public_response = admin_client.get(public)
    private_response = admin_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_performer_admin_detail(admin_client, performer):
    path = reverse('admin:app_performer_change', args=(performer.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performerprivate_admin_detail(admin_client, performance):
    public = reverse('admin:app_performance_change', args=(performance.id.hex,))
    private = reverse('admin:app_performanceprivate_change', args=(performance.performanceprivate.pk,))
    public_response = admin_client.get(public)
    private_response = admin_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_person_admin_detail(admin_client, person):
    path = reverse('admin:app_person_change', args=(person.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_admin_detail(admin_client, round):
    path = reverse('admin:app_round_change', args=(round.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_admin_detail(admin_client, score):
    path = reverse('admin:app_score_change', args=(score.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_admin_detail(admin_client, session):
    path = reverse('admin:app_session_change', args=(session.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_admin_detail(admin_client, slot):
    path = reverse('admin:app_slot_change', args=(slot.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_admin_detail(admin_client, song):
    path = reverse('admin:app_song_change', args=(song.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_songprivate_admin_detail(admin_client, song):
    public = reverse('admin:app_song_change', args=(song.id.hex,))
    private = reverse('admin:app_songprivate_change', args=(song.songprivate.pk,))
    public_response = admin_client.get(public)
    private_response = admin_client.get(private)
    assert ok(public_response)
    assert ok(private_response)


@pytest.mark.django_db()
def test_submission_admin_detail(admin_client, submission):
    path = reverse('admin:app_submission_change', args=(submission.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_admin_detail(admin_client, venue):
    path = reverse('admin:app_venue_change', args=(venue.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_admin_detail(admin_client, user):
    path = reverse('admin:app_user_change', args=(user.id.hex,))
    response = admin_client.get(path)
    assert ok(response)
