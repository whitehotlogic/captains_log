from drf_queryfields import QueryFieldsMixin
from models import (Crew, Day, Hour, Note, PortOfCall, Provision, Supply,
                    SupplyProvision, Trip, Vessel)
from rest_framework.serializers import (DateField, ModelSerializer,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField)
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin


class CrewSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Crew
        fields = (
            "id", "name", "can_skipper", "is_active",
            "created_at", "updated_at"
        )


class VesselSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Vessel
        fields = (
            "id", "name", "manufacturer", "length", "draft", "model",
            "hull_number", "engine_manufacturer", "engine_number",
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
            "hull_number", "engine_manufacturer", "engine_number",
            "engine_type", "owner", "skipper", "owner_certification_agency",
            "owner_certification_number", "created_at", "updated_at"
        )


class ProvisionSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Provision
        fields = (
            "id", "name", "measurement_name", "created_at", "updated_at"
        )


class SupplySerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Supply
        fields = (
            "vessel", "fuel", "water",
            "battery", "provisions", "created_at", "updated_at"
        )


class SupplyProvisionSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = SupplyProvision
        fields = (
            "id", "supply", "provision", "quantity", "created_at"
        )


class PortOfCallSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = PortOfCall
        fields = (
            "id", "name", "latitude", "longitude", "notes",
            "created_at", "updated_at"
        )


class TripSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Trip
        fields = (
            "id", "name", "vessels", "start_date", "end_date",
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
        PartialUpdateSerializerMixin, ModelSerializer):

    class Meta:
        model = Vessel
        fields = ("id", "url")


class PortOfCallNestedSerializer(
        PartialUpdateSerializerMixin, ModelSerializer):

    class Meta:
        model = PortOfCall
        fields = ("id", "url")


class DayDetailSerializer(
        PartialUpdateSerializerMixin, ModelSerializer):
    vessel = VesselSerializer(read_only=True)
    port_of_call = PortOfCallSerializer(read_only=True)

    class Meta:
        model = Day
        fields = (
            "id", "vessel", "port_of_call", "date",
            "total_distance_this_day", "high_tide", "low_tide",
            "created_at", "updated_at"
        )


class DayListSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):
    vessel = VesselNestedSerializer(read_only=True)
    port_of_call = PortOfCallNestedSerializer(read_only=True)

    class Meta:
        model = Day
        fields = (
            "id", "vessel", "port_of_call", "date",
            "total_distance_this_day", "high_tide", "low_tide",
            "created_at", "updated_at"
        )


class DayCreateSerializer(
        PartialUpdateSerializerMixin, ModelSerializer):
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
        PartialUpdateSerializerMixin, ModelSerializer):

    class Meta:
        model = Day
        fields = ("date")


class HourSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Hour
        fields = (
            "id", "day", "time", "course", "speed", "latitude",
            "longitude", "weather", "wind_speed", "wind_direction",
            "visibility", "engine_hours", "distance_since_last_entry",
            "timezone", "created_at", "updated_at"
        )


class DateHourSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Hour
        fields = (
            "id", "time", "course", "speed", "latitude",
            "longitude", "weather", "wind_speed", "wind_direction",
            "visibility", "engine_hours", "distance_since_last_entry",
            "timezone", "created_at", "updated_at"
        )


class NoteSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Note
        fields = (
            "id", "timestamp", "vessel", "note", "created_at",
            "updated_at"
        )
