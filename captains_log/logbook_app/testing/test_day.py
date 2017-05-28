import json

from captains_log.logbook_app.models import Day, PortOfCall, Vessel, Crew
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .config.day_config import DAY_1, DAY_3
from .config.portofcall_config import PORT_OF_CALL_1, PORT_OF_CALL_2
from .config.vessel_config import VESSEL_1, VESSEL_2
from .config.crew_config import CREW_1, CREW_2


class DayCreateTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.port_of_call_1 = PortOfCall.objects.create(**PORT_OF_CALL_1)
        self.port_of_call_2 = PortOfCall.objects.create(**PORT_OF_CALL_2)
        self.crew_1 = Crew.objects.create(**CREW_1)
        self.crew_2 = Crew.objects.create(**CREW_2)
        VESSEL_1["owner"] = self.crew_1
        VESSEL_1["skipper"] = self.crew_1
        VESSEL_2["owner"] = self.crew_2
        VESSEL_2["skipper"] = self.crew_2
        self.vessel_1 = Vessel.objects.create(**VESSEL_1)
        self.vessel_2 = Vessel.objects.create(**VESSEL_2)
        DAY_1_TEMP = dict(DAY_1)
        DAY_3_TEMP = dict(DAY_3)
        DAY_1_TEMP["vessel"] = self.vessel_1
        DAY_3_TEMP["vessel"] = self.vessel_2
        DAY_1_TEMP["port_of_call"] = self.port_of_call_1
        DAY_3_TEMP["port_of_call"] = self.port_of_call_2
        self.day_1 = self.client.post(
            "/logbook/api/days/", DAY_1, format="json")
        self.day_1_content = json.loads(self.day_1.content)
        self.day_3 = self.client.post(
            "/logbook/api/days/", DAY_3, format="json")
        self.day_3_content = json.loads(self.day_3.content)

    def tearDown(self):
        Day.objects.all().delete()
        Vessel.objects.all().delete()

    def test_created_day(self):
        """
        Ensure we can create a new account object.
        """
        found_day = Day.objects.get(pk=1)

        self.assertEqual(self.day_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Day.objects.count(), 2)
        self.assertEqual(DAY_1["date"], str(found_day.date))
        self.assertEqual(DAY_1["port_of_call"], found_day.port_of_call.id)
        self.assertEqual(self.vessel_1.name, found_day.vessel.name)

    def test_get_days(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.get(
            "/logbook/api/days/", format="json")
        content = json.loads(response.content)

        self.assertEqual(content["count"], 2)
        self.assertEqual(len(content["results"]), 2)
        self.assertEqual(content["results"][0]["date"], DAY_1["date"])
        self.assertEqual(content["results"][1]["date"], DAY_3["date"])
        self.assertEqual(self.day_1_content["date"], DAY_1["date"])
        self.assertEqual(self.day_3_content["date"], DAY_3["date"])

    def test_get_day_1(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.get(
            "/logbook/api/days/1", format="json", follow=True)
        content = json.loads(response.content)

        self.assertEqual(content["port_of_call"]["id"], DAY_1["port_of_call"])

    def test_get_day_3(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.get(
            "/logbook/api/days/2", format="json", follow=True)
        content = json.loads(response.content)

        self.assertEqual(content["port_of_call"], DAY_3["port_of_call"])
