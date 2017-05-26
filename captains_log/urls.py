from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from logbook_app import views
from rest_framework_nested import routers

app_name = "logbook_app"

router = routers.DefaultRouter()

router.register(r"crew", views.CrewViewSet)
router.register(r"vessels", views.VesselViewSet)
router.register(r"trips", views.TripViewSet)
router.register(r"days", views.DayViewSet)
router.register(r"hours", views.HourViewSet)
router.register(r"portsofcall", views.PortOfCallViewSet)
router.register(r"notes", views.NoteViewSet)

vessel_day_router = routers.NestedSimpleRouter(
    router, r"vessels", lookup="vessels")
vessel_day_router.register(r"days", views.DayViewSet, base_name="days")

vessel_day_hour_router = routers.NestedSimpleRouter(
    vessel_day_router, r"days", lookup="day")
vessel_day_hour_router.register(r"hours", views.HourViewSet, base_name="hours")

urlpatterns = [
    url(r"^$", RedirectView.as_view(url='logbook/api/')),
    url(r"^logbook/api/", include(router.urls)),
    url(r"^logbook/api/", include(vessel_day_router.urls)),
    url(r"^logbook/api/", include(vessel_day_hour_router.urls)),
    url(r'^logbook/api/', include(vessel_day_router.urls)),
    url(r"^logbook/api/vessels/(?P<vessel>[0-9]+)/dates/(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})/$",  # noqa
        views.DateHourViewSet.as_view({"get": "retrieve"})),
    url(r"^logbook/api/vessels/(?P<pk>[0-9]+)/history/$",
        views.VesselHistoryViewSet.as_view({"get": "list"})),
    url(r"^logbook/api/portsofcall/(?P<pk>[0-9]+)/history/$",
        views.PortOfCallHistoryViewSet.as_view({"get": "list"})),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
