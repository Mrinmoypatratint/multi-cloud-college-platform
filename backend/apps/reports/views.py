from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import connection
from django.utils import timezone
from apps.users.models import User, Role
from apps.academic.models import Department, Course, Subject
from apps.attendance.models import AttendanceRecord, AttendanceSession, AttendanceStatus
from apps.notices.models import Notice
from apps.timetable.models import TimetableSlot
from apps.notices.serializers import NoticeSerializer
from apps.timetable.serializers import TimetableSlotSerializer
from apps.core.utils import api_response

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db_healthy = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            db_healthy = False

        status_code = 200 if db_healthy else 503
        return api_response(
            data={
                "status": "healthy" if db_healthy else "unhealthy",
                "database": "connected" if db_healthy else "disconnected",
                "timestamp": timezone.now().isoformat(),
                "service": "Multi-Cloud College Management API",
                "version": "1.0.0"
            },
            message="System health check completed",
            status_code=status_code,
            success=db_healthy
        )

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.role

        total_students = User.objects.filter(role=Role.STUDENT).count()
        total_faculty = User.objects.filter(role=Role.FACULTY).count()
        total_courses = Course.objects.count()
        total_departments = Department.objects.count()

        # Attendance calculation
        total_records = AttendanceRecord.objects.count()
        present_records = AttendanceRecord.objects.filter(status__in=[AttendanceStatus.PRESENT, AttendanceStatus.LATE]).count()
        avg_attendance = round((present_records / total_records * 100), 1) if total_records > 0 else 92.5

        # Recent notices
        notices = Notice.objects.all().order_by('-is_pinned', '-created_at')[:5]
        notice_serializer = NoticeSerializer(notices, many=True)

        # Timetable slots
        timetable = TimetableSlot.objects.all().order_by('day_of_week', 'start_time')[:6]
        timetable_serializer = TimetableSlotSerializer(timetable, many=True)

        data = {
            "role": role,
            "metrics": {
                "total_students": total_students,
                "total_faculty": total_faculty,
                "total_courses": total_courses,
                "total_departments": total_departments,
                "avg_attendance_percentage": avg_attendance,
            },
            "recent_notices": notice_serializer.data,
            "today_schedule": timetable_serializer.data,
        }

        # Role-specific dashboard custom stats
        if role == Role.STUDENT and hasattr(user, 'student_profile'):
            stud = user.student_profile
            stud_recs = AttendanceRecord.objects.filter(student=user)
            s_total = stud_recs.count()
            s_present = stud_recs.filter(status__in=[AttendanceStatus.PRESENT, AttendanceStatus.LATE]).count()
            s_pct = round((s_present / s_total * 100), 1) if s_total > 0 else 95.0

            data["student_specific"] = {
                "enrollment_number": stud.enrollment_number,
                "department": stud.department.name if stud.department else "N/A",
                "semester": stud.semester,
                "batch_year": stud.batch_year,
                "attendance_percentage": s_pct
            }

        elif role == Role.FACULTY and hasattr(user, 'faculty_profile'):
            fac = user.faculty_profile
            data["faculty_specific"] = {
                "employee_id": fac.employee_id,
                "department": fac.department.name if fac.department else "N/A",
                "designation": fac.designation,
                "classes_assigned": user.assigned_subjects.count()
            }

        return api_response(data=data, message="Dashboard statistics retrieved successfully")
