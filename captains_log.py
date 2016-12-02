#!/usr/bin/env python3
import config.config as config
import os
import sqlite3
import time
from datetime import date
from threading import Thread

import schedule
from mocks.position import POSITION as MOCK_POSITION
from mocks.weather import WEATHER as MOCK_WEATHER
from setup import run_setup

if os.path.isfile("config/config.py") is not True:
    run_setup()

from model.entry import Entry  # isort:skip  # noqa: E402

entry = Entry(db_name="log.db")

entry.init_database()


def add_vessel_entry():
    try:
        entry.insert_vessel_info(
            name=config.CONFIG["vessel_name"],
            hull_number=config.CONFIG["hull_number"],
            uscg_number=config.CONFIG["uscg_number"],
            fuel_capacity=config.CONFIG["fuel_capacity"],
            water_capacity=config.CONFIG["water_capacity"],
            battery_capacity=config.CONFIG["battery_capacity"],
            engine_manufacturer=config.CONFIG["engine_manufacturer"],
            engine_number=config.CONFIG["engine_number"],
            owner_name=config.CONFIG["owner_name"],
            owner_certification_agency=config.CONFIG[
                "owner_certification_agency"],
            owner_certification_number=config.CONFIG[
                "owner_certification_number"], engine_type="diesel")
    except sqlite3.IntegrityError:  # vessel entry already exists
        pass


vessel_name = config.CONFIG["vessel_name"]

port_of_call_start = "START"
port_of_call_end = "END"
high_tide = 45.45
low_tide = 23.23
skipper = "Shane"
current_date = date.today()
direction = 215  # southwest
position = None
wind_speed = None
wind_direction = None
visibility = None
latitude, longitude = 37.781400, -122.514760  # San Francisco


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


def job(hour):
    reload(config)  # make sure vessel info is updated
    print(hour)
    global latitude, longitude
    global direction, wind_speed, wind_direction, visibility, vessel_name

    speed = MOCK_POSITION["speed"]()
    direction = MOCK_POSITION["direction"](
        last_direction=direction)
    wind_speed = MOCK_WEATHER["wind_speed"](
        last_wind_speed=wind_speed)
    wind_direction = MOCK_WEATHER["wind_direction"](
        last_wind_direction=wind_direction)
    visibility = MOCK_WEATHER["visibility"](
        last_visibility=visibility)
    add_vessel_entry()
    if (entry.daily_entry_exists(  # don't create superfluous daily entries
            current_date, config.CONFIG["vessel_name"]) is False):
        entry.insert_daily_entry(
            vessel=vessel_name, date=date.today(),
            skipper="Skipper Name", time=hour, engine_type="diesel")
    new_position = MOCK_POSITION["lat_lon"](
        last_latitude=latitude, last_longitude=longitude,
        speed=speed, last_direction=direction)
    position = new_position
    latitude = position["latitude"]
    longitude = position["longitude"]
    entry.insert_hourly_entry(
        time=hour, latitude=latitude,
        longitude=longitude, course=direction, date=date.today(),
        wind_speed=wind_speed, wind_direction=wind_direction,
        visibility=visibility)

for hour in range(24):  # 0, 23
    hour_string = str(hour)
    if len(hour_string) == 1:
        hour_string = "0" + hour_string  # "00", "23"
    schedule.every().day.at(hour_string + ":00").do(job, hour)

Thread(target=main).start()
