from captains_log.logbook_app.models import (Crew, Day, Hour, PortOfCall,
                                             Provision, Supply,
                                             SupplyProvision, Trip, Vessel)
from django_filters import rest_framework as filters


class CrewFilter(filters.FilterSet):

    class Meta:
        model = Crew
        fields = [
            "crew_name", "can_skipper"
        ]


class VesselFilter(filters.FilterSet):

    class Meta:
        model = Vessel
        fields = [
            "vessel_name", "owner", "skipper", "manufacturer", "model",
            "hull_number", "engine_manufacturer", "engine_number",
            "engine_type", "certification_agency",
            "certification_number", "created_at"
        ]


class ProvisionFilter(filters.FilterSet):

    class Meta:
        model = Provision
        fields = [
            "provision_name", "created_at", "updated_at"
        ]


class SupplyFilter(filters.FilterSet):

    class Meta:
        model = Supply
        fields = [
            "vessel", "fuel", "water", "battery"
        ]


class SupplyProvisionFilter(filters.Filter):

    class Meta:
        model = SupplyProvision
        fields = [
            "supply", "provision"
        ]


class TripFilter(filters.FilterSet):

    class Meta:
        model = Trip
        fields = [
            "trip_name", "vessels", "starting_port", "stops", "destination_port",
            "start_date", "end_date", "created_at", "updated_at"
        ]


class PortOfCallFilter(filters.FilterSet):

    class Meta:
        model = PortOfCall
        fields = [
            "port_of_call_name", "latitude", "longitude", "created_at"
        ]


class DayFilter(filters.FilterSet):

    class Meta:
        model = Day
        fields = [
            "vessel_id", "date", "created_at"
        ]


class HourFilter(filters.FilterSet):

    class Meta:
        model = Hour
        fields = [
            "day_id", "time", "created_at"
        ]
