from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.notices.models import Notice, TargetAudience
from apps.notices.serializers import NoticeSerializer
from apps.users.permissions import IsStaff, IsCollegeAdmin

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-is_pinned', '-created_at')
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['target_role', 'target_department', 'priority', 'is_pinned']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'priority', 'is_pinned']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaff()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_college_admin() or user.is_staff_user():
            return queryset
        
        # Filter notices based on target role & user's department
        user_role = user.role
        user_dept_id = None
        if hasattr(user, 'student_profile') and user.student_profile.department:
            user_dept_id = user.student_profile.department.id
        elif hasattr(user, 'faculty_profile') and user.faculty_profile.department:
            user_dept_id = user.faculty_profile.department.id

        role_query = Q(target_role=TargetAudience.ALL) | Q(target_role=user_role)
        dept_query = Q(target_department__isnull=True)
        if user_dept_id:
            dept_query |= Q(target_department_id=user_dept_id)

        return queryset.filter(role_query & dept_query)
