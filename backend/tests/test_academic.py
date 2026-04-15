from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.models import Role
from apps.academic.models import Department, Course, Subject, DegreeLevel

User = get_user_model()

class AcademicTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin_user',
            password='password123',
            role=Role.COLLEGE_ADMIN
        )
        self.student = User.objects.create_user(
            username='student_user',
            password='password123',
            role=Role.STUDENT
        )
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(
            code='BTECH-CSE', name='BTech Computer Science',
            department=self.dept, degree_level=DegreeLevel.BACHELOR
        )

    def test_create_department_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('department-list')
        response = self.client.post(url, {
            'code': 'ECE',
            'name': 'Electronics Engineering',
            'description': 'Dept of ECE'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.filter(code='ECE').count(), 1)

    def test_create_department_as_student_forbidden(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('department-list')
        response = self.client.post(url, {
            'code': 'ME',
            'name': 'Mechanical'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_departments_authenticated(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
