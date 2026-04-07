from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel

class Role(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    COLLEGE_ADMIN = 'COLLEGE_ADMIN', 'College Admin'
    FACULTY = 'FACULTY', 'Faculty'
    STAFF = 'STAFF', 'Staff'
    STUDENT = 'STUDENT', 'Student'

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)

    def is_super_admin(self):
        return self.role == Role.SUPER_ADMIN or self.is_superuser

    def is_college_admin(self):
        return self.role in [Role.SUPER_ADMIN, Role.COLLEGE_ADMIN]

    def is_faculty_user(self):
        return self.role in [Role.SUPER_ADMIN, Role.COLLEGE_ADMIN, Role.FACULTY]

    def is_staff_user(self):
        return self.role in [Role.SUPER_ADMIN, Role.COLLEGE_ADMIN, Role.STAFF]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_number = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    batch_year = models.IntegerField(default=2026)
    semester = models.IntegerField(default=1)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Student: {self.user.username} ({self.enrollment_number})"

class FacultyProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='faculties')
    designation = models.CharField(max_length=100, default='Assistant Professor')
    specialization = models.CharField(max_length=200, blank=True, null=True)
    joining_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Faculty: {self.user.username} ({self.employee_id})"

class StaffProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    designation = models.CharField(max_length=100, default='Administrative Officer')

    def __str__(self):
        return f"Staff: {self.user.username} ({self.employee_id})"
