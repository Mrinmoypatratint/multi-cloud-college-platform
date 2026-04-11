from rest_framework import serializers
from apps.notices.models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    department_code = serializers.CharField(source='target_department.code', read_only=True)

    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'author', 'author_name', 'target_role', 'target_department', 'department_code', 'priority', 'is_pinned', 'attachment_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
