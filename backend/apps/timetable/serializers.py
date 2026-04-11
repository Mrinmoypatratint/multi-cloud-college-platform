from rest_framework import serializers
from apps.timetable.models import TimetableSlot

class TimetableSlotSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    faculty_name = serializers.SerializerMethodField()
    course_name = serializers.CharField(source='subject.course.name', read_only=True)

    class Meta:
        model = TimetableSlot
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'subject', 'subject_code', 'subject_name', 'faculty', 'faculty_name', 'course_name', 'room_number', 'section', 'created_at']

    def get_faculty_name(self, obj):
        return obj.faculty.get_full_name() or obj.faculty.username
