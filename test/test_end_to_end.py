import config
import os
import shutil
import sys
import unittest
from datetime import date, timedelta
from unittest.runner import TextTestResult

from mocks.position import POSITION as MOCK_POSITION
from mocks.weather import WEATHER as MOCK_WEATHER

TextTestResult.getDescription = lambda _, test: test.shortDescription()

if os.path.isfile("config/config.py") is not True:
    shutil.copyfile("config/config_example.py", "config/config.py")
    reload(config)

try:
    from model.entry import Entry
except ImportError:
    sys.path.append("..")
    from model.entry import Entry


try:
    unicode
except NameError:
    unicode = str  # python3 compatibility

DAYS_TO_SIMULATE = 10


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        if os.path.isfile("test.db") is True:
            os.remove("test.db")
        print("Creating database...")
        Entry(db_name="test.db").init_database()
        print("Database created")
        print("Creating vessel entry...")
        Entry(db_name="test.db").insert_vessel_info(
            name=config.config.CONFIG["vessel_name"],
            hull_number=config.config.CONFIG["hull_number"],
            uscg_number=config.config.CONFIG["uscg_number"],
            fuel_capacity=config.config.CONFIG["fuel_capacity"],
            water_capacity=config.config.CONFIG["water_capacity"],
            battery_capacity=config.config.CONFIG["battery_capacity"],
            engine_manufacturer=config.config.CONFIG["engine_manufacturer"],
            engine_number=config.config.CONFIG["engine_number"],
            owner_name=config.config.CONFIG["owner_name"],
            owner_certification_agency=config.config.CONFIG[
                "owner_certification_agency"],
            owner_certification_number=config.config.CONFIG[
                "owner_certification_number"], engine_type="diesel")

        """    Creating entries for {0} days...""".format(DAYS_TO_SIMULATE)

        direction = 215  # southwest
        position = None
        wind_speed = None
        wind_direction = None
        visibility = None
        latitude, longitude = 37.781400, -122.514760  # San Francisco

        for day in range(DAYS_TO_SIMULATE):  # create hourly entry
            for hour in range(24):
                if hour == 0:  # create daily entry
                    Entry(db_name="test.db").insert_daily_entry(
                        vessel=config.config.CONFIG["vessel_name"],
                        date=date.today() + timedelta(days=day),
                        skipper="Skipper Name", time=hour,
                        port_of_call_start="START", port_of_call_end="END",
                        high_tide=0.1, low_tide=1.1)
                speed = MOCK_POSITION["speed"]()
                direction = MOCK_POSITION["direction"](
                    last_direction=direction)
                wind_speed = MOCK_WEATHER["wind_speed"](
                    last_wind_speed=wind_speed)
                wind_direction = MOCK_WEATHER["wind_direction"](
                    last_wind_direction=wind_direction)
                visibility = MOCK_WEATHER["visibility"](
                    last_visibility=visibility)
                Entry(db_name="test.db").insert_hourly_entry(
                    time=hour, latitude=latitude,
                    longitude=longitude, course=direction,
                    date=date.today() + timedelta(days=day),
                    wind_speed=wind_speed, wind_direction=wind_direction,
                    visibility=visibility)
                new_position = MOCK_POSITION["lat_lon"](
                    last_latitude=latitude, last_longitude=longitude,
                    speed=speed, last_direction=direction)
                position = new_position
                latitude = position["latitude"]
                longitude = position["longitude"]

        for day in range(DAYS_TO_SIMULATE):  # update total distance each day
            Entry(db_name="test.db").update_total_distance_daily_entry(
                date.today() + timedelta(days=day))

    @classmethod
    def tearDownClass(self):
        pass
        # os.remove("test.db")

    def test_number_of_records(self):
        number_of_vessels = Entry(db_name="test.db").get_count_from_table(
            "vessel")

        self.assertEqual(number_of_vessels, 1)

        number_of_days = Entry(db_name="test.db").get_count_from_table(
            "day")

        self.assertEqual(number_of_days, DAYS_TO_SIMULATE)

        number_of_hours = Entry(db_name="test.db").get_count_from_table(
            "hour")

        self.assertEqual(number_of_hours, DAYS_TO_SIMULATE * 24)

    def test_vessel_data(self):
        print("    Test data types in vessel...")
        vessel_info = Entry(db_name="test.db").get_vessel_info(1)

        name = vessel_info[0]
        hull_number = vessel_info[1]
        uscg_number = vessel_info[2]
        fuel_capacity = vessel_info[3]
        water_capacity = vessel_info[4]
        battery_capacity = vessel_info[5]
        engine_manufacturer = vessel_info[6]
        engine_number = vessel_info[7]
        engine_type = vessel_info[8]
        owner_name = vessel_info[9]
        owner_certification_agency = vessel_info[10]
        owner_certification_number = vessel_info[11]

        self.assertEqual(type(name), unicode)
        self.assertEqual(type(hull_number), int)
        self.assertEqual(type(uscg_number), int)
        self.assertEqual(type(fuel_capacity), int)
        self.assertEqual(type(water_capacity), int)
        self.assertEqual(type(battery_capacity), int)
        self.assertEqual(type(engine_manufacturer), unicode)
        self.assertEqual(type(engine_number), int)
        self.assertEqual(type(engine_type), unicode)
        self.assertEqual(type(owner_name), unicode)
        self.assertEqual(type(owner_certification_agency), unicode)
        self.assertEqual(type(owner_certification_number), unicode)

    def test_day_data(self):
        print("    Test data types in day...")
        day_info = Entry(db_name="test.db").get_day_info(1)

        vessel_id = day_info[0]
        current_date = day_info[1]
        port_of_call_start = day_info[2]
        port_of_call_end = day_info[3]
        total_distance_this_day = day_info[4]
        high_tide = day_info[5]
        low_tide = day_info[6]
        skipper = day_info[7]

        self.assertEqual(type(vessel_id), int)
        self.assertEqual(type(current_date), unicode)
        self.assertEqual(type(port_of_call_start), unicode)
        self.assertEqual(type(port_of_call_end), unicode)
        self.assertEqual(type(total_distance_this_day), float)
        self.assertEqual(type(high_tide), float)
        self.assertEqual(type(low_tide), float)
        self.assertEqual(type(skipper), unicode)

    def test_hour_data(self):
        print("    Test data types in hour...")
        hour_info = Entry(db_name="test.db").get_hour_info(2)

        day_id = hour_info[0]
        current_time = hour_info[1]
        course = hour_info[2]
        latitude = hour_info[3]
        longitude = hour_info[4]
        weather = hour_info[5]
        wind_speed = hour_info[6]
        wind_direction = hour_info[7]
        visibility = hour_info[8]
        engine_hours = hour_info[9]
        fuel_level = hour_info[10]
        water_level = hour_info[11]
        distance_since_last_entry = hour_info[12]

        self.assertEqual(type(day_id), int)
        self.assertEqual(type(current_time), int)
        self.assertEqual(type(course), int)
        self.assertEqual(type(latitude), float)
        self.assertEqual(type(longitude), float)
        self.assertEqual(type(weather), type(None))
        self.assertEqual(type(wind_speed), int)
        self.assertEqual(type(wind_direction), int)
        self.assertEqual(type(visibility), int)
        self.assertEqual(type(engine_hours), type(None))
        self.assertEqual(type(fuel_level), type(None))
        self.assertEqual(type(water_level), type(None))
        if distance_since_last_entry == 0:  # distance may be zero
            self.assertEqual(type(distance_since_last_entry), int)
        else:  # sqlite stores 0.0 as 0
            self.assertEqual(type(distance_since_last_entry), float)


if __name__ == '__main__':
    unittest.main()
