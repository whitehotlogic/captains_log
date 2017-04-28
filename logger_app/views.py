# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from logger_app.serializers import (DaySerializer, HourSerializer,
                                    NoteSerializer, VesselSerializer)
from rest_framework.viewsets import ModelViewSet

from .filters import DayFilter, VesselFilter, HourFilter
from .models import Day, Hour, Note, Vessel


class VesselViewSet(ModelViewSet):
    """
    API endpoint that allows vessels to be viewed or edited.
    """
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
    filter_class = VesselFilter


class DayViewSet(ModelViewSet):
    """
    API endpoint that allows days to be viewed or edited.
    """
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    filter_class = DayFilter


class HourViewSet(ModelViewSet):
    """
    API endpoint that allows hours to be viewed or edited.
    """
    queryset = Hour.objects.all()
    serializer_class = HourSerializer
    filter_class = HourFilter


class NoteViewSet(ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
