from django_filters import rest_framework as filters

from .models import Crew, Day, Hour, PortOfCall, Trip, Vessel


class CrewFilter(filters.FilterSet):

    class Meta:
        model = Crew
        fields = [
            "name", "can_skipper"
        ]


class VesselFilter(filters.FilterSet):

    class Meta:
        model = Vessel
        fields = [
            "name", "owner", "skipper", "manufacturer", "model", "hull_number",
            "engine_manufacturer", "engine_number", "engine_type",
            "owner_certification_agency", "owner_certification_number",
            "created_at"
        ]


class TripFilter(filters.FilterSet):

    class Meta:
        model = Trip
        fields = [
            "name", "vessels", "starting_port", "stops", "destination_port",
            "start_date", "end_date", "created_at", "updated_at"
        ]


class PortOfCallFilter(filters.FilterSet):

    class Meta:
        model = PortOfCall
        fields = [
            "name", "latitude", "longitude", "created_at"
        ]


class DayFilter(filters.FilterSet):

    class Meta:
        model = Day
        fields = [
            "vessel_id", "date", "skipper", "created_at"
        ]


class HourFilter(filters.FilterSet):

    class Meta:
        model = Hour
        fields = [
            "day_id", "time", "created_at"
        ]
