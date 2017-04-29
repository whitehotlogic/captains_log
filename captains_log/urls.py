from django.conf.urls import url, include
# from rest_framework import routers
from rest_framework_nested import routers
from logger_app import views

router = routers.DefaultRouter()

router.register(r'vessels', views.VesselViewSet)
router.register(r'days', views.DayViewSet)
router.register(r'hours', views.HourViewSet)
router.register(r'portsofcall', views.PortOfCallViewSet)
router.register(r'notes', views.NoteViewSet)

vessel_day_router = routers.NestedSimpleRouter(
    router, r'vessels', lookup='vessel')
vessel_day_router.register(r'days', views.DayViewSet, base_name='days')

vessel_day_hour_router = routers.NestedSimpleRouter(
    vessel_day_router, r'days', lookup='day')
vessel_day_hour_router.register(r'hours', views.HourViewSet, base_name='hours')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(vessel_day_router.urls)),
    url(r'^api/', include(vessel_day_hour_router.urls)),
    url(r'^api/vessels/(?P<vessel>[0-9]+)/dates/(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})/$',
        views.DateHourViewSet.as_view({'get': 'retrieve'})),
]
