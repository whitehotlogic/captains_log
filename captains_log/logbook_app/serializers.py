from django.contrib.auth.models import User
from drf_queryfields import QueryFieldsMixin
from captains_log.logbook_app import middleware
from models import (Crew, Day, Hour, Note, PortOfCall, Provision, Supply,
                    SupplyProvision, Trip, Vessel)
from rest_framework.serializers import (CharField, DateField, ModelSerializer,
                                        PrimaryKeyRelatedField)
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin


class UserCreateSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    def create(self, validated_data):
        user = middleware.UserCreateUpdateMiddleware().create(validated_data)
        user.password = None
        return user

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name", "password"
        )


class UserUpdateSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    current_password = CharField(default=None, max_length=128)
    new_password = CharField(default=None, max_length=128)

    def update(self, instance, validated_data):
        return middleware.UserCreateUpdateMiddleware().update(
            instance, validated_data)

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "current_password", "new_password"
        )


class UserSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id", "username"
        )


class CrewCreateUpdateSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    crew_user_password = CharField(default=None, max_length=128)

    def create(self, validated_data):
        return middleware.CrewCreateUpdateMiddleware(
            self.context["request"]).create(validated_data)

    def update(self, instance, validated_data):
        return middleware.CrewCreateUpdateMiddleware(
            self.context["request"]).update(instance, validated_data)

    class Meta:
        model = Crew
        fields = (
            "id", "crew_name", "crew_user", "crew_user_password",
            "can_skipper", "is_active", "created_at", "updated_at"
        )


class CrewSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Crew
        fields = (
            "id", "crew_name", "crew_user",
            "can_skipper", "is_active", "created_at", "updated_at"
        )


class VesselSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    def create(self, validated_data):
        return middleware.VesselCreateUpdateMiddleware(
            self.context["request"]).create(validated_data)

    def update(self, instance, validated_data):
        return middleware.VesselCreateUpdateMiddleware(
            self.context["request"]).update(instance, validated_data)

    class Meta:
        model = Vessel
        fields = (
            "id", "vessel_name", "manufacturer", "model", "length", "draft",
            "hull_number", "engine_manufacturer", "engine_number",
            "engine_type", "owner", "skipper", "certification_agency",
            "certification_number", "image", "created_at", "updated_at"
        )


class VesselHistorySerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Vessel
        fields = (
            "history_id", "vessel_name", "manufacturer",  "model", "length",
            "draft", "hull_number", "engine_manufacturer", "engine_number",
            "engine_type", "owner", "skipper", "certification_agency",
            "certification_number", "created_at", "updated_at"
        )


class ProvisionSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Provision
        fields = (
            "id", "provision_name", "measurement_name",
            "created_at", "updated_at"
        )


class SupplySerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    def create(self, validated_data):
        return middleware.SupplyCreateUpdateMiddleware(
            self.context["request"]).create(validated_data)

    def update(self, instance, validated_data):
        return middleware.SupplyCreateUpdateMiddleware(
            self.context["request"]).update(instance, validated_data)

    class Meta:
        model = Supply
        fields = (
            "id", "vessel", "fuel", "water",
            "battery", "provisions", "created_at", "updated_at"
        )


class SupplyHistorySerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = Supply
        fields = (
            "vessel", "fuel", "water",
            "battery", "created_at", "updated_at"
        )


class SupplyProvisionSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    def create(self, validated_data):
        return middleware.SupplyProvisionCreateUpdateMiddleware(
            self.context["request"]).create(validated_data)

    def update(self, instance, validated_data):
        return middleware.SupplyProvisionCreateUpdateMiddleware(
            self.context["request"]).update(instance, validated_data)

    class Meta:
        model = SupplyProvision
        fields = (
            "id", "supply", "provision", "quantity", "created_at", "updated_at"
        )


class PortOfCallSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    def create(self, validated_data):
        return middleware.PortOfCallCreateUpdateMiddleware(
            self.context["request"]).create(validated_data)

    def update(self, instance, validated_data):
        return middleware.PortOfCallCreateUpdateMiddleware(
            self.context["request"]).update(instance, validated_data)

    class Meta:
        model = PortOfCall
        fields = (
            "id", "port_of_call_name", "latitude", "longitude", "notes",
            "created_at", "updated_at"
        )


class PortOfCallHistorySerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    class Meta:
        model = PortOfCall
        fields = (
            "history_id", "port_of_call_name", "latitude", "longitude",
            "notes", "created_at", "updated_at"
        )


class TripSerializer(
        QueryFieldsMixin, PartialUpdateSerializerMixin,
        ModelSerializer):

    def create(self, validated_data):
        return middleware.TripCreateUpdateMiddleware(
            self.context["request"]).create(validated_data)

    def update(self, instance, validated_data):
        return middleware.TripCreateUpdateMiddleware(
            self.context["request"]).update(instance, validated_data)

    class Meta:
        model = Trip
        fields = (
            "id", "trip_name", "vessels", "start_date", "end_date",
            "starting_port", "stops", "destination_port",
            "created_at", "updated_at"
        )


class VesselNestedSerializer(
        PartialUpdateSerializerMixin, ModelSerializer):

    class Meta:
        model = Vessel
        fields = ("id",)


class PortOfCallNestedSerializer(
        PartialUpdateSerializerMixin, ModelSerializer):

    class Meta:
        model = PortOfCall
        fields = ("id",)


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

    def create(self, validated_data):
        return middleware.NoteCreateUpdateMiddleware(
            self.context["request"]).create(validated_data)

    class Meta:
        model = Note
        fields = (
            "id", "vessel", "note", "created_at", "updated_at"
        )
