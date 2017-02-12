
# Standard Libary
import json

# Third-Party
import pytest
from rest_framework.test import APIClient

# Django
from django.apps import apps as api_apps
from django.core import management
from django.test.client import Client
from django.urls import reverse

# First-Party
from app.factories import (  # ContestScoreFactory,; ContestantScoreFactory,; EntityFactory,; PerformanceScoreFactory,; PerformerScoreFactory,; SongScoreFactory,
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



# from app.models import (
#     Assignment,
#     Award,
#     Catalog,
#     Contest,
#     ContestScore,
#     Contestant,
#     ContestantScore,
#     Convention,
#     Entity,
#     Host,
#     Membership,
#     Office,
#     Officer,
#     Performance,
#     PerformanceScore,
#     Performer,
#     PerformerScore,
#     Person,
#     Round,
#     Score,
#     Session,
#     Slot,
#     Song,
#     SongScore,
#     Submission,
#     Venue,
#     User,
# )


def ok(response):
    return response.status_code == 200


@pytest.fixture
def admin_client():
    admin = AdminFactory()
    client = Client()
    client.force_login(admin)
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
def test_api_endpoint(admin_client):
    path = reverse('api-root')
    response = admin_client.get(path)
    assert ok(response)


# @pytest.mark.django_db()
# def test_assignment_endpoint_list(admin_client, assignment):
#     path = reverse('assignment-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_award_endpoint_list(admin_client, award):
#     path = reverse('award-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_catalog_endpoint_list(admin_client, catalog):
#     path = reverse('catalog-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_contest_endpoint_list(admin_client, contest):
#     path = reverse('contest-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_contestant_endpoint_list(admin_client, contestant):
#     path = reverse('contestant-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_convention_endpoint_list(admin_client, convention):
#     path = reverse('convention-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_entity_endpoint_list(admin_client, organization):
#     path = reverse('entity-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_host_endpoint_list(admin_client, host):
#     path = reverse('host-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_membership_endpoint_list(admin_client, membership):
#     path = reverse('membership-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_office_endpoint_list(admin_client, office):
#     path = reverse('office-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_officer_endpoint_list(admin_client, officer):
#     path = reverse('officer-list')
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_performance_endpoint_list(admin_client, performance):
#     path = reverse('performance-list')
#     response = admin_client.get(path)
#     assert ok(response)


@pytest.mark.django_db()
def test_performer_endpoint_list(admin_client, performer):
    path = reverse('performer-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_person_endpoint_list(admin_client, person):
    path = reverse('person-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_endpoint_list(admin_client, round):
    path = reverse('round-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_endpoint_list(admin_client, score):
    path = reverse('score-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_endpoint_list(admin_client, session):
    path = reverse('session-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_endpoint_list(admin_client, slot):
    path = reverse('slot-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_endpoint_list(admin_client, song):
    path = reverse('song-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_submission_endpoint_list(admin_client, submission):
    path = reverse('submission-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_endpoint_list(admin_client, venue):
    path = reverse('venue-list')
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_endpoint_list(admin_client, user):
    path = reverse('user-list')
    response = admin_client.get(path)
    assert ok(response)


# Detail Views

@pytest.mark.django_db()
def test_assignment_endpoint_detail(admin_client, assignment):
    path = reverse('assignment-detail', args=(assignment.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_award_endpoint_detail(admin_client, award):
    path = reverse('award-detail', args=(award.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_catalog_endpoint_detail(admin_client, catalog):
    path = reverse('catalog-detail', args=(catalog.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contest_endpoint_detail(admin_client, contest):
    path = reverse('contest-detail', args=(contest.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_contestant_endpoint_detail(admin_client, contestant):
    path = reverse('contestant-detail', args=(contestant.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_convention_endpoint_detail(admin_client, convention):
    path = reverse('convention-detail', args=(convention.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_entity_endpoint_detail(admin_client, organization):
    path = reverse('entity-detail', args=(organization.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_host_endpoint_detail(admin_client, host):
    path = reverse('host-detail', args=(host.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_membership_endpoint_detail(admin_client, membership):
    path = reverse('membership-detail', args=(membership.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_office_endpoint_detail(admin_client, office):
    path = reverse('office-detail', args=(office.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_officer_endpoint_detail(admin_client, officer):
    path = reverse('officer-detail', args=(officer.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performance_endpoint_detail(admin_client, performance):
    path = reverse('performance-detail', args=(performance.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performer_endpoint_detail(admin_client, performer):
    path = reverse('performer-detail', args=(performer.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_person_endpoint_detail(admin_client, person):
    path = reverse('person-detail', args=(person.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_round_endpoint_detail(admin_client, round):
    path = reverse('round-detail', args=(round.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_score_endpoint_detail(admin_client, score):
    path = reverse('score-detail', args=(score.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_session_endpoint_detail(admin_client, session):
    path = reverse('session-detail', args=(session.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_slot_endpoint_detail(admin_client, slot):
    path = reverse('slot-detail', args=(slot.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_song_endpoint_detail(admin_client, song):
    path = reverse('song-detail', args=(song.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_submission_endpoint_detail(admin_client, submission):
    path = reverse('submission-detail', args=(submission.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_venue_endpoint_detail(admin_client, venue):
    path = reverse('venue-detail', args=(venue.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_user_endpoint_detail(admin_client, user):
    path = reverse('user-detail', args=(user.id.hex,))
    response = admin_client.get(path)
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
def test_performer_admin_list(admin_client, performer):
    path = reverse('admin:app_performer_changelist')
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
    path = reverse('admin:app_contest_change', args=(contest.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


# @pytest.mark.django_db()
# def test_contestant_admin_detail(admin_client, contestant):
#     path = reverse('admin:app_contestant_change', args=(contestant.id.hex,))
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_convention_admin_detail(admin_client, convention):
#     path = reverse('admin:app_convention_change', args=(convention.id.hex,))
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_entity_admin_detail(admin_client, organization):
#     path = reverse('admin:app_entity_change', args=(organization.id.hex,))
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_host_admin_detail(admin_client, host):
#     path = reverse('admin:app_host_change', args=(host.id.hex,))
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_membership_admin_detail(admin_client, membership):
#     path = reverse('admin:app_membership_change', args=(membership.id.hex,))
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_office_admin_detail(admin_client, office):
#     path = reverse('admin:app_office_change', args=(office.id.hex,))
#     response = admin_client.get(path)
#     assert ok(response)


# @pytest.mark.django_db()
# def test_officer_admin_detail(admin_client, officer):
#     path = reverse('admin:app_officer_change', args=(officer.id.hex,))
#     response = admin_client.get(path)
#     assert ok(response)


@pytest.mark.django_db()
def test_performance_admin_detail(admin_client, performance):
    path = reverse('admin:app_performance_change', args=(performance.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


@pytest.mark.django_db()
def test_performer_admin_detail(admin_client, performer):
    path = reverse('admin:app_performer_change', args=(performer.id.hex,))
    response = admin_client.get(path)
    assert ok(response)


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


# ms = [
#     'assignment',
#     'award',
#     'catalog',
#     'contest',
#     # 'contestscore',
#     'contestant',
#     # 'contestantscore',
#     'convention',
#     'organization',
#     'host',
#     'membership',
#     'office',
#     'officer',
#     'performance',
#     # 'performancescore',
#     'performer',
#     # 'performerscore',
#     'person',
#     'round',
#     'score',
#     'session',
#     'slot',
#     'song',
#     # 'songscore',
#     'submission',
#     'venue',
#     'user',
# ]
# for m in ms:
#     out = """
# @pytest.mark.django_db()
# def test_{0}_endpoint_detail(client, {0}):
#     path = reverse('{0}-detail', args=({0}.id.hex,))
#     response = client.get(path)
#     assert ok(response)
# """.format(m)
#     print out







# for m in ms:
#     out = """
#     @pytest.fixture
#     def {0}():
#         return {1}Factory()
#     """.format(m, m.capitalize())
#     print out

# @pytest.mark.django_db()
# def test_venue_endpoint_detail(client, venue):
#     """Test Venue Endpoint."""
#     path = reverse('venue-detail', args=(venue.id.hex,))
#     response = client.get(path)
# #     assert jsonapi['data']['attributes']['name'] == "Test Convention Center"

#     for m in modules:
#         path = reverse('{0}-list'.format(m.lower()))
#         response = client.get(path)
#         assert_ok(response)

#     for m in modules:
#         f = config.get_model(m)
#         o = f.objects.first()
#         assert_true(o)
#         path = reverse('{0}-detail'.format(m.lower()), args=(o.id.hex,))
#         response = client.get(path)
#         assert_ok(response)


# modules = [
#     'assignment',
#     'award',
#     'catalog',
#     'contest',
#     # 'contestscore',
#     'contestant',
#     # 'contestantscore',
#     'convention',
#     'entity',
#     'host',
#     'membership',
#     'office',
#     'officer',
#     'performance',
#     # 'performancescore',
#     'performer',
#     # 'performerscore',
#     'person',
#     'round',
#     'score',
#     'session',
#     'slot',
#     'song',
#     # 'songscore',
#     'submission',
#     'venue',
#     'user',
# ]

# for m in modules:
#     def test_lists():
#         client = APIClient()
#         admin = User.objects.get(username='admin@barberscore.com')
#         client.force_authenticate(user=admin)
#         modules = [
#             'Assignment',
#             'Award',
#             'Catalog',
#             'Contest',
#             # 'ContestScore',
#             'Contestant',
#             # 'ContestantScore',
#             'Convention',
#             'Entity',
#             'Host',
#             'Membership',
#             'Office',
#             'Officer',
#             'Performance',
#             # 'PerformanceScore',
#             'Performer',
#             # 'PerformerScore',
#             'Person',
#             'Round',
#             'Score',
#             'Session',
#             'Slot',
#             'Song',
#             # 'SongScore',
#             'Submission',
#             'Venue',
#             'User',
#         ]

#         for m in modules:
#             path = reverse('{0}-list'.format(m.lower()))
#             response = client.get(path)
#             assert ok()

#         for m in modules:
#             f = config.get_model(m)
#             o = f.objects.first()
#             assert_true(o)
#             path = reverse('{0}-detail'.format(m.lower()), args=(o.id.hex,))
#             response = client.get(path)
#             assert_ok(response)


# @pytest.fixture
# def complete():
#     UserFactory(
#         username='admin@barberscore.com',
#         is_staff=True,
#     )
#     user = UserFactory(
#         username='user@barberscore.com',
#     )
#     organization = OrganizationFactory(
#     )
#     district = DistrictFactory(
#         parent=organization,
#     )
#     quartet = QuartetFactory(
#         parent=district,
#     )
#     person = PersonFactory(
#         user=user,
#     )
#     office = OfficeFactory(
#     )
#     award = AwardFactory(
#         entity=organization,
#     )
#     convention = ConventionFactory(
#     )
#     session = SessionFactory(
#         convention=convention,
#     )
#     round = RoundFactory(
#         session=session,
#     )
#     contest = ContestFactory(
#         session=session,
#         award=award,
#     )
#     performer = PerformerFactory(
#         session=session,
#         entity=quartet,
#     )
#     membership = MembershipFactory(
#         person=person,
#         entity=organization,
#     )
#     performance = PerformanceFactory(
#         round=round,
#         performer=performer,
#     )
#     song = SongFactory(
#         performance=performance,
#     )
#     VenueFactory(
#     )
#     contestant = ContestantFactory(
#         performer=performer,
#         contest=contest,
#     )
#     HostFactory(
#         convention=convention,
#         entity=organization,
#     )
#     AssignmentFactory(
#         convention=convention,
#         person=person,
#     )
#     CatalogFactory(
#     )
#     OfficerFactory(
#         membership=membership,
#         office=office,
#     )
#     ScoreFactory(
#         song=song,
#     )
#     SlotFactory(
#         round=round,
#     )
#     SubmissionFactory(
#         performer=performer,
#     )
#     # Not sure about this approach, but it works
#     contest_score = ContestScore(
#         contest_ptr=contest,
#     )
#     contest_score.save_base(raw=True)

#     contestant_score = ContestantScore(
#         contestant_ptr=contestant,
#     )
#     contestant_score.save_base(raw=True)

#     performance_score = PerformanceScore(
#         performance_ptr=performance,
#     )
#     performance_score.save_base(raw=True)

#     performer_score = PerformerScore(
#         performer_ptr=performer,
#     )
#     performer_score.save_base(raw=True)

#     song_score = SongScore(
#         song_ptr=song,
#     )
#     song_score.save_base(raw=True)






# @with_setup(simple_setup, tear_down)
# def test_admin():
#     client = Client()
#     admin = User.objects.get(username='admin@barberscore.com')
#     client.force_login(admin)
#     modules = [
#         'Assignment',
#         'Award',
#         'Catalog',
#         'Contest',
#         'ContestScore',
#         'Contestant',
#         'ContestantScore',
#         'Convention',
#         'Entity',
#         'Host',
#         'Membership',
#         'Office',
#         'Officer',
#         'Performance',
#         'PerformanceScore',
#         'Performer',
#         'PerformerScore',
#         'Person',
#         'Round',
#         'Score',
#         'Session',
#         'Slot',
#         'Song',
#         'SongScore',
#         'Submission',
#         'Venue',
#         'User',
#     ]
#     for m in modules:
#         path = reverse('admin:app_{0}_changelist'.format(m.lower()))
#         response = client.get(path)
#         assert_ok(response)

#     for m in modules:
#         f = config.get_model(m)
#         o = f.objects.first()
#         assert_true(o)
#         path = reverse('admin:app_{0}_change'.format(m.lower()), args=(o.id.hex,))
#         response = client.get(path)
#         assert_ok(response)










# from rest_assured.testcases import (
#     BaseRESTAPITestCase,
#     ReadRESTAPITestCaseMixin,
#     ReadWriteRESTAPITestCaseMixin,
# )

# # Django
# from django.test import SimpleTestCase


# # # Public CRUD Tests
# # class AwardPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'award'
# #     factory_class = InternationalQuartetAwardFactory


# # class JudgePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'judge'
# #     factory_class = JudgeFactory


# # class ChapterPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'chapter'
# #     factory_class = ChapterFactory


# # class ChartPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'chart'
# #     factory_class = ChartFactory


# # class ContestantPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'contestant'
# #     factory_class = ContestantFactory


# # class ContestPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'contest'
# #     factory_class = ContestFactory


# # class ConventionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'convention'
# #     factory_class = ConventionFactory


# # class OrganizationPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'organization'
# #     factory_class = OrganizationFactory


# # class AssignmentPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'assignment'
# #     factory_class = AssignmentFactory


# # class MemberPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'member'
# #     factory_class = MemberFactory


# # class PerformancePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'performance'
# #     factory_class = PerformanceFactory


# # class PerformerPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'performer'
# #     factory_class = PerformerFactory


# # class PersonPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'person'
# #     factory_class = PersonFactory


# # class GroupPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'group'
# #     factory_class = GroupFactory


# # class RolePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'role'
# #     factory_class = RoleFactory


# # class RoundPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'round'
# #     factory_class = RoundFactory


# # class ScorePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'score'
# #     factory_class = ScoreFactory
# #     user_factory = AdminFactory


# # class SessionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'session'
# #     factory_class = InternationalQuartetSessionFactory


# # class SongPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'song'
# #     factory_class = SongFactory


# # class SubmissionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'submission'
# #     factory_class = SubmissionFactory


# # class VenuePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'venue'
# #     factory_class = VenueFactory


# # # Admin CRUD Tests
# # class ChartAdminTest(ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'chart'
# #     factory_class = ChartFactory
# #     user_factory = AdminFactory
# #     create_data = {'title': 'The Older Songs'}
# #     update_data = {'title': 'The Oldest Songs'}





# def build_admin():
#     AdminFactory()
#     return


# def build_primitives():
#     AdminFactory()
#     user = PublicFactory(
#         email='joe@barberscore.com',
#         name='Joe District',
#     )
#     representative = PersonFactory(
#         name='Joe District',
#         user=user,
#     )
#     bhs = InternationalFactory()
#     district = DistrictFactory(
#         parent=bhs,
#         representative=representative,
#     )
#     InternationalQuartetAwardFactory(
#         organization=bhs,
#     )
#     InternationalChorusAwardFactory(
#         organization=bhs,
#     )
#     InternationalSeniorsAwardFactory(
#         organization=bhs,
#     )
#     InternationalYouthAwardFactory(
#         organization=bhs,
#     )
#     DistrictQuartetAwardFactory(
#         organization=district,
#     )
#     DistrictChorusAwardFactory(
#         organization=district,
#     )
#     DistrictSeniorsAwardFactory(
#         organization=district,
#     )
#     DistrictYouthAwardFactory(
#         organization=district,
#     )

#     OfficialAdminJudgeFactory.create_batch(5)
#     OfficialMusicJudgeFactory.create_batch(10)
#     OfficialPresentationJudgeFactory.create_batch(10)
#     OfficialSingingJudgeFactory.create_batch(10)

#     chapters = DistrictChapterFactory.create_batch(
#         20,
#         organization=district,
#     )

#     for chapter in chapters:
#         ChorusFactory(
#             organization=district,
#             chapter=chapter,
#         )

#     persons = PersonFactory.create_batch(
#         1000,
#         chapter=random.choice(chapters),
#     )
#     quartets = QuartetFactory.create_batch(100)
#     for quartet in quartets:
#         TenorFactory(
#             group=quartet,
#             person=persons.pop()
#         )
#         LeadFactory(
#             group=quartet,
#             person=persons.pop()
#         )
#         BaritoneFactory(
#             group=quartet,
#             person=persons.pop()
#         )
#         BassFactory(
#             group=quartet,
#             person=persons.pop()
#         )

#     VenueFactory.create_batch(10)
#     return


# def build_international():
#     build_admin()
#     venue = VenueFactory(
#         location='Bridgestone Arena',
#         city='Nashville',
#         state='Tennessee',
#     )
#     bhs = InternationalFactory()
#     district_organization = DistrictFactory(
#         parent=bhs,
#     )
#     quartet_award = InternationalQuartetAwardFactory(
#         organization=bhs,
#     )
#     chorus_award = InternationalChorusAwardFactory(
#         organization=bhs,
#     )
#     convention = SummerConventionFactory(
#         organization=bhs,
#         venue=venue,
#         status=Convention.STATUS.validated,
#     )
#     quartet_session = SessionFactory(
#         kind=Session.KIND.quartet,
#         convention=convention,
#         status=Session.STATUS.validated,
#         num_rounds=3,
#     )
#     chorus_session = SessionFactory(
#         kind=Session.KIND.chorus,
#         convention=convention,
#         status=Session.STATUS.validated,
#         num_rounds=1,
#     )
#     admins = OfficialAdminJudgeFactory.create_batch(3)
#     for admin in admins:
#         AssignmentFactory(
#             session=quartet_session,
#             judge=admin,
#             category=Assignment.CATEGORY.admin,
#             kind=Assignment.KIND.official,
#             status=Assignment.STATUS.validated,
#         )
#         AssignmentFactory(
#             session=chorus_session,
#             judge=admin,
#             category=Assignment.CATEGORY.admin,
#             kind=Assignment.KIND.official,
#             status=Assignment.STATUS.validated,
#         )
#     categories = [
#         'music',
#         'presentation',
#         'singing',
#     ]
#     chorus_assignments = []
#     quartet_assignments = []
#     for category in categories:
#         i = 1
#         while i <= 5:
#             judge = JudgeFactory(
#                 status=Judge.STATUS.active,
#                 category=getattr(Judge.CATEGORY, category),
#             )
#             quartet_assignment = AssignmentFactory(
#                 session=quartet_session,
#                 judge=judge,
#                 category=getattr(Assignment.CATEGORY, category),
#                 kind=Assignment.KIND.official,
#                 slot=i,
#                 status=Assignment.STATUS.validated,
#             )
#             quartet_assignments.append(quartet_assignment)
#             chorus_assignment = AssignmentFactory(
#                 session=chorus_session,
#                 judge=judge,
#                 category=getattr(Assignment.CATEGORY, category),
#                 kind=Assignment.KIND.official,
#                 slot=i,
#                 status=Assignment.STATUS.validated,
#             )
#             chorus_assignments.append(chorus_assignment)
#             i += 1
#     quartet_contest = ContestFactory(
#         session=quartet_session,
#         award=quartet_award,
#         status=Contest.STATUS.validated,
#         num_rounds=3,
#     )
#     chorus_contest = ContestFactory(
#         session=chorus_session,
#         award=chorus_award,
#         status=Contest.STATUS.validated,
#         num_rounds=1,
#     )
#     quartet_quarters = quartet_session.rounds.get(num=1)
#     quartet_session.current = quartet_quarters
#     quartet_session.primary = quartet_contest
#     quartet_session.save()
#     chorus_finals = chorus_session.rounds.get(num=1)
#     chorus_session.current = chorus_finals
#     chorus_session.primary = chorus_contest
#     chorus_session.save()
#     quartets = QuartetFactory.create_batch(50)
#     i = 1
#     for quartet in quartets:
#         performer = PerformerFactory(
#             session=quartet_session,
#             group=quartet,
#             status=Performer.STATUS.validated,
#             representing=district_organization,
#             prelim=FuzzyInteger(50, 95).fuzz(),
#         )
#         s = 1
#         while s <= 6:
#             try:
#                 SubmissionFactory(
#                     performer=performer,
#                     status=Submission.STATUS.validated,
#                 )
#             except IntegrityError:
#                 SubmissionFactory(
#                     performer=performer,
#                     status=Submission.STATUS.validated,
#                 )
#             s += 1
#         ContestantFactory(
#             contest=quartet_contest,
#             performer=performer,
#             status=Contestant.STATUS.validated,
#         )
#         slot = SlotFactory(
#             round=quartet_quarters,
#             num=i,
#             onstage=FuzzyDateTime(
#                 datetime(2016, 7, 1, tzinfo=venue.timezone),
#                 datetime(2016, 7, 2, tzinfo=venue.timezone),
#             )
#         )
#         PerformanceFactory(
#             performer=performer,
#             round=quartet_quarters,
#             slot=slot,
#             num=i,
#             status=Performance.STATUS.validated,
#         )
#         i += 1
#     quartet_quarters.status = Round.STATUS.validated
#     quartet_quarters.save()
#     choruses = ChorusFactory.create_batch(20)
#     i = 1
#     for chorus in choruses:
#         performer = PerformerFactory(
#             session=chorus_session,
#             group=chorus,
#             status=Performer.STATUS.validated,
#             representing=district_organization,
#             prelim=FuzzyInteger(50, 95).fuzz(),
#         )
#         s = 1
#         while s <= 2:
#             try:
#                 SubmissionFactory(
#                     performer=performer,
#                     status=Submission.STATUS.validated,
#                 )
#             except IntegrityError:
#                 SubmissionFactory(
#                     performer=performer,
#                     status=Submission.STATUS.validated,
#                 )
#             s += 1
#         ContestantFactory(
#             contest=chorus_contest,
#             performer=performer,
#             status=Contestant.STATUS.validated,
#         )
#         slot = SlotFactory(
#             round=chorus_finals,
#             num=i,
#             onstage=FuzzyDateTime(
#                 datetime(2016, 7, 2, tzinfo=venue.timezone),
#                 datetime(2016, 7, 3, tzinfo=venue.timezone),
#             ),
#         )
#         PerformanceFactory(
#             slot=slot,
#             performer=performer,
#             round=chorus_finals,
#             num=i,
#             status=Performance.STATUS.validated,
#         )
#         i += 1
#     chorus_finals.status = Round.STATUS.validated
#     chorus_finals.save()


# def score_performance(performance):
#     performance.start()
#     center = performance.performer.prelim
#     i = (performance.round.num * 2) - 2
#     for song in performance.songs.all():
#         song.submission = performance.performer.submissions.order_by('id')[i]
#         for score in song.scores.all():
#             score.points = center + FuzzyInteger(-4, 4).fuzz()
#             score.save()
#         song.save()
#         i += 1
#     performance.finish()
#     performance.save()
#     return


# def score_round(round):
#     for performance in round.performances.all():
#         score_performance(performance)
#     return


# def finish_session(session):
#     for round in session.rounds.order_by('-kind'):
#         score_round(round)
#         round.finish()
#         round.save()
#     return


# def calculate_session(session):
#     for performer in session.performers.all():
#         for performance in performer.performances.all():
#             for song in performance.songs.all():
#                 song.calculate()
#                 song.save()
#             performance.calculate()
#             performance.save()
#         performer.calculate()
#         performer.save()
#     return


# def calculate_performer(performer):
#     for performance in performer.performances.all():
#         for song in performance.songs.all():
#             song.calculate()
#             song.save()
#         performance.calculate()
#         performance.save()
#     performer.calculate()
#     performer.save()
#     return


# def complete_convention(convention):
#     for session in convention.sessions.all():
#         finish_session(session)
#         calculate_session(session)
#         session.save()

# @with_setup(setup_international)
# def test_stub():
#     assert True
