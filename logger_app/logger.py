#!/usr/bin/env python3
import logging
import time
from datetime import date
from threading import Thread

import schedule
from geopy.distance import vincenty

from .models import Day, Hour, Vessel, PortOfCall
from .sensors import Sensors

from timezonefinder import TimezoneFinder

logger = logging.getLogger("captains_log")


class LoggerJob(object):

    def __init__(self):
        self.timezone_finder = TimezoneFinder()
        self.sensor_array = Sensors(mock=True)
        try:
            self.vessel = Vessel.objects.latest(field_name="created_at")
        except Vessel.DoesNotExist as error:
            logger.debug("LoggerJob __init__ - {0}".format(error))
        try:
            most_recent_day = Day.objects.filter(
                vessel=self.vessel).latest("created_at")
        except (AttributeError, Day.DoesNotExist) as error:
            logger.warning(
                "Previous Day not found. One will be created "
                "at the beginning of the next hour if a vessel is defined "
                "at POST /vessel/"
            )
        try:
            previous_entry = Hour.objects.filter(
                day=most_recent_day).latest("created_at")
            self.update_sensor_array_by_previous_entry(previous_entry)

        except (UnboundLocalError, Hour.DoesNotExist) as error:
            logger.info(
                "Previous Hour entry not found. One will be created "
                "at the beginning of the next hour if a vessel is defined "
                "at POST /vessel/"
            )

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
        logger.debug("Sensor array updated - {0}".format(
            vars(self.sensor_array)))

    def create_daily_entry(self, today):
        try:
            port_of_call = PortOfCall.objects.latest(
                field_name="created_at")
        except PortOfCall.DoesNotExist:
            port_of_call = None
        current_day = Day.objects.create(
            vessel=self.vessel,
            date=today,
            total_distance_this_day=0,
            port_of_call=port_of_call,
            high_tide=213.4,
            low_tide=212.4,
            skipper="Shane"
        )
        logger.debug("Daily entry created - {0}".format(vars(current_day)))
        logger.info("Daily entry created - {0}".format(str(current_day)))

        return current_day

    def create_hourly_entry(
            self, current_day, hour, old_latitude, old_longitude):
        latitude = self.sensor_array.latitude
        longitude = self.sensor_array.longitude
        try:
            timezone = self.timezone_finder.timezone_at(
                lat=latitude, lng=longitude)
            if timezone is None:
                timezone = "UTC"
        except ValueError:
            timezone = "UTC"
        hourly_entry = Hour.objects.create(
            day=current_day,
            time=hour,
            course=self.sensor_array.course,
            speed=self.sensor_array.speed,
            latitude=latitude,
            longitude=longitude,
            weather="clear",
            wind_speed=self.sensor_array.wind_speed,
            wind_direction=self.sensor_array.wind_direction,
            visibility=self.sensor_array.visibility,
            engine_hours=self.sensor_array.engine_hours,
            fuel_level=self.sensor_array.fuel_level,
            water_level=self.sensor_array.water_level,
            distance_since_last_entry=self.distance_since_last_entry(
                old_latitude, old_longitude
            ),
            timezone=timezone
        )
        logger.debug("Hourly entry created - {0}".format(vars(hourly_entry)))
        logger.info("Hourly entry created - {0}".format(str(hourly_entry)))

        return hourly_entry

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
            self.vessel
        except AttributeError:
            try:
                self.vessel = Vessel.objects.latest(field_name="created_at")
            except Vessel.DoesNotExist as error:
                logger.error("{0}".format(error))
        try:
            old_latitude = self.sensor_array.latitude
            old_longitude = self.sensor_array.longitude
            self.sensor_array.update()
            today = date.today()
            current_day = Day.objects.filter(date=today, vessel=self.vessel)
            if len(current_day) < 1:
                current_day = self.create_daily_entry(today)
            else:
                current_day = current_day[0]
            self.create_hourly_entry(
                current_day, hour, old_latitude, old_longitude)
        except Exception as error:
            logger.error("Job during hour:{0} - {1}".format(hour, error))

    def initiate_hourly_entries(self):
        # # FIXME: below line
        # schedule.every(1).minutes.do(self.job, 5)
        for hour in range(24):  # 0, 23
            hour_string = str(hour)
            if len(hour_string) == 1:
                hour_string = "0" + hour_string  # "00", "23"
            schedule.every().day.at("{0}:00".format(hour_string)).do(
                self.job, hour)
        logger.debug("Hourly entry jobs created")

        hourly_entry_job = Thread(target=self.run_pending)
        logger.debug("Hourly entry thread created")
        hourly_entry_job.start()
        logger.debug("Hourly entry thread started")
