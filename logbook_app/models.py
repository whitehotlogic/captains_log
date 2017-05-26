# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from simple_history.models import HistoricalRecords


class Crew(models.Model):
    name = models.CharField(max_length=255, null=False)
    can_skipper = models.BooleanField(default=False)

    def __str__(self):
        if self.can_skipper:
            return "Skipper: {0}".format(self.name)
        else:
            return self.name


class Vessel(models.Model):
    name = models.CharField(max_length=255, null=False)
    model = models.CharField(max_length=100, null=True)
    manufacturer = models.CharField(max_length=100, null=True)
    length = models.FloatField(null=False)
    draft = models.FloatField(null=False)
    hull_number = models.CharField(max_length=255, null=False)
    fuel_capacity = models.FloatField(null=False)
    water_capacity = models.FloatField(null=False)
    battery_capacity = models.FloatField(null=False)
    engine_manufacturer = models.CharField(max_length=255, null=True)
    engine_number = models.CharField(max_length=255, null=True)
    engine_type = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(Crew, null=False, related_name="vessel_owner")
    skipper = models.OneToOneField(
        Crew, null=False, related_name="vessel_skipper", db_column="skipper")
    owner_certification_agency = models.CharField(max_length=255)
    owner_certification_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{0}, owned by {1}".format(self.name, self.owner)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["manufacturer"]),
            models.Index(fields=["model"]),
            models.Index(fields=["hull_number"]),
            models.Index(fields=["owner_certification_agency"]),
            models.Index(fields=["owner_certification_number"]),
            models.Index(fields=["owner"]),
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
    history = HistoricalRecords()

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


class Trip(models.Model):
    name = models.CharField(max_length=255)
    vessels = models.ManyToManyField(Vessel)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=True)
    starting_port = models.ForeignKey(
        PortOfCall, null=False, related_name="trip_starting_port")
    stops = models.ManyToManyField(PortOfCall, blank=True)
    destination_port = models.ForeignKey(
        PortOfCall, null=False, related_name="trip_destination_port")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        indexes = [

        ]
        unique_together = ("starting_port", "destination_port",)


class Day(models.Model):
    trip = models.ForeignKey(Trip, null=True)
    vessel = models.ForeignKey(Vessel, null=False)
    port_of_call = models.ForeignKey(PortOfCall, null=True)
    date = models.DateField(null=False, blank=False)
    total_distance_this_day = models.FloatField(default=0.0)
    high_tide = models.FloatField()
    low_tide = models.FloatField()
    skipper = models.OneToOneField(
        Vessel, null=False, to_field="skipper",
        related_name="day_skipper", unique=True)
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
    note = models.CharField(max_length=1024, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["note"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"
