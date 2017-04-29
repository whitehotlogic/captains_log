from models import Day, Hour, Note, PortOfCall, Vessel
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin


class VesselSerializer(
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vessel
        fields = (
            "id", "url", "name", "hull_number", "fuel_capacity",
            "water_capacity", "battery_capacity", "engine_manufacturer",
            "engine_number", "engine_type", "owner_name",
            "owner_certification_agency", "owner_certification_number",
            "created_at", "updated_at"
        )


class PortOfCallSerializer(
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PortOfCall
        fields = (
            "id", "url", "name", "latitude", "longitude", "notes",
            "created_at", "updated_at"
        )


class VesselNestedSerializer(
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vessel
        fields = ("id", "url")


class PortOfCallNestedSerializer(
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PortOfCall
        fields = ("id", "url")


class DayDetailSerializer(
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):
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
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):
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
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):
    vessel = serializers.PrimaryKeyRelatedField(
        queryset=Vessel.objects.all())
    port_of_call = serializers.PrimaryKeyRelatedField(
        queryset=PortOfCall.objects.all(), required=False, allow_null=True)
    date = serializers.DateField()

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
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Day
        fields = ("url", "date")


class HourSerializer(
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

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
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

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
        PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):
    # vessel = VesselNestedSerializer()

    class Meta:
        model = Note
        fields = (
            "id", "url", "timestamp", "vessel", "note", "created_at",
            "updated_at"
        )
