import json

from captains_log.logbook_app.models import Crew
from captains_log.logbook_app.testing.config.crew_config import (CREW_1,
                                                                 CREW_2,
                                                                 CREW_3)
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class DayCreateTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.crew_1 = self.client.post(
            "/logbook/api/crew/", CREW_1, format="json")
        self.crew_1_content = json.loads(self.crew_1.content)
        self.crew_2 = self.client.post(
            "/logbook/api/crew/", CREW_2, format="json")
        self.crew_2_content = json.loads(self.crew_2.content)
        self.crew_3 = self.client.post(
            "/logbook/api/crew/", CREW_3, format="json")
        self.crew_3_content = json.loads(self.crew_3.content)

    def tearDown(self):
        Crew.objects.all().delete()

    def test_created_crew(self):
        """
        Ensure we can create a new account object.
        """
        found_crew = Crew.objects.get(pk=1)

        self.assertEqual(self.crew_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Crew.objects.count(), 3)
        self.assertEqual(CREW_1["is_active"], found_crew.is_active)
        self.assertEqual(CREW_1["can_skipper"], found_crew.can_skipper)
        self.assertEqual(CREW_1["crew_name"], found_crew.crew_name)

    def test_get_crew(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.get(
            "/logbook/api/crew/", format="json")
        content = json.loads(response.content)

        self.assertEqual(content["count"], 3)
        self.assertEqual(len(content["results"]), 3)
        self.assertEqual(
            content["results"][0]["crew_name"], CREW_1["crew_name"])
        self.assertEqual(
            content["results"][1]["crew_name"], CREW_2["crew_name"])
        self.assertEqual(
            content["results"][2]["crew_name"], CREW_3["crew_name"])
        self.assertEqual(self.crew_1_content["crew_name"], CREW_1["crew_name"])
        self.assertEqual(self.crew_2_content["crew_name"], CREW_2["crew_name"])
        self.assertEqual(self.crew_3_content["crew_name"], CREW_3["crew_name"])
