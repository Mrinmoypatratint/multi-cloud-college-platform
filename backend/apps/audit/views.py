from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.audit.models import AuditLog
from apps.audit.serializers import AuditLogSerializer
from apps.users.permissions import IsSuperAdmin, IsCollegeAdmin

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-created_at')
    serializer_class = AuditLogSerializer
    permission_classes = [IsCollegeAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['method', 'status_code', 'user']
    search_fields = ['action', 'path', 'user__username', 'ip_address']
