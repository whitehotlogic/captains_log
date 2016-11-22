#!/usr/bin/env python3
import schedule

from datetime import datetime

from model.entry import Entry

Entry(db_name="log.db").init_database()

def job(n):
    print(n)

for hour in range(24):
    hour = str(hour)
    if len(hour) == 1:
        hour = "0" + hour
    schedule.every().day.at(hour + ":00").do(job, hour)

while True:
    schedule.run_pending()

# TODO: create vessel entry if not exists
# TODO: every hour create an entry
# TODO: 1) if day not exists create it - 2) if hour == 0, create new day
