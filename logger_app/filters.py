from django_filters import rest_framework as filters
from django_filters import widgets
from .models import Day, Vessel, Hour


class VesselFilter(filters.FilterSet):
    created_at = date_range = filters.DateFromToRangeFilter(widget=widgets.RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Vessel
        fields = [
            'name', 'owner_name', 'hull_number', 'engine_manufacturer',
            'engine_number', 'engine_type', 'owner_certification_agency',
            'owner_certification_number', 'created_at'
        ]


class DayFilter(filters.FilterSet):
    created_at = filters.IsoDateTimeFilter()

    class Meta:
        model = Day
        fields = [
            'vessel_id', 'date', 'port_of_call_start', 'port_of_call_end',
            'skipper', 'created_at'
        ]


class HourFilter(filters.FilterSet):

    class Meta:
        model = Hour
        fields = [
            'day_id', 'time', 'created_at'
        ]
