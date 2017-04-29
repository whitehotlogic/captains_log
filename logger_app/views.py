# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb
from collections import OrderedDict

from logger_app import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from .filters import DayFilter, HourFilter, PortOfCallFilter, VesselFilter
from .models import Day, Hour, Note, PortOfCall, Vessel


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
    filter_class = DayFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DayListSerializer
        if self.action == 'retrieve':
            return serializers.DayDetailSerializer
        if self.action == 'create':
            return serializers.DayCreateSerializer
        if self.action == 'update':
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
    API endpoint that shows a detail view of a day, associated with a vessel,
    and a list view of the hours associated with that day.
    """
    queryset = Day.objects.all()
    serializer_class = serializers.DateHourSerializer

    def retrieve(self, request, *args, **kwargs):
        # pdb.set_trace()
        vessel = Vessel.objects.get(pk=self.kwargs['vessel'])
        try:
            day_queryset = Day.objects.get(
                date=self.kwargs['date'], vessel=vessel)
        except Day.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        hour_queryset = Hour.objects.filter(day=day_queryset)
        self.kwargs['pk'] = day_queryset.id
        hour_queryset.day = day_queryset
        day_serializer = serializers.DayDetailSerializer(
            day_queryset, context={'request': self.request}
        )
        hour_serializer = serializers.DateHourSerializer(
            hour_queryset, context={'request': self.request}, many=True)
        day_detail = day_serializer.data
        hours = OrderedDict((
            ('count', len(hour_serializer.data)),
            ('next', None),
            ('previous', None),
            ('results', hour_serializer.data)
        ))
        day_detail['hours'] = hours
        return Response(day_detail)


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
