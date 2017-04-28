from models import Vessel, Day, Hour, Note
from rest_framework import serializers


class VesselSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vessel
        fields = "__all__"


class DaySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Day
        fields = "__all__"


class DateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Day
        fields = ('url', 'date')


class HourSerializer(serializers.HyperlinkedModelSerializer):
    day = DateSerializer()

    class Meta:
        model = Hour
        fields = "__all__"


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    # vessel = VesselSerializer()

    class Meta:
        model = Note
        fields = "__all__"
