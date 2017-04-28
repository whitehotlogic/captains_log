#!/usr/bin/env python3
import time
from datetime import date, datetime
from threading import Thread

import schedule
from django.forms.models import model_to_dict
from geopy.distance import vincenty

from .models import Day, Hour, Note, Vessel
from .sensors import Sensors


class LoggerJob(object):
    def __init__(self):
        self.vessel = Vessel.objects.get(pk=1)
        self.sensor_array = Sensors(mock=True)
        try:
            most_recent_day = Day.objects.filter(
                vessel=self.vessel).latest('created_at')
            previous_entry = Hour.objects.filter(
                day=most_recent_day).latest('created_at')
            self.update_sensor_array_by_previous_entry(previous_entry)
        except (Day.DoesNotExist, Hour.DoesNotExist):
            pass

    def update_sensor_array_by_previous_entry(self, previous_entry):
        self.sensor_array.latitude = previous_entry.latitude
        self.sensor_array.longitude = previous_entry.longitude
        self.sensor_array.course = previous_entry.course
        self.sensor_array.speed = previous_entry.speed
        self.sensor_array.fuel_level = previous_entry.fuel_level
        self.sensor_array.water_level = previous_entry.water_level
        self.sensor_array.weather = previous_entry.weather
        self.sensor_array.wind_speed = previous_entry.wind_speed
        self.sensor_array.wind_direction = previous_entry.wind_direction
        self.sensor_array.visibility = previous_entry.visibility
        self.sensor_array.engine_hours = previous_entry.engine_hours

    def run_pending(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def distance_since_last_entry(self, old_latitude, old_longitude):
        if old_latitude is None or old_latitude is None:
            return 0
        distance = vincenty(
            (old_latitude, old_longitude),
            (self.sensor_array.latitude, self.sensor_array.longitude)
        ).miles * 0.868976
        return distance

    def job(self, hour):
        try:
            old_latitude = self.sensor_array.latitude
            old_longitude = self.sensor_array.longitude
            self.sensor_array.update()
            today = date.today()
            current_day = Day.objects.filter(date=today, vessel=self.vessel)
            if len(current_day) < 1:
                current_day = Day.objects.create(
                    vessel=self.vessel,
                    date=today,
                    port_of_call_start="Maldives",
                    port_of_call_end="Maldives",
                    total_distance_this_day=2312312.4,
                    high_tide=213.4,
                    low_tide=212.4,
                    skipper="Shane"
                )
            else:
                current_day = current_day[0]
            Hour.objects.create(
                day=current_day,
                time=hour,
                course=self.sensor_array.course,
                speed=self.sensor_array.speed,
                latitude=self.sensor_array.latitude,
                longitude=self.sensor_array.longitude,
                weather="clear",
                wind_speed=self.sensor_array.wind_speed,
                wind_direction=self.sensor_array.wind_direction,
                visibility=self.sensor_array.visibility,
                engine_hours=self.sensor_array.engine_hours,
                fuel_level=self.sensor_array.fuel_level,
                water_level=self.sensor_array.water_level,
                distance_since_last_entry=self.distance_since_last_entry(
                    old_latitude, old_longitude
                )
            )
        except Exception as error:
            print error

    def initiate_hourly_entries(self):
        # # FIXME: below line
        # schedule.every(1).minutes.do(self.job, 5)
        for hour in range(24):  # 0, 23
            hour_string = str(hour)
            if len(hour_string) == 1:
                hour_string = "0" + hour_string  # "00", "23"
            schedule.every().day.at("{0}:00".format(hour_string)).do(
                self.job, hour)

        hourly_entry_job = Thread(target=self.run_pending)
        hourly_entry_job.start()
