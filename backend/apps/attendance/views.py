from rest_framework import viewsets, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from apps.attendance.models import AttendanceSession, AttendanceRecord, AttendanceStatus
from apps.attendance.serializers import AttendanceSessionSerializer, AttendanceRecordSerializer, BulkAttendanceSerializer
from apps.academic.models import Subject
from apps.users.permissions import IsFaculty, IsCollegeAdmin
from apps.core.utils import api_response

User = get_user_model()

class AttendanceSessionViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSession.objects.all().order_by('-date', '-created_at')
    serializer_class = AttendanceSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject', 'faculty', 'date', 'section']
    search_fields = ['subject__code', 'subject__name', 'section']

    def perform_create(self, serializer):
        serializer.save(faculty=self.request.user)

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all().order_by('-created_at')
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['session', 'student', 'status']

class BulkAttendanceView(APIView):
    permission_classes = [IsFaculty]

    def post(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST, success=False)

        data = serializer.validated_data
        try:
            subject = Subject.objects.get(id=data['subject_id'])
        except Subject.DoesNotExist:
            return api_response(message="Subject not found", status_code=status.HTTP_404_NOT_FOUND, success=False)

        session, created = AttendanceSession.objects.get_or_create(
            subject=subject,
            date=data['date'],
            section=data.get('section', 'A'),
            defaults={
                'faculty': request.user,
                'slot_time': data.get('slot_time', '09:00 AM - 10:00 AM'),
                'remarks': data.get('remarks', '')
            }
        )

        records_created = 0
        records_updated = 0

        for item in data['records']:
            student_id = item.get('student_id')
            rec_status = item.get('status', AttendanceStatus.PRESENT)
            remarks = item.get('remarks', '')

            try:
                student = User.objects.get(id=student_id)
            except User.DoesNotExist:
                continue

            rec, rec_created = AttendanceRecord.objects.update_or_create(
                session=session,
                student=student,
                defaults={'status': rec_status, 'remarks': remarks}
            )

            if rec_created:
                records_created += 1
            else:
                records_updated += 1

        session_serializer = AttendanceSessionSerializer(session)
        return api_response(
            data=session_serializer.data,
            message=f"Attendance processed successfully ({records_created} added, {records_updated} updated)",
            status_code=status.HTTP_200_OK
        )

class StudentAttendanceSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id=None):
        target_student = request.user
        if student_id and request.user.is_faculty_user():
            try:
                target_student = User.objects.get(id=student_id)
            except User.DoesNotExist:
                return api_response(message="Student not found", status_code=status.HTTP_404_NOT_FOUND, success=False)

        records = AttendanceRecord.objects.filter(student=target_student)
        total_classes = records.count()
        present_classes = records.filter(status__in=[AttendanceStatus.PRESENT, AttendanceStatus.LATE]).count()
        absent_classes = records.filter(status=AttendanceStatus.ABSENT).count()
        percentage = round((present_classes / total_classes * 100), 2) if total_classes > 0 else 100.0

        # Subject breakdown
        subject_stats = []
        subjects = Subject.objects.filter(attendance_sessions__records__student=target_student).distinct()
        for subj in subjects:
            subj_records = records.filter(session__subject=subj)
            s_total = subj_records.count()
            s_present = subj_records.filter(status__in=[AttendanceStatus.PRESENT, AttendanceStatus.LATE]).count()
            s_pct = round((s_present / s_total * 100), 2) if s_total > 0 else 100.0
            subject_stats.append({
                'subject_id': subj.id,
                'subject_code': subj.code,
                'subject_name': subj.name,
                'total_classes': s_total,
                'present_classes': s_present,
                'percentage': s_pct
            })

        return api_response(data={
            'student_id': target_student.id,
            'student_name': target_student.get_full_name() or target_student.username,
            'total_classes': total_classes,
            'present_classes': present_classes,
            'absent_classes': absent_classes,
            'overall_percentage': percentage,
            'subject_breakdown': subject_stats
        }, message="Attendance summary retrieved successfully")
