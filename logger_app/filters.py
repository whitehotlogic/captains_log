from django_filters import rest_framework as filters
from django_filters import widgets
from .models import Day, Vessel, Hour, PortOfCall


class VesselFilter(filters.FilterSet):

    class Meta:
        model = Vessel
        fields = [
            "name", "owner_name", "hull_number", "engine_manufacturer",
            "engine_number", "engine_type", "owner_certification_agency",
            "owner_certification_number", "created_at"
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
