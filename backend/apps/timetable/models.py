from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class DayOfWeek(models.TextChoices):
    MONDAY = 'MONDAY', 'Monday'
    TUESDAY = 'TUESDAY', 'Tuesday'
    WEDNESDAY = 'WEDNESDAY', 'Wednesday'
    THURSDAY = 'THURSDAY', 'Thursday'
    FRIDAY = 'FRIDAY', 'Friday'
    SATURDAY = 'SATURDAY', 'Saturday'
    SUNDAY = 'SUNDAY', 'Sunday'

class TimetableSlot(TimeStampedModel):
    day_of_week = models.CharField(max_length=15, choices=DayOfWeek.choices, default=DayOfWeek.MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE, related_name='timetable_slots')
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timetable_slots')
    room_number = models.CharField(max_length=50, default='Room 101')
    section = models.CharField(max_length=10, default='A')

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.day_of_week} {self.start_time}-{self.end_time}: {self.subject.code} ({self.room_number})"
