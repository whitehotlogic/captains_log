from datetime import datetime

from django.contrib.auth.models import User
from models import Crew
from rest_framework.exceptions import PermissionDenied


class CrewCreateUpdateSerializerMiddleware(object):

    def create(self, validated_data):
        crew_user = validated_data.get("crew_user", None)
        crew_user_password = validated_data.get("crew_user_password", None)
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
        instance.updated_at = datetime.now()
        instance.save()
        return instance
