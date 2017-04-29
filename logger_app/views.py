# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from logger_app import serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from .filters import DayFilter, HourFilter, PortOfCallFilter, VesselFilter
from .models import Day, Hour, Note, PortOfCall, Vessel
from rest_framework_extensions.mixins import NestedViewSetMixin
from .pagination import DateResultsSetPagination
import itertools

class VesselViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows vessels to be viewed or edited.
    """
    queryset = Vessel.objects.all()
    serializer_class = serializers.VesselSerializer
    filter_class = VesselFilter


class PortOfCallViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows vessels to be viewed or edited.
    """
    queryset = PortOfCall.objects.all()
    serializer_class = serializers.PortOfCallSerializer
    filter_class = PortOfCallFilter


class DayViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows days to be viewed or edited.
    """
    queryset = Day.objects.all()
    serializer_class = serializers.DayListSerializer
    filter_class = DayFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DayListSerializer
        if self.action == 'retrieve':
            return serializers.DayDetailSerializer
        if self.action == 'create':
            return serializers.DayCreateSerializer
        return serializers.DayListSerializer


class DateViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows days to be viewed or edited.
    """
    queryset = Day.objects.all()
    serializer_class = serializers.DayListSerializer
    lookup_field = 'vessel'
    filter_class = DayFilter

    def get_queryset(self):
        print vars(self)
        vessel = Vessel.objects.get(pk=self.kwargs['vessel'])
        queryset = Day.objects.filter(date=self.kwargs['date'], vessel=vessel)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DayListSerializer
        if self.action == 'retrieve':
            return serializers.DayDetailSerializer
        if self.action == 'create':
            return serializers.DayCreateSerializer
        return serializers.DayListSerializer


class DateHourViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows days to be viewed or edited.
    """
    day_queryset = Day.objects.all()
    serializer_class = serializers.DateHourSerializer
    lookup_field = 'vessel'
    # filter_class = DayFilter

    def get_queryset(self):
        print vars(self)
        vessel = Vessel.objects.get(pk=self.kwargs['vessel'])
        day_queryset = Day.objects.get(
            date=self.kwargs['date'], vessel=vessel)
        hour_queryset = Hour.objects.filter(day=day_queryset)
        self.kwargs['pk'] = day_queryset.id
        # hour_queryset.pk = day_queryset.id
        hour_queryset.day = day_queryset
        # print vars(hour_queryset)
        hour_serializer = serializers.HourSerializer(
            hour_queryset, context={'request': self.request}, many=True)
        print hour_serializer
        return hour_serializer


class HourViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows hours to be viewed or edited.
    """
    queryset = Hour.objects.all()
    serializer_class = serializers.HourSerializer
    filter_class = HourFilter


class NoteViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.
    """
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
