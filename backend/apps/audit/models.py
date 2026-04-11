from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class AuditLog(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    action = models.CharField(max_length=255)
    status_code = models.IntegerField(default=200)
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"[{self.created_at}] {username} {self.method} {self.path} ({self.status_code})"
