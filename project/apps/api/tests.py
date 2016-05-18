from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import (
    AdminFactory,
    AwardFactory,
    CertificationFactory,
    ChapterFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    DistrictFactory,
    InternationalFactory,
    JudgeFactory,
    MemberFactory,
    PerformanceFactory,
    PerformerFactory,
    PersonFactory,
    QuartetFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SongFactory,
    SubmissionFactory,
    TenorFactory,
    VenueFactory,
)


class ModelTests(APITestCase):
    def setUp(self):
        AdminFactory()
        jwt = reverse('obtain-jwt-token')
        data = {
            'email': 'admin@barberscore.com',
            'password': 'password'
        }
        login = self.client.post(jwt, data)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + login.data['token'])
        self.international = InternationalFactory()
        self.district = DistrictFactory()
        self.award = AwardFactory(
            organization=self.international,
        )
        self.chapter = ChapterFactory(
            organization=self.district,
        )
        self.chart = ChartFactory()
        self.person = PersonFactory()
        self.quartet = QuartetFactory(
            organization=self.district,
        )
        self.venue = VenueFactory()
        self.convention = ConventionFactory(
            organization=self.international,
            venue=self.venue,
        )
        self.session = SessionFactory(
            convention=self.convention,
        )
        self.contest = ContestFactory(
            session=self.session,
            award=self.award,
        )
        self.certification = CertificationFactory(
            person=self.person,
        )
        self.judge = JudgeFactory(
            session=self.session,
            certification=self.certification,
        )
        self.round = RoundFactory(
            session=self.session,
        )
        self.performer = PerformerFactory(
            session=self.session,
            group=self.quartet,
        )
        self.contestant = ContestantFactory(
            performer=self.performer,
            contest=self.contest,
        )
        self.member = MemberFactory(
            chapter=self.chapter,
            person=self.person,
        )
        self.role = TenorFactory(
            group=self.quartet,
            person=self.person,
        )
        self.submission = SubmissionFactory(
            performer=self.performer,
            chart=self.chart,
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

    def test_get_awards(self):
        """Ensure we can get the award list."""
        url = reverse('award-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_certifications(self):
        """Ensure we can get the certification list."""
        url = reverse('certification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_chapters(self):
        """Ensure we can get the chapter list."""
        url = reverse('chapter-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_charts(self):
        """Ensure we can get the chart list."""
        url = reverse('chart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_contests(self):
        """Ensure we can get the contest list."""
        url = reverse('contest-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_contestants(self):
        """Ensure we can get the contestant list."""
        url = reverse('contestant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_conventions(self):
        """Ensure we can get the convention list."""
        url = reverse('convention-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_groups(self):
        """Ensure we can get the group list."""
        url = reverse('group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_judges(self):
        """Ensure we can get the judge list."""
        url = reverse('judge-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_members(self):
        """Ensure we can get the member list."""
        url = reverse('member-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_organizations(self):
        """Ensure we can get the member list."""
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 2)

    def test_get_performances(self):
        """Ensure we can get the performance list."""
        url = reverse('performance-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_performers(self):
        """Ensure we can get the performer list."""
        url = reverse('performer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_persons(self):
        """Ensure we can get the person list."""
        url = reverse('person-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_roles(self):
        """Ensure we can get the role list."""
        url = reverse('role-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_rounds(self):
        """Ensure we can get the round list."""
        url = reverse('round-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_scores(self):
        """Ensure we can get the score list."""
        url = reverse('song-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_sessions(self):
        """Ensure we can get the session list."""
        url = reverse('session-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_songs(self):
        """Ensure we can get the song list."""
        url = reverse('song-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_submissions(self):
        """Ensure we can get the submission list."""
        url = reverse('submission-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)

    def test_get_venues(self):
        """Ensure we can get the venue list."""
        url = reverse('venue-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['pagination']['count'], 1)
