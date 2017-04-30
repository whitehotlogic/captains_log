from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from logbook_app.models import Day, Hour, PortOfCall, Note, Vessel


class AccountTests(APITestCase):
    def test_create_vessel(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('logbook_app:list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vessel.objects.count(), 1)
        self.assertEqual(Vessel.objects.get().name, 'DabApps')
# Using the standard RequestFactory API to create a form POST request
# factory = APIRequestFactory()
#
# vessel_data = {}
# request = factory.post('/api/vessels/', vessel_data, format='json')
