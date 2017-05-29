from django.contrib.auth.models import User
from models import (Crew, Note, PortOfCall, Supply, SupplyProvision, Trip,
                    Vessel)
from rest_framework.exceptions import PermissionDenied


class CreateUpdateMiddleware(object):

    def __init__(self, request):
        self.request = request

    def acting_user(self):
        if hasattr(self.request.user, "_wrapped"):
            return self.request.user._wrapped
        else:
            return self.request.user


class UserCreateUpdateMiddleware(object):

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.get("username"),
            validated_data.get("email"),
            validated_data.get("password"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name")
        )

    def update(self, instance, validated_data):
        validated_data["current_password"] = validated_data.get(
            "current_password")
        if instance.check_password(validated_data["current_password"]):
            if validated_data.get("new_password"):
                instance.set_password(validated_data["new_password"])
            instance.username = validated_data.get(
                "username", instance.username)
            instance.first_name = validated_data.get(
                "first_name", instance.first_name)
            instance.last_name = validated_data.get(
                "last_name", instance.last_name)
            instance.email = validated_data.get("email", instance.email)
            instance.updated_by = self.acting_user()
            instance.save()
            return instance
        else:
            raise PermissionDenied("Incorrect credentials for User")


class CrewCreateUpdateMiddleware(CreateUpdateMiddleware):

    def create(self, validated_data):
        crew_user = validated_data.get("crew_user", None)
        crew_user_password = validated_data.get("crew_user_password", None)
        validated_data["created_by"] = self.acting_user()
        validated_data["updated_by"] = self.acting_user()
        if "crew_user_password" in validated_data:
            del validated_data["crew_user_password"]
        if crew_user is not None:
            if isinstance(crew_user, User):
                if crew_user.check_password(crew_user_password):
                    return Crew.objects.create(**validated_data)
                else:
                    raise PermissionDenied(
                        "Incorrect password for User {0}".format(
                            crew_user.username)
                    )
            else:
                try:
                    crew_user_id = int(crew_user)
                    try:
                        user = User.objects.get(pk=crew_user_id)
                    except User.DoesNotExist:
                        raise PermissionDenied("Incorrect password for User")
                    if user.check_password(crew_user_password):
                        return Crew.objects.create(**validated_data)
                    raise PermissionDenied("Incorrect password for User")
                except ValueError:
                    pass
        return Crew.objects.create(**validated_data)

    def update(self, instance, validated_data):
        crew_user = validated_data.get("crew_user", None)
        crew_user_password = validated_data.get("crew_user_password", None)
        if "crew_user_password" in validated_data:
            del validated_data["crew_user_password"]
        if crew_user is not None:
            if isinstance(crew_user, User):
                if crew_user.check_password(crew_user_password):
                    instance.crew_user = crew_user
                else:
                    raise PermissionDenied(
                        "Incorrect password for User {0}".format(
                            crew_user.username)
                    )
            else:
                try:
                    crew_user_id = int(crew_user)
                    try:
                        user = User.objects.get(pk=crew_user_id)
                    except User.DoesNotExist:
                        raise PermissionDenied("Incorrect password for User")
                    if user.check_password(crew_user_password):
                        instance.crew_user = user
                    raise PermissionDenied("Incorrect password for User")
                except ValueError:
                    pass
        else:
            instance.crew_user = None
        instance.crew_name = validated_data.get(
            "crew_name", instance.crew_name)
        instance.can_skipper = validated_data.get(
            "can_skipper", instance.can_skipper)
        instance.is_active = validated_data.get(
            "is_active", instance.is_active)
        instance.updated_by = self.acting_user()
        instance.save()
        return instance


class VesselCreateUpdateMiddleware(CreateUpdateMiddleware):

    def create(self, validated_data):
        validated_data["created_by"] = self.acting_user()
        validated_data["updated_by"] = self.acting_user()
        return Vessel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.vessel_name = validated_data.get(
            "vessel_name", instance.vessel_name)
        instance.model = validated_data.get("model", instance.model)
        instance.manufacturer = validated_data.get(
            "manufacturer", instance.manufacturer)
        instance.length = validated_data.get("length", instance.length)
        instance.draft = validated_data.get("draft", instance.draft)
        instance.hull_number = validated_data.get(
            "hull_number", instance.hull_number)
        instance.engine_manufacturer = validated_data.get(
            "engine_manufacturer", instance.engine_manufacturer)
        instance.engine_number = validated_data.get(
            "engine_number", instance.engine_number)
        instance.engine_type = validated_data.get(
            "engine_type", instance.engine_type)
        instance.owner = validated_data.get("owner", instance.owner)
        instance.skipper = validated_data.get("skipper", instance.skipper)
        instance.certification_agency = validated_data.get(
            "certification_agency", instance.certification_agency)
        instance.certification_number = validated_data.get(
            "certification_number", instance.certification_number)
        instance.image = validated_data.get("image", instance.image)
        instance.updated_by = self.acting_user()
        instance.save()
        return instance


class SupplyCreateUpdateMiddleware(CreateUpdateMiddleware):

    def create(self, validated_data):
        validated_data["created_by"] = self.acting_user()
        validated_data["updated_by"] = self.acting_user()
        return Supply.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.vessel = validated_data.get("vessel", instance.vessel)
        instance.fuel = validated_data.get("fuel", instance.fuel)
        instance.water = validated_data.get("water", instance.water)
        instance.battery = validated_data.get("battery", instance.battery)
        instance.updated_by = self.acting_user()
        instance.save()
        return instance


class SupplyProvisionCreateUpdateMiddleware(CreateUpdateMiddleware):

    def create(self, validated_data):
        validated_data["created_by"] = self.acting_user()
        validated_data["updated_by"] = self.acting_user()
        return SupplyProvision.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.supply = validated_data.get("supply", instance.supply)
        instance.provision = validated_data.get(
            "provision", instance.provision)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.updated_by = self.acting_user()
        instance.save()
        return instance


class PortOfCallCreateUpdateMiddleware(CreateUpdateMiddleware):

    def create(self, validated_data):
        validated_data["created_by"] = self.acting_user()
        validated_data["updated_by"] = self.acting_user()
        return PortOfCall.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.port_of_call_name = validated_data.get(
            "port_of_call_name", instance.port_of_call_name)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get(
            "longitude", instance.longitude)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.updated_by = self.acting_user()
        instance.save()
        return instance


class TripCreateUpdateMiddleware(CreateUpdateMiddleware):

    def create(self, validated_data):
        validated_data["created_by"] = self.acting_user()
        validated_data["updated_by"] = self.acting_user()
        return Trip.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.trip_name = validated_data.get(
            "trip_name", instance.trip_name)
        instance.vessels = validated_data.get("vessels", instance.vessels)
        instance.start_date = validated_data.get(
            "start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.starting_port = validated_data.get(
            "starting_port", instance.starting_port)
        instance.crew = validated_data.get("crew", instance.crew)
        instance.stops = validated_data.get("stops", instance.stops)
        instance.destination_port = validated_data.get(
            "destination_port", instance.destination_port)
        instance.updated_by = self.acting_user()
        instance.save()
        return instance


class NoteCreateMiddleware(CreateUpdateMiddleware):

    def create(self, validated_data):
        validated_data["created_by"] = self.acting_user()
        validated_data["updated_by"] = self.acting_user()
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.vessel = validated_data.get("vessel", instance.vessel)
        instance.note = validated_data.get("note", instance.note)
        instance.updated_by = self.acting_user()
        instance.save()
        return instance
