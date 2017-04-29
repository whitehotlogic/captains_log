# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


class Vessel(models.Model):
    name = models.CharField(max_length=255, null=False)
    hull_number = models.CharField(max_length=255, null=False)
    fuel_capacity = models.FloatField(null=False)
    water_capacity = models.FloatField(null=False)
    battery_capacity = models.FloatField(null=False)
    engine_manufacturer = models.CharField(max_length=255)
    engine_number = models.CharField(max_length=255)
    engine_type = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    owner_certification_agency = models.CharField(max_length=255)
    owner_certification_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}, owned by {1}".format(self.name, self.owner_name)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["hull_number"]),
            models.Index(fields=["owner_certification_agency"]),
            models.Index(fields=["owner_certification_number"]),
            models.Index(fields=["owner_name"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"


class PortOfCall(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    notes = models.CharField(max_length=1024, default="", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} at ({1}, {2})".format(
            self.name, self.latitude, self.longitude)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"


class Day(models.Model):
    vessel = models.ForeignKey(Vessel, null=False)
    port_of_call = models.ForeignKey(PortOfCall, null=True)
    date = models.DateField(null=False, blank=False)
    total_distance_this_day = models.FloatField(default=0.0)
    high_tide = models.FloatField()
    low_tide = models.FloatField()
    skipper = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1}:{2}, skippered by {3} on {4}".format(
            self.vessel.name, self.vessel.owner_certification_agency,
            self.vessel.owner_certification_number, self.skipper, self.date
        )

    class Meta:
        indexes = [
            models.Index(fields=["vessel"]),
            models.Index(fields=["date"]),
            models.Index(fields=["port_of_call"]),
            models.Index(fields=["skipper"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"


class Hour(models.Model):
    day = models.ForeignKey(Day, null=False)
    time = models.IntegerField(null=False)
    course = models.IntegerField()
    speed = models.IntegerField()
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    weather = models.CharField(max_length=255)
    wind_speed = models.FloatField()
    wind_direction = models.IntegerField()
    visibility = models.IntegerField()
    engine_hours = models.FloatField()
    fuel_level = models.FloatField()
    water_level = models.FloatField()
    distance_since_last_entry = models.FloatField(null=False)
    timezone = models.CharField(max_length=100, default="UTC", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        time_tuple = (
            self.day.date.year, self.day.date.month, self.day.date.day,
            self.time)
        datetime_object = datetime(*time_tuple)
        return "{0} - {1}:{2} at {3}".format(
            self.day.vessel.name, self.day.vessel.owner_certification_agency,
            self.day.vessel.owner_certification_number, datetime_object
        )

    class Meta:
        indexes = [
            models.Index(fields=["day"]),
            models.Index(fields=["time"]),
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["weather"]),
            models.Index(fields=["wind_speed", "wind_direction"]),
            models.Index(fields=["engine_hours"]),
            models.Index(fields=["fuel_level"]),
            models.Index(fields=["water_level"]),
            models.Index(fields=["visibility"]),
            models.Index(fields=["distance_since_last_entry"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"


class Note(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=False)
    vessel = models.ForeignKey(Vessel, null=False)
    note = models.CharField(max_length=1024, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["note"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"
