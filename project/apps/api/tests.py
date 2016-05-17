from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import (
    AdminFactory,
    ConventionFactory,
    InternationalFactory,
    DistrictFactory,
    AwardFactory,
    ChartFactory,
    QuartetFactory,
    ChorusFactory,
    PersonFactory,
    VenueFactory,
    SessionFactory,
    CertificationFactory,
    JudgeFactory,
    MemberFactory,
    TenorFactory,
    RoundFactory,
    ContestFactory,
    PerformerFactory,
    SubmissionFactory,
    ContestantFactory,
    PerformanceFactory,
    SongFactory,
    ScoreFactory,
)


# class ConventionTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         ConventionFactory()

#     def test_get_conventions(self):
#         """Ensure we can get the convention list."""
#         url = reverse('convention-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class OrganizationTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         InternationalFactory()
#         DistrictFactory()

#     def test_get_organizations(self):
#         """Ensure we can get the organization list."""
#         url = reverse('organization-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class AwardTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         AwardFactory()

#     def test_get_awards(self):
#         """Ensure we can get the award list."""
#         url = reverse('award-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class ChartTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         ChartFactory()

#     def test_get_charts(self):
#         """Ensure we can get the chart list."""
#         url = reverse('chart-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class GroupTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         QuartetFactory()
#         ChorusFactory()

#     def test_get_groups(self):
#         """Ensure we can get the group list."""
#         url = reverse('group-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class PersonTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         PersonFactory()

#     def test_get_persons(self):
#         """Ensure we can get the person list."""
#         url = reverse('person-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class VenueTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         VenueFactory()

#     def test_get_venues(self):
#         """Ensure we can get the venue list."""
#         url = reverse('venue-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class SessionTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         SessionFactory()

#     def test_get_sessions(self):
#         """Ensure we can get the person list."""
#         url = reverse('session-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class CertificationTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         CertificationFactory()

#     def test_get_certifications(self):
#         """Ensure we can get the person list."""
#         url = reverse('certification-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class JudgeTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         JudgeFactory()

#     def test_get_judges(self):
#         """Ensure we can get the judge list."""
#         url = reverse('judge-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class MemberTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         MemberFactory()

#     def test_get_members(self):
#         """Ensure we can get the member list."""
#         url = reverse('member-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class RoleTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         TenorFactory()

#     def test_get_roles(self):
#         """Ensure we can get the role list."""
#         url = reverse('role-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class RoundTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         RoundFactory()

#     def test_get_rounds(self):
#         """Ensure we can get the round list."""
#         url = reverse('round-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class ContestTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         ContestFactory()

#     def test_get_contests(self):
#         """Ensure we can get the contest list."""
#         url = reverse('contest-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class PerformerTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         PerformerFactory()

#     def test_get_performers(self):
#         """Ensure we can get the performer list."""
#         url = reverse('performer-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class SubmissionTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         SubmissionFactory()

#     def test_get_submissions(self):
#         """Ensure we can get the submission list."""
#         url = reverse('submission-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class ContestantTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         ContestantFactory(
#             performer=PerformerFactory(),
#             contest=ContestFactory(),
#         )

#     def test_get_contestants(self):
#         """Ensure we can get the contestant list."""
#         url = reverse('contestant-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class PerformanceTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         PerformanceFactory()

#     def test_get_performances(self):
#         """Ensure we can get the performance list."""
#         url = reverse('performance-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class SongTests(APITestCase):
#     def setUp(self):
#         AdminFactory()
#         jwt = reverse('obtain-jwt-token')
#         data = {
#             'email': 'admin@barberscore.com',
#             'password': 'password'
#         }
#         login = self.client.post(jwt, data)
#         self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
#         SongFactory()

#     def test_get_songs(self):
#         """Ensure we can get the song list."""
#         url = reverse('song-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


class ScoreTests(APITestCase):
    def setUp(self):
        AdminFactory()
        jwt = reverse('obtain-jwt-token')
        data = {
            'email': 'admin@barberscore.com',
            'password': 'password'
        }
        login = self.client.post(jwt, data)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
        self.venue = VenueFactory()
        self.convention = ConventionFactory(
            venue=self.venue,
        )
        self.session = SessionFactory(
            convention=self.convention,
        )
        self.judge = JudgeFactory(
            session=self.session,
        )
        self.round = RoundFactory(
            session=self.session,
        )
        self.performer = PerformerFactory(
            session=self.session,
        )
        self.submission = SubmissionFactory(
            performer=self.performer
        )
        self.performance = PerformanceFactory(
            performer=self.performer,
            round=self.round,
        )
        self.song = SongFactory(
            performance=self.performance,
            submission=self.submission
        )
        self.score = ScoreFactory(
            song=self.song,
            judge=self.judge,
        )

    def test_get_scores(self):
        """Ensure we can get the score list."""
        url = reverse('song-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
