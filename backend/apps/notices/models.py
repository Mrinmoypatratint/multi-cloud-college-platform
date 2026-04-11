from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class PriorityLevel(models.TextChoices):
    LOW = 'LOW', 'Low'
    NORMAL = 'NORMAL', 'Normal'
    HIGH = 'HIGH', 'High'
    URGENT = 'URGENT', 'Urgent'

class TargetAudience(models.TextChoices):
    ALL = 'ALL', 'All Users'
    STUDENT = 'STUDENT', 'Students Only'
    FACULTY = 'FACULTY', 'Faculty Only'
    STAFF = 'STAFF', 'Staff Only'

class Notice(TimeStampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='published_notices')
    target_role = models.CharField(max_length=20, choices=TargetAudience.choices, default=TargetAudience.ALL)
    target_department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='notices')
    priority = models.CharField(max_length=15, choices=PriorityLevel.choices, default=PriorityLevel.NORMAL)
    is_pinned = models.BooleanField(default=False)
    attachment_url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"[{self.priority}] {self.title}"
