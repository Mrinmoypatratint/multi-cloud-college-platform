from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class DegreeLevel(models.TextChoices):
    BACHELOR = 'BACHELOR', 'Bachelor Degree'
    MASTER = 'MASTER', 'Master Degree'
    DIPLOMA = 'DIPLOMA', 'Diploma'
    DOCTORATE = 'DOCTORATE', 'Doctorate / PhD'

class Department(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    head_of_department = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

class Course(TimeStampedModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    duration_years = models.IntegerField(default=4)
    degree_level = models.CharField(max_length=20, choices=DegreeLevel.choices, default=DegreeLevel.BACHELOR)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Subject(TimeStampedModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    semester = models.IntegerField(default=1)
    credits = models.IntegerField(default=3)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code}) - Sem {self.semester}"

class SubjectFacultyAssignment(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='faculty_assignments')
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_subjects')
    academic_year = models.CharField(max_length=20, default='2025-2026')
    section = models.CharField(max_length=10, default='A')

    class Meta:
        unique_together = ('subject', 'faculty', 'academic_year', 'section')

    def __str__(self):
        return f"{self.subject.code} - {self.faculty.get_full_name()} ({self.section})"
