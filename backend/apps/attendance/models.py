from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class AttendanceStatus(models.TextChoices):
    PRESENT = 'PRESENT', 'Present'
    ABSENT = 'ABSENT', 'Absent'
    LATE = 'LATE', 'Late'
    EXCUSED = 'EXCUSED', 'Excused'

class AttendanceSession(TimeStampedModel):
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE, related_name='attendance_sessions')
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conducted_sessions')
    date = models.DateField()
    slot_time = models.CharField(max_length=50, default='09:00 AM - 10:00 AM')
    section = models.CharField(max_length=10, default='A')
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.subject.code} Session on {self.date} ({self.section})"

class AttendanceRecord(TimeStampedModel):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=15, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.session.subject.code} ({self.status})"
