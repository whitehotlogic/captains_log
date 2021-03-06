import logging
from datetime import datetime, timedelta

from captains_log.logbook_app.logbook import Logbook
from captains_log.logbook_app.models import Crew, Day, Hour, PortOfCall, Vessel
from django.test import TestCase

from .config.portofcall_config import PORT_OF_CALL_1
from .config.vessel_config import VESSEL_1
from .config.crew_config import CREW_1


class ManyEntriesTests(TestCase):

    def setUp(self):
        self.DAYS_TO_TEST = 100
        logger = logging.getLogger("captains_log")
        logger.setLevel(logging.ERROR)
        crew = Crew.objects.create(**CREW_1)
        VESSEL_1["owner"] = crew
        VESSEL_1["skipper"] = crew
        Vessel.objects.create(**VESSEL_1)
        PortOfCall.objects.create(**PORT_OF_CALL_1)
        self.logbook = Logbook()
        self.logbook.sensor_array.update()
        today = datetime.today() - timedelta(days=1)
        for day in range(self.DAYS_TO_TEST):
            today += timedelta(days=1)
            current_day = self.logbook.create_daily_entry(today)
            for hour in range(24):
                self.logbook.create_hourly_entry(
                    current_day, hour, self.logbook.sensor_array.latitude,
                    self.logbook.sensor_array.longitude
                )
                self.logbook.sensor_array.update()

    def tearDown(self):
        Hour.objects.all().delete()
        Day.objects.all().delete()
        PortOfCall.objects.all().delete()
        Vessel.objects.all().delete()
        Crew.objects.all().delete()

    def test_many_entries_exist(self):
        crew = Crew.objects.all()
        vessels = Vessel.objects.all()
        ports_of_call = PortOfCall.objects.all()
        days = Day.objects.all()
        hours = Hour.objects.all()

        self.assertEqual(crew.count(), 1)
        self.assertEqual(vessels.count(), 1)
        self.assertEqual(ports_of_call.count(), 1)
        self.assertEqual(days.count(), self.DAYS_TO_TEST)
        self.assertEqual(hours.count(), self.DAYS_TO_TEST * 24)
