from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import (
    ConventionFactory,
)


class ConventionTests(APITestCase):
    def setUp(self):
        ConventionFactory()

    def test_get_conventions(self):
        """Ensure we can get the convention list."""
        url = reverse('convention-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
