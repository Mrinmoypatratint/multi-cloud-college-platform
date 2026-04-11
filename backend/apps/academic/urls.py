from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.academic.views import DepartmentViewSet, CourseViewSet, SubjectViewSet, SubjectFacultyAssignmentViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='department')
router.register('courses', CourseViewSet, basename='course')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('assignments', SubjectFacultyAssignmentViewSet, basename='subject-assignment')

urlpatterns = [
    path('', include(router.urls)),
]
