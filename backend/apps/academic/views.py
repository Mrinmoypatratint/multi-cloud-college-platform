from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.academic.models import Department, Course, Subject, SubjectFacultyAssignment
from apps.academic.serializers import DepartmentSerializer, CourseSerializer, SubjectSerializer, SubjectFacultyAssignmentSerializer
from apps.users.permissions import IsCollegeAdmin

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('code')
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['code', 'name', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCollegeAdmin()]
        return [permissions.IsAuthenticated()]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'degree_level']
    search_fields = ['code', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCollegeAdmin()]
        return [permissions.IsAuthenticated()]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('semester', 'code')
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'semester']
    search_fields = ['code', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCollegeAdmin()]
        return [permissions.IsAuthenticated()]

class SubjectFacultyAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SubjectFacultyAssignment.objects.all().order_by('-academic_year', 'section')
    serializer_class = SubjectFacultyAssignmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'faculty', 'academic_year', 'section']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCollegeAdmin()]
        return [permissions.IsAuthenticated()]
