import os
import sys
import unittest
import config
from datetime import date, timedelta
from mocks.position import POSITION as MOCK_POSITION
import shutil

if os.path.isfile("config/config.py") is not True:
    shutil.copyfile("config/config_example.py", "config/config.py")
    reload(config)


try:
    from model.entry import Entry
except ImportError:
    sys.path.append("..")
    from model.entry import Entry


class TestDatabase(unittest.TestCase):

    def setUp(self):
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
                "owner_certification_number"]
        )

    def tearDown(self):
        pass
        # os.remove("test.db")

    def test_create_false_entries(self):
        print("    Creating entries...")
        Entry(db_name="test.db").init_database()

        direction = 215  # southwest
        position = None
        latitude, longitude = 37.781400, -122.514760  # San Francisco

        for day in range(10):
            for hour in range(24):
                if hour == 0:
                    Entry(db_name="test.db").insert_daily_entry(
                        vessel=config.config.CONFIG["vessel_name"],
                        date=date.today() + timedelta(days=day),
                        skipper="Skipper Name", time=hour
                    )
                speed = MOCK_POSITION["speed"]()
                direction = MOCK_POSITION["direction"](
                    last_direction=direction)
                Entry(db_name="test.db").insert_hourly_entry(
                    time=hour, latitude=latitude,
                    longitude=longitude, course=direction, speed=speed,
                    date=date.today() + timedelta(days=day)
                )
                new_position = MOCK_POSITION["lat_lon"](
                    last_latitude=latitude, last_longitude=longitude,
                    speed=speed, last_direction=direction)
                position = new_position
                latitude = position["latitude"]
                longitude = position["longitude"]

        for day in range(10):
            Entry(db_name="test.db").update_total_distance_daily_entry(
                        date.today() + timedelta(days=day))





if __name__ == '__main__':
    unittest.main()