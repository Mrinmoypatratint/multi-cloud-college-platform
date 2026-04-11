from rest_framework import serializers
from apps.attendance.models import AttendanceSession, AttendanceRecord
from django.contrib.auth import get_user_model

User = get_user_model()

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    enrollment_number = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'session', 'student', 'student_name', 'enrollment_number', 'status', 'remarks', 'created_at']

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username

    def get_enrollment_number(self, obj):
        if hasattr(obj.student, 'student_profile'):
            return obj.student.student_profile.enrollment_number
        return "N/A"

class AttendanceSessionSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    faculty_name = serializers.SerializerMethodField()
    records = AttendanceRecordSerializer(many=True, read_only=True)
    present_count = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSession
        fields = ['id', 'subject', 'subject_code', 'subject_name', 'faculty', 'faculty_name', 'date', 'slot_time', 'section', 'remarks', 'records', 'present_count', 'total_students', 'created_at']

    def get_faculty_name(self, obj):
        return obj.faculty.get_full_name() or obj.faculty.username

    def get_present_count(self, obj):
        return obj.records.filter(status='PRESENT').count()

    def get_total_students(self, obj):
        return obj.records.count()

class BulkAttendanceSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
    slot_time = serializers.CharField(required=False, default='09:00 AM - 10:00 AM')
    section = serializers.CharField(required=False, default='A')
    remarks = serializers.CharField(required=False, allow_blank=True, default='')
    records = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )
