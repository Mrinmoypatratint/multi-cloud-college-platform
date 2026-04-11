from rest_framework import serializers
from apps.academic.models import Department, Course, Subject, SubjectFacultyAssignment
from django.contrib.auth import get_user_model

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.SerializerMethodField()
    courses_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'code', 'name', 'description', 'head_of_department', 'head_name', 'courses_count', 'students_count', 'created_at']

    def get_head_name(self, obj):
        if obj.head_of_department:
            return obj.head_of_department.get_full_name() or obj.head_of_department.username
        return "Unassigned"

    def get_courses_count(self, obj):
        return obj.courses.count()

    def get_students_count(self, obj):
        return obj.students.count()

class CourseSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source='department.code', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    subjects_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'department', 'department_code', 'department_name', 'duration_years', 'degree_level', 'subjects_count', 'created_at']

    def get_subjects_count(self, obj):
        return obj.subjects.count()

class SubjectSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'course', 'course_code', 'course_name', 'semester', 'credits', 'description', 'created_at']

class SubjectFacultyAssignmentSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    faculty_name = serializers.SerializerMethodField()

    class Meta:
        model = SubjectFacultyAssignment
        fields = ['id', 'subject', 'subject_code', 'subject_name', 'faculty', 'faculty_name', 'academic_year', 'section', 'created_at']

    def get_faculty_name(self, obj):
        return obj.faculty.get_full_name() or obj.faculty.username
