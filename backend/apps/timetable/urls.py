from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.timetable.views import TimetableSlotViewSet

router = DefaultRouter()
router.register('slots', TimetableSlotViewSet, basename='timetable-slot')

urlpatterns = [
    path('', include(router.urls)),
]
