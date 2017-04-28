# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['hull_number']),
            models.Index(fields=['owner_certification_agency']),
            models.Index(fields=['owner_certification_number']),
            models.Index(fields=['owner_name']),
            models.Index(fields=['created_at']),
        ]


class Day(models.Model):
    vessel = models.ForeignKey(Vessel, null=False)
    date = models.DateField(null=False, blank=False, auto_now_add=True)
    port_of_call_start = models.CharField(max_length=255)
    port_of_call_end = models.CharField(max_length=255)
    total_distance_this_day = models.FloatField()
    high_tide = models.FloatField()
    low_tide = models.FloatField()
    skipper = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['vessel']),
            models.Index(fields=['date']),
            models.Index(fields=['port_of_call_start', 'port_of_call_end']),
            models.Index(fields=['skipper']),
            models.Index(fields=['created_at']),
        ]


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['day']),
            models.Index(fields=['time']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['weather']),
            models.Index(fields=['wind_speed', 'wind_direction']),
            models.Index(fields=['engine_hours']),
            models.Index(fields=['fuel_level']),
            models.Index(fields=['water_level']),
            models.Index(fields=['visibility']),
            models.Index(fields=['distance_since_last_entry']),
            models.Index(fields=['created_at']),
        ]


class Note(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=False)
    vessel = models.ForeignKey(Vessel, null=False)
    note = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['note']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['created_at']),
        ]
