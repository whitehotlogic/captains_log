from drf_queryfields import QueryFieldsMixin
from models import Crew, Day, Hour, Note, PortOfCall, Trip, Vessel
from rest_framework.serializers import (DateField, HyperlinkedModelSerializer,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField)
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin


class CrewSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):

        class Meta:
            model = Crew
            fields = (
                "id", "url", "name", "can_skipper"
            )


class VesselSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):

    class Meta:
        model = Vessel
        fields = (
            "id", "url", "name", "manufacturer", "length", "draft", "model",
            "hull_number", "fuel_capacity", "water_capacity",
            "battery_capacity", "engine_manufacturer", "engine_number",
            "engine_type", "owner", "skipper", "owner_certification_agency",
            "owner_certification_number", "image", "created_at", "updated_at"
        )


class VesselHistorySerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Vessel
        fields = (
            "id", "name", "manufacturer", "length", "draft", "model",
            "hull_number", "fuel_capacity", "water_capacity",
            "battery_capacity", "engine_manufacturer", "engine_number",
            "engine_type", "owner", "skipper", "owner_certification_agency",
            "owner_certification_number", "created_at", "updated_at"
        )


class PortOfCallSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):

    class Meta:
        model = PortOfCall
        fields = (
            "id", "url", "name", "latitude", "longitude", "notes",
            "created_at", "updated_at"
        )


class TripSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):

    class Meta:
        model = Trip
        fields = (
            "id", "url", "name", "vessels", "start_date", "end_date",
            "starting_port", "stops", "destination_port",
            "created_at", "updated_at"
        )


class PortOfCallHistorySerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = PortOfCall
        fields = (
            "id", "name", "latitude", "longitude", "notes",
            "created_at", "updated_at"
        )


class VesselNestedSerializer(
        PartialUpdateSerializerMixin, HyperlinkedModelSerializer):

    class Meta:
        model = Vessel
        fields = ("id", "url")


class PortOfCallNestedSerializer(
        PartialUpdateSerializerMixin, HyperlinkedModelSerializer):

    class Meta:
        model = PortOfCall
        fields = ("id", "url")


class DayDetailSerializer(
        PartialUpdateSerializerMixin, HyperlinkedModelSerializer):
    vessel = VesselSerializer(read_only=True)
    port_of_call = PortOfCallSerializer(read_only=True)

    class Meta:
        model = Day
        fields = (
            "id", "url", "vessel", "port_of_call", "date",
            "total_distance_this_day", "high_tide", "low_tide", "skipper",
            "created_at", "updated_at"
        )


class DayListSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):
    vessel = VesselNestedSerializer(read_only=True)
    port_of_call = PortOfCallNestedSerializer(read_only=True)

    class Meta:
        model = Day
        fields = (
            "id", "url", "vessel", "port_of_call", "date",
            "total_distance_this_day", "high_tide", "low_tide", "skipper",
            "created_at", "updated_at"
        )


class DayCreateSerializer(
        PartialUpdateSerializerMixin, HyperlinkedModelSerializer):
    vessel = PrimaryKeyRelatedField(
        queryset=Vessel.objects.all())
    port_of_call = PrimaryKeyRelatedField(
        queryset=PortOfCall.objects.all(), required=False, allow_null=True)
    date = DateField()

    def create(self, validated_data):
        """
        Create and return a new `Day` instance, given the validated data.
        """
        date_entry = validated_data.pop("date", None)
        if date_entry is not None:
            validated_data["date"] = date_entry
        return Day.objects.create(**validated_data)

    class Meta:
        model = Day
        fields = "__all__"


class DateSerializer(
        PartialUpdateSerializerMixin, HyperlinkedModelSerializer):

    class Meta:
        model = Day
        fields = ("url", "date")


class HourSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):

    class Meta:
        model = Hour
        fields = (
            "id", "url", "day", "time", "course", "speed", "latitude",
            "longitude", "weather", "wind_speed", "wind_direction",
            "visibility", "engine_hours", "fuel_level", "water_level",
            "distance_since_last_entry", "timezone",
            "created_at", "updated_at"
        )


class DateHourSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):

    class Meta:
        model = Hour
        fields = (
            "id", "url", "time", "course", "speed", "latitude",
            "longitude", "weather", "wind_speed", "wind_direction",
            "visibility", "engine_hours", "fuel_level", "water_level",
            "distance_since_last_entry", "timezone",
            "created_at", "updated_at"
        )


class NoteSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        HyperlinkedModelSerializer):

    class Meta:
        model = Note
        fields = (
            "id", "url", "timestamp", "vessel", "note", "created_at",
            "updated_at"
        )
