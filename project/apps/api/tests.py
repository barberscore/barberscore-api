from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import (
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
    ContestantFactory,
)


class ConventionTests(APITestCase):
    def setUp(self):
        ConventionFactory.create()

    def test_get_conventions(self):
        """Ensure we can get the convention list."""
        url = reverse('convention-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrganizationTests(APITestCase):
    def setUp(self):
        InternationalFactory.create()
        DistrictFactory.create()

    def test_get_organizations(self):
        """Ensure we can get the organization list."""
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AwardTests(APITestCase):
    def setUp(self):
        AwardFactory.create()

    def test_get_awards(self):
        """Ensure we can get the award list."""
        url = reverse('award-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChartTests(APITestCase):
    def setUp(self):
        ChartFactory.create()

    def test_get_charts(self):
        """Ensure we can get the chart list."""
        url = reverse('chart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupTests(APITestCase):
    def setUp(self):
        QuartetFactory.create()
        ChorusFactory.create()

    def test_get_groups(self):
        """Ensure we can get the group list."""
        url = reverse('group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PersonTests(APITestCase):
    def setUp(self):
        PersonFactory.create()

    def test_get_persons(self):
        """Ensure we can get the person list."""
        url = reverse('person-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VenueTests(APITestCase):
    def setUp(self):
        VenueFactory.create()

    def test_get_venues(self):
        """Ensure we can get the venue list."""
        url = reverse('venue-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SessionTests(APITestCase):
    def setUp(self):
        SessionFactory.create()

    def test_get_sessions(self):
        """Ensure we can get the person list."""
        url = reverse('session-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CertificationTests(APITestCase):
    def setUp(self):
        CertificationFactory.create()

    def test_get_certifications(self):
        """Ensure we can get the person list."""
        url = reverse('certification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JudgeTests(APITestCase):
    def setUp(self):
        JudgeFactory.create()

    def test_get_judges(self):
        """Ensure we can get the judge list."""
        url = reverse('judge-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MemberTests(APITestCase):
    def setUp(self):
        MemberFactory.create()

    def test_get_members(self):
        """Ensure we can get the member list."""
        url = reverse('member-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoleTests(APITestCase):
    def setUp(self):
        TenorFactory.create()

    def test_get_roles(self):
        """Ensure we can get the role list."""
        url = reverse('role-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoundTests(APITestCase):
    def setUp(self):
        RoundFactory.create()

    def test_get_rounds(self):
        """Ensure we can get the round list."""
        url = reverse('round-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContestTests(APITestCase):
    def setUp(self):
        ContestFactory.create()

    def test_get_contests(self):
        """Ensure we can get the contest list."""
        url = reverse('contest-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PerformerTests(APITestCase):
    def setUp(self):
        PerformerFactory.create()

    def test_get_performers(self):
        """Ensure we can get the performer list."""
        url = reverse('performer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContestantTests(APITestCase):
    def setUp(self):
        ContestantFactory.create(
        )

    def test_get_contestants(self):
        """Ensure we can get the contestant list."""
        url = reverse('contestant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
