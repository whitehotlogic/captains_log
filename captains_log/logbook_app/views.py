# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from captains_log.logbook_app import serializers
from captains_log.logbook_app.filters import (CrewFilter, DayFilter,
                                              HourFilter, PortOfCallFilter,
                                              ProvisionFilter, SupplyFilter,
                                              TripFilter, VesselFilter)
from captains_log.logbook_app.models import (Crew, Day, Hour, Note, PortOfCall,
                                             Provision, Supply,
                                             SupplyProvision, Trip, Vessel)
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework import mixins, viewsets


class UserViewSet(ModelViewSet):
    """
    API Endpoint for registering users
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        if self.action == "update":
            return serializers.UserUpdateSerializer
        if self.action == "partial_update":
            return serializers.UserUpdateSerializer
        return serializers.UserSerializer


class UserAutocompleteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API Endpoint for receiving a completed username from a partial match
    """
    queryset = User.objects.all()

    def list(self, request):
        if self.request.GET.get("username"):
            queryset = self.queryset.filter(
                vessel_name__icontains=self.request.GET[
                    "username"])[:10]
            serializer = serializers.UserAutocompleteSerializer(
                queryset, context={"request": request}, many=True)
            return Response(serializer.data)
        return Response([])


class CrewViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows crew to be viewed or edited
    """
    queryset = Crew.objects.all()
    filter_class = CrewFilter

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CrewCreateUpdateSerializer
        if self.action == "update":
            return serializers.CrewCreateUpdateSerializer
        if self.action == "partial_update":
            return serializers.CrewCreateUpdateSerializer
        return serializers.CrewSerializer


class CrewAutocompleteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API Endpoint for receiving a completed crew_name from a partial match
    """
    queryset = Crew.objects.all()

    def list(self, request):
        if self.request.GET.get("crew_name"):
            queryset = self.queryset.filter(
                crew_name__icontains=self.request.GET[
                    "crew_name"])[:10]
            serializer = serializers.CrewAutocompleteSerializer(
                queryset, context={"request": request}, many=True)
            return Response(serializer.data)
        return Response([])


class VesselViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows vessels to be viewed or edited.
    All measurements are in feet/gallons.
    """
    queryset = Vessel.objects.all()
    serializer_class = serializers.VesselSerializer
    filter_class = VesselFilter


class VesselAutocompleteViewSet(
        mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API Endpoint for receiving a completed vessel_name from a partial match
    """
    queryset = Vessel.objects.all()

    def list(self, request):
        if self.request.GET.get("vessel_name"):
            queryset = self.queryset.filter(
                vessel_name__icontains=self.request.GET[
                    "vessel_name"])[:10]
            serializer = serializers.VesselAutocompleteSerializer(
                queryset, context={"request": request}, many=True)
            return Response(serializer.data)
        return Response([])


class ProvisionViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows provisions to be viewed or edited.
    All measurements are in feet/gallons.
    """
    queryset = Provision.objects.all()
    serializer_class = serializers.ProvisionSerializer
    filter_class = ProvisionFilter


class ProvisionAutocompleteViewSet(
        mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API Endpoint for receiving a completed provision_name from a partial match
    """
    queryset = Provision.objects.all()

    def list(self, request):
        if self.request.GET.get("provision_name"):
            queryset = self.queryset.filter(
                provision_name__icontains=self.request.GET[
                    "provision_name"])[:10]
            serializer = serializers.ProvisionAutocompleteSerializer(
                queryset, context={"request": request}, many=True)
            return Response(serializer.data)
        return Response([])


class SupplyViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows vessels to be viewed or edited.
    All measurements are in feet/gallons.
    """
    queryset = Supply.objects.all()
    serializer_class = serializers.SupplySerializer
    filter_class = SupplyFilter


class SupplyProvisionViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows supply provisions to be viewed or edited.
    All measurements are in feet/gallons.
    """
    queryset = SupplyProvision.objects.all()
    serializer_class = serializers.SupplyProvisionSerializer


class PortOfCallViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows vessels to be viewed or edited.
    """
    queryset = PortOfCall.objects.all()
    serializer_class = serializers.PortOfCallSerializer
    filter_class = PortOfCallFilter


class TripViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows trips to be viewed or edited
    """
    queryset = Trip.objects.all()
    serializer_class = serializers.TripSerializer
    filter_class = TripFilter


class DayViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows days to be viewed or edited.
    """
    queryset = Day.objects.all()
    filter_class = DayFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.DayDetailSerializer
        if self.action == "create":
            return serializers.DayCreateSerializer
        if self.action == "update":
            return serializers.DayCreateSerializer
        if self.action == "partial_update":
            return serializers.DayCreateSerializer
        return serializers.DayListSerializer


class VesselHistoryViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that shows history of vessel changes.
    All measurements are in feet/gallons.
    """
    queryset = Vessel.history.all()
    serializer_class = serializers.VesselHistorySerializer

    def get_queryset(self):
        history = Vessel.history.filter(id=self.kwargs["pk"])
        return history


class SupplyHistoryViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that shows history of vessel changes.
    All measurements are in feet/gallons.
    """
    queryset = Supply.history.all()
    serializer_class = serializers.SupplyHistorySerializer

    def get_queryset(self):
        history = Supply.history.filter(id=self.kwargs["pk"])
        return history


class PortOfCallHistoryViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that shows history of vessel changes.
    All measurements are in feet/gallons.
    """
    queryset = PortOfCall.history.all()
    serializer_class = serializers.PortOfCallSerializer

    def get_queryset(self):
        history = PortOfCall.history.filter(id=self.kwargs["pk"])
        return history


class PortOfCallAutocompleteViewSet(
        mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API Endpoint for receiving a completed port_of_call from a partial match
    """
    queryset = PortOfCall.objects.all()

    def list(self, request):
        if self.request.GET.get("port_of_call_name"):
            queryset = self.queryset.filter(
                port_of_call_name__icontains=self.request.GET[
                    "port_of_call_name"])[:10]
            serializer = serializers.PortOfCallAutocompleteSerializer(
                queryset, context={"request": request}, many=True)
            return Response(serializer.data)
        return Response([])


class DateViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that allows days to be viewed or edited.
    """
    queryset = Day.objects.all()
    serializer_class = serializers.DayListSerializer
    lookup_field = "vessel"
    filter_class = DayFilter

    def get_queryset(self):
        vessel = Vessel.objects.get(pk=self.kwargs["vessel"])
        queryset = Day.objects.filter(date=self.kwargs["date"], vessel=vessel)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.DayDetailSerializer
        if self.action == "create":
            return serializers.DayCreateSerializer
        return serializers.DayListSerializer


class DateHourViewSet(NestedViewSetMixin, ModelViewSet):
    """
    API endpoint that shows a detail view of a day, associated with a vessel,
    and a list view of the hours associated with that day.
    """
    queryset = Day.objects.all()
    serializer_class = serializers.DateHourSerializer
    pagination_class = None

    def retrieve(self, request, *args, **kwargs):
        vessel = Vessel.objects.get(pk=self.kwargs["vessel"])
        try:
            day_queryset = Day.objects.get(
                date=self.kwargs["date"], vessel=vessel)
        except Day.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        hour_queryset = Hour.objects.filter(day=day_queryset)
        self.kwargs["pk"] = day_queryset.id
        hour_queryset.day = day_queryset
        day_serializer = serializers.DayDetailSerializer(
            day_queryset, context={"request": self.request}
        )
        hour_serializer = serializers.DateHourSerializer(
            hour_queryset, context={"request": self.request}, many=True)
        day_detail = OrderedDict(day_serializer.data)
        hours = OrderedDict((
            ("count", len(hour_serializer.data)),
            ("next", None),
            ("previous", None),
            ("results", hour_serializer.data)
        ))
        day_detail["hours"] = hours
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
