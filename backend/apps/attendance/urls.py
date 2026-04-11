from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.attendance.views import (
    AttendanceSessionViewSet, AttendanceRecordViewSet,
    BulkAttendanceView, StudentAttendanceSummaryView
)

router = DefaultRouter()
router.register('sessions', AttendanceSessionViewSet, basename='attendance-session')
router.register('records', AttendanceRecordViewSet, basename='attendance-record')

urlpatterns = [
    path('bulk/', BulkAttendanceView.as_view(), name='bulk-attendance'),
    path('summary/', StudentAttendanceSummaryView.as_view(), name='my-attendance-summary'),
    path('summary/<int:student_id>/', StudentAttendanceSummaryView.as_view(), name='student-attendance-summary'),
    path('', include(router.urls)),
]
