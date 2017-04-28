from django.conf.urls import url, include
from rest_framework import routers
from logger_app import views

router = routers.DefaultRouter()
router.register(r'vessel', views.VesselViewSet)
router.register(r'day', views.DayViewSet)
router.register(r'hour', views.HourViewSet)
router.register(r'note', views.NoteViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'),
    ),
]
