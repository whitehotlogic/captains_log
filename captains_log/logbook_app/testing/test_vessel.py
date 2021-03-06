import json

from captains_log.logbook_app.models import Day, Hour, PortOfCall, Vessel, Crew
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .config.day_config import DAY_1, DAY_2
from .config.hour_config import HOUR_SET_1
from .config.portofcall_config import PORT_OF_CALL_1, PORT_OF_CALL_2
from .config.vessel_config import VESSEL_1, VESSEL_2
from .config.crew_config import CREW_1, CREW_2


class VesselCreateTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.crew_1 = Crew.objects.create(**CREW_1)
        self.crew_2 = Crew.objects.create(**CREW_2)
        VESSEL_1["owner"] = self.crew_1.id
        VESSEL_1["skipper"] = self.crew_1.id
        VESSEL_2["owner"] = self.crew_2.id
        VESSEL_2["skipper"] = self.crew_2.id
        self.vessel_1 = self.client.post(
            "/logbook/api/vessels/", VESSEL_1, format="json")
        self.vessel_1_content = json.loads(self.vessel_1.content)
        self.vessel_2 = self.client.post(
            "/logbook/api/vessels/", VESSEL_2, format="json")
        self.vessel_2_content = json.loads(self.vessel_2.content)

    def tearDown(self):
        Vessel.objects.all().delete()
        Crew.objects.all().delete()

    def test_created_vessel(self):
        """
        Ensure we can create a new account object.
        """
        found_vessel = Vessel.objects.get(pk=self.vessel_1_content["id"])
        self.assertEqual(self.vessel_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vessel.objects.count(), 2)
        self.assertEqual(VESSEL_1["vessel_name"], found_vessel.vessel_name)
        self.assertEqual(
            VESSEL_1["hull_number"], found_vessel.hull_number)

    def test_get_vessels(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.get(
            "/logbook/api/vessels/", format="json")
        content = json.loads(response.content)

        self.assertEqual(content["count"], 2)
        self.assertEqual(len(content["results"]), 2)
        self.assertEqual(
            content["results"][0]["hull_number"], VESSEL_1["hull_number"])
        self.assertEqual(
            content["results"][1]["hull_number"], VESSEL_2["hull_number"])
        self.assertEqual(
            self.vessel_1_content["hull_number"], VESSEL_1["hull_number"])
        self.assertEqual(
            self.vessel_2_content["hull_number"], VESSEL_2["hull_number"])

    def test_get_vessel_1(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.get(
            "/logbook/api/vessels/1", format="json", follow=True)
        content = json.loads(response.content)

        self.assertEqual(content["owner"], VESSEL_1["owner"])

    def test_get_vessel_2(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.get(
            "/logbook/api/vessels/2", format="json", follow=True)
        content = json.loads(response.content)

        self.assertEqual(content["owner"], VESSEL_2["owner"])


class VesselCheckByDateTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.crew_1 = Crew.objects.create(**CREW_1)
        self.crew_2 = Crew.objects.create(**CREW_2)
        VESSEL_1["owner"] = self.crew_1
        VESSEL_1["skipper"] = self.crew_1
        VESSEL_2["owner"] = self.crew_2
        VESSEL_2["skipper"] = self.crew_2
        self.vessel_1 = Vessel.objects.create(**VESSEL_1)
        self.vessel_2 = Vessel.objects.create(**VESSEL_2)
        self.port_of_call_1 = PortOfCall.objects.create(**PORT_OF_CALL_1)
        self.port_of_call_2 = PortOfCall.objects.create(**PORT_OF_CALL_2)
        DAY_1_TEMP = dict(DAY_1)
        DAY_2_TEMP = dict(DAY_2)
        DAY_1_TEMP["vessel"] = self.vessel_1
        DAY_2_TEMP["vessel"] = self.vessel_2
        DAY_1_TEMP["port_of_call"] = self.port_of_call_1
        DAY_2_TEMP["port_of_call"] = self.port_of_call_2
        self.day_1 = Day.objects.create(**DAY_1_TEMP)
        self.day_2 = Day.objects.create(**DAY_2_TEMP)
        HOUR_SET_1_TEMP = list(HOUR_SET_1)
        for hour in HOUR_SET_1_TEMP:
            hour["day"] = self.day_1
            Hour.objects.create(**hour)
        self.hour_set_1 = Hour.objects.filter(day=self.day_1)

    def tearDown(self):
        Crew.objects.all().delete()
        Vessel.objects.all().delete()
        PortOfCall.objects.all().delete()
        Day.objects.all().delete()
        Hour.objects.all().delete()

    def test_existing_date(self):
        response = self.client.get(
            "/logbook/api/vessels/{0}/dates/{1}".format(
                DAY_1["vessel"], DAY_1["date"]),
            format="json", follow=True
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["hours"]["count"], 3)
        self.assertEqual(len(content["hours"]["results"]), 3)
        self.assertEqual(
            content["hours"]["results"][0]["time"], self.hour_set_1[0].time)
        self.assertEqual(
            content["port_of_call"]["port_of_call_name"],
            self.day_1.port_of_call.port_of_call_name
        )

    def test_redirects_without_slash(self):
        response = self.client.get(
            "/logbook/api/vessels/{0}/dates/{1}".format(
                DAY_1["vessel"], DAY_1["date"]), format="json"
        )

        self.assertRedirects(
            response, "/logbook/api/vessels/{0}/dates/{1}/".format(
                DAY_1["vessel"], DAY_1["date"]),
            status_code=status.HTTP_301_MOVED_PERMANENTLY
        )

    def test_nonexistent_date(self):
        response = self.client.get(
            "/logbook/api/vessels/{0}/dates/{1}".format(
                DAY_1["vessel"], DAY_2["date"]),
            format="json", follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
