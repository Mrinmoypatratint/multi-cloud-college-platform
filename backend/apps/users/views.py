from rest_framework import viewsets, status, generics, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db import models

from apps.users.models import StudentProfile, FacultyProfile, StaffProfile, Role
from apps.users.serializers import (
    UserSerializer, UserCreateSerializer, CustomTokenObtainPairSerializer,
    StudentProfileSerializer, FacultyProfileSerializer, StaffProfileSerializer
)
from apps.users.permissions import IsCollegeAdmin, IsSuperAdmin, IsFaculty, IsOwnerOrAdmin
from apps.core.utils import api_response

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return api_response(data=serializer.data, message="User profile retrieved successfully")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'student_profile__enrollment_number', 'faculty_profile__employee_id']
    ordering_fields = ['date_joined', 'username', 'first_name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsCollegeAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        role_param = self.request.query_params.get('role')
        dept_param = self.request.query_params.get('department')
        
        if role_param:
            queryset = queryset.filter(role=role_param)
        if dept_param:
            queryset = queryset.filter(
                models.Q(student_profile__department_id=dept_param) |
                models.Q(faculty_profile__department_id=dept_param) |
                models.Q(staff_profile__department_id=dept_param)
            )
        return queryset

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all().order_by('-created_at')
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'batch_year', 'semester']
    search_fields = ['enrollment_number', 'user__first_name', 'user__last_name', 'user__email']

class FacultyProfileViewSet(viewsets.ModelViewSet):
    queryset = FacultyProfile.objects.all().order_by('-created_at')
    serializer_class = FacultyProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'designation']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'specialization']
