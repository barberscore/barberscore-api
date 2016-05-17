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
    SessionFactory,
    CertificationFactory,
    JudgeFactory,
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
