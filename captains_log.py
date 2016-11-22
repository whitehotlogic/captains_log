#!/usr/bin/env python3
import os
from config.config import CONFIG
from datetime import date

import schedule
from setup import run_setup

if os.path.isfile("config/config.py") is not True:
    run_setup()

from model.entry import Entry  # isort:skip  # noqa: E402

Entry(db_name="log.db").init_database()


def job(hour):
    reload(CONFIG)  # make sure vessel info is updated
    vessel_name = CONFIG["vessel_name"]
    if Entry.daily_entry_exists(date.today(), vessel_name) is False:
        Entry(db_name="log.db").insert_daily_entry(
            vessel=CONFIG["vessel_name"], date=date.today(),
            skipper="Skipper Name", time=hour, engine_type="diesel"
        )
    Entry(db_name="log.db").insert_hourly_entry(
        time=hour, latitude=latitude,
        longitude=longitude, course=direction, date=date.today(),
        wind_speed=wind_speed, wind_direction=wind_direction,
        visibility=visibility
    )

for hour in range(24):  # 0, 23
    hour_string = str(hour)
    if len(hour_string) == 1:
        hour_string = "0" + hour_string  # "00", "23"
    schedule.every().day.at(hour_string + ":00").do(job, hour)

while True:
    schedule.run_pending()

# TODO: create vessel entry if not exists
# TODO: every hour create an entry
# TODO: 1) if day not exists create it - 2) if hour == 0, create new day
