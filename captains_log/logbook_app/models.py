# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords


class Crew(models.Model):
    crew_name = models.CharField(max_length=255, null=False)
    crew_user = models.OneToOneField(
        User, null=True,
        help_text="Optionally associate a crew member with a user account"
    )
    can_skipper = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.can_skipper:
            return "{0} (can skipper)".format(self.crew_name)
        else:
            return self.name

    class Meta:
        indexes = [
            models.Index(fields=["crew_name"]),
            models.Index(fields=["can_skipper"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["can_skipper", "is_active"]),
        ]


class Vessel(models.Model):
    vessel_name = models.CharField(max_length=255, null=False)
    model = models.CharField(max_length=100, null=True)
    manufacturer = models.CharField(max_length=100, null=True)
    length = models.DecimalField(
        max_digits=5, decimal_places=1, null=False,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    draft = models.DecimalField(
        max_digits=5, decimal_places=1, null=False,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    hull_number = models.CharField(max_length=255, null=False)
    engine_manufacturer = models.CharField(max_length=255, null=True)
    engine_number = models.CharField(max_length=255, null=True)
    engine_type = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(Crew, null=True, related_name="vessel_owner")
    skipper = models.OneToOneField(
        Crew, null=True, related_name="vessel_skipper", db_column="skipper")
    owner_certification_agency = models.CharField(max_length=255)
    owner_certification_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True)
    history = HistoricalRecords()

    def __str__(self):
        if self.skipper is not None:
            return "{0}, owned by {1}, current skipper: {2}".format(
                self.vessel_name, self.owner, self.skipper.crew_name)
        else:
            return "{0}, owned by {1}".format(self.name, self.owner)

    class Meta:
        indexes = [
            models.Index(fields=["vessel_name"]),
            models.Index(fields=["manufacturer"]),
            models.Index(fields=["model"]),
            models.Index(fields=["hull_number"]),
            models.Index(fields=["owner_certification_agency"]),
            models.Index(fields=["owner_certification_number"]),
            models.Index(fields=["owner"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"


class Provision(models.Model):
    provision_name = models.CharField(max_length=255, null=False)
    measurement_name = models.CharField(
        max_length=255, null=False,
        help_text="Example: gallons / loaves / cans"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}, measured in: {1}".format(
            self.provision_name, self.measurement_name)


class Supply(models.Model):  # extend Vessel
    vessel = models.ForeignKey(Vessel)
    fuel = models.DecimalField(
        max_digits=5, decimal_places=2, null=False,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Measured in gallons"
    )
    water = models.DecimalField(
        max_digits=5, decimal_places=2, null=False,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Measured in gallons"
    )
    battery = models.DecimalField(
        max_digits=5, decimal_places=2, null=False,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Measured in Voltage"
    )
    provisions = models.ManyToManyField(Provision, through='SupplyProvision')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{0}".format(self.vessel.vessel_name)


class SupplyProvision(models.Model):
    supply = models.ForeignKey(Supply)
    provision = models.ForeignKey(Provision)
    quantity = models.DecimalField(
        max_digits=5, decimal_places=2, null=False,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} for {1}".format(
            self.provision.provision_name, self.supply.vessel)

    indexes = [
        models.Index(fields=["supply"]),
        models.Index(fields=["provision"]),
        models.Index(fields=["created_at"]),
    ]


class PortOfCall(models.Model):
    port_of_call_name = models.CharField(max_length=255)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    notes = models.CharField(max_length=1024, default="", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{0} at ({1}, {2})".format(
            self.port_of_call_name, self.latitude, self.longitude)

    class Meta:
        indexes = [
            models.Index(fields=["port_of_call_name"]),
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"


class Trip(models.Model):
    trip_name = models.CharField(max_length=255)
    vessels = models.ManyToManyField(Vessel, blank=False)
    start_date = models.DateField(null=False, default=date.today)
    end_date = models.DateField(null=True)
    starting_port = models.ForeignKey(
        PortOfCall, null=False, related_name="trip_starting_port")
    crew = models.ManyToManyField(Crew, blank=False)
    stops = models.ManyToManyField(PortOfCall, blank=True)
    destination_port = models.ForeignKey(
        PortOfCall, null=False, related_name="trip_destination_port")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{0}".format(self.trip_name)

    class Meta:
        indexes = [
            models.Index(fields=["trip_name"]),
            models.Index(fields=["start_date"]),
            models.Index(fields=["end_date"]),
            models.Index(fields=["starting_port"]),
            models.Index(fields=["destination_port"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]
        unique_together = ("starting_port", "destination_port",)


class Day(models.Model):
    trip = models.ForeignKey(Trip, null=True)
    vessel = models.ForeignKey(Vessel, null=False)
    port_of_call = models.ForeignKey(PortOfCall, null=True)
    date = models.DateField(null=False, blank=False)
    total_distance_this_day = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, default=0.0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    high_tide = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    low_tide = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} - {1}:{2}, on {3}".format(
            self.vessel.vessel_name, self.vessel.owner_certification_agency,
            self.vessel.owner_certification_number, self.date
        )

    class Meta:
        indexes = [
            models.Index(fields=["vessel"]),
            models.Index(fields=["date"]),
            models.Index(fields=["port_of_call"]),
            models.Index(fields=["created_at"]),
        ]
        get_latest_by = "created_at"


class Hour(models.Model):
    day = models.ForeignKey(Day, null=False)
    time = models.IntegerField(
        null=False, help_text="0 through 23",
        validators=[MinValueValidator(0), MaxValueValidator(23)]
    )
    course = models.IntegerField()
    speed = models.IntegerField()
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    weather = models.CharField(max_length=255)
    wind_speed = models.FloatField()
    wind_direction = models.IntegerField()
    visibility = models.IntegerField()
    engine_hours = models.FloatField()
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
            self.day.vessel.vessel_name,
            self.day.vessel.owner_certification_agency,
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
