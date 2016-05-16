from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import (
    ConventionFactory,
    OrganizationFactory,
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
        OrganizationFactory.create()

    def test_get_organizations(self):
        """Ensure we can get the organization list."""
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
