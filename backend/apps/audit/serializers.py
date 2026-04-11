from rest_framework import serializers
from apps.audit.models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'username', 'user_role', 'ip_address', 'method', 'path', 'action', 'status_code', 'details', 'created_at']

    def get_username(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return "System / Anonymous"

    def get_user_role(self, obj):
        if obj.user:
            return obj.user.get_role_display()
        return "N/A"
