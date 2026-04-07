from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import Role, StudentProfile, FacultyProfile, StaffProfile
from apps.academic.models import Department, Course, Subject, SubjectFacultyAssignment, DegreeLevel
from apps.attendance.models import AttendanceSession, AttendanceRecord, AttendanceStatus
from apps.timetable.models import TimetableSlot, DayOfWeek
from apps.notices.models import Notice, PriorityLevel, TargetAudience
from datetime import date, time

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial demo data for Multi-Cloud College Platform'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with demo data...')

        # 1. Create Super Admin
        super_admin, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'superadmin@college.edu',
                'first_name': 'Global',
                'last_name': 'Administrator',
                'role': Role.SUPER_ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            super_admin.set_password('admin123')
            super_admin.save()
            self.stdout.write(self.style.SUCCESS('Created Super Admin: superadmin / admin123'))

        # 2. Create College Admin
        college_admin, created = User.objects.get_or_create(
            username='collegeadmin',
            defaults={
                'email': 'admin@college.edu',
                'first_name': 'Sarah',
                'last_name': 'Connor',
                'role': Role.COLLEGE_ADMIN,
                'is_staff': True
            }
        )
        if created:
            college_admin.set_password('admin123')
            college_admin.save()
            self.stdout.write(self.style.SUCCESS('Created College Admin: collegeadmin / admin123'))

        # 3. Create Departments
        dept_cse, _ = Department.objects.get_or_create(
            code='CSE',
            defaults={'name': 'Computer Science & Engineering', 'description': 'Department of Computer Science & Engineering'}
        )
        dept_ece, _ = Department.objects.get_or_create(
            code='ECE',
            defaults={'name': 'Electronics & Communication Engg', 'description': 'Department of ECE'}
        )
        dept_me, _ = Department.objects.get_or_create(
            code='ME',
            defaults={'name': 'Mechanical Engineering', 'description': 'Department of Mechanical Engineering'}
        )

        # 4. Create Faculty
        fac1, created = User.objects.get_or_create(
            username='dr_smith',
            defaults={
                'email': 'smith@college.edu',
                'first_name': 'Robert',
                'last_name': 'Smith',
                'role': Role.FACULTY
            }
        )
        if created:
            fac1.set_password('admin123')
            fac1.save()
            FacultyProfile.objects.create(
                user=fac1,
                employee_id='FAC-1001',
                department=dept_cse,
                designation='Associate Professor',
                specialization='Distributed Systems & Cloud Computing'
            )

        fac2, created = User.objects.get_or_create(
            username='dr_davis',
            defaults={
                'email': 'davis@college.edu',
                'first_name': 'Elena',
                'last_name': 'Davis',
                'role': Role.FACULTY
            }
        )
        if created:
            fac2.set_password('admin123')
            fac2.save()
            FacultyProfile.objects.create(
                user=fac2,
                employee_id='FAC-1002',
                department=dept_cse,
                designation='Assistant Professor',
                specialization='Database Systems & Web Engineering'
            )

        # 5. Create Staff
        staff1, created = User.objects.get_or_create(
            username='staff_john',
            defaults={
                'email': 'john@college.edu',
                'first_name': 'John',
                'last_name': 'Miller',
                'role': Role.STAFF
            }
        )
        if created:
            staff1.set_password('admin123')
            staff1.save()
            StaffProfile.objects.create(
                user=staff1,
                employee_id='STF-2001',
                department=dept_cse,
                designation='Senior Registrar'
            )

        # 6. Create Courses & Subjects
        course_btech, _ = Course.objects.get_or_create(
            code='BTECH-CSE',
            defaults={'name': 'B.Tech in Computer Science', 'department': dept_cse, 'duration_years': 4, 'degree_level': DegreeLevel.BACHELOR}
        )

        subj_dsa, _ = Subject.objects.get_or_create(
            code='CS301',
            defaults={'name': 'Data Structures & Algorithms', 'course': course_btech, 'semester': 3, 'credits': 4, 'description': 'Fundamental algorithms, tree/graph structures, and complexity.'}
        )
        subj_db, _ = Subject.objects.get_or_create(
            code='CS302',
            defaults={'name': 'Database Management Systems', 'course': course_btech, 'semester': 3, 'credits': 4, 'description': 'Relational data models, SQL, transactions, and normalization.'}
        )
        subj_cloud, _ = Subject.objects.get_or_create(
            code='CS401',
            defaults={'name': 'Multi-Cloud Architecture', 'course': course_btech, 'semester': 5, 'credits': 3, 'description': 'Containerization, Kubernetes, AWS & Azure infrastructure.'}
        )

        # Assignments
        SubjectFacultyAssignment.objects.get_or_create(subject=subj_dsa, faculty=fac1, defaults={'academic_year': '2025-2026', 'section': 'A'})
        SubjectFacultyAssignment.objects.get_or_create(subject=subj_db, faculty=fac2, defaults={'academic_year': '2025-2026', 'section': 'A'})
        SubjectFacultyAssignment.objects.get_or_create(subject=subj_cloud, faculty=fac1, defaults={'academic_year': '2025-2026', 'section': 'A'})

        # 7. Create Students
        students_data = [
            ('alice_student', 'alice@student.college.edu', 'Alice', 'Johnson', 'STU-2026-001'),
            ('bob_student', 'bob@student.college.edu', 'Bob', 'Williams', 'STU-2026-002'),
            ('charlie_student', 'charlie@student.college.edu', 'Charlie', 'Brown', 'STU-2026-003'),
            ('diana_student', 'diana@student.college.edu', 'Diana', 'Prince', 'STU-2026-004')
        ]

        created_students = []
        for uname, email, fname, lname, enr in students_data:
            stu, created = User.objects.get_or_create(
                username=uname,
                defaults={
                    'email': email,
                    'first_name': fname,
                    'last_name': lname,
                    'role': Role.STUDENT
                }
            )
            if created:
                stu.set_password('admin123')
                stu.save()
                StudentProfile.objects.create(
                    user=stu,
                    enrollment_number=enr,
                    department=dept_cse,
                    batch_year=2026,
                    semester=3
                )
                self.stdout.write(self.style.SUCCESS(f"Created Student: {uname} / admin123"))
            created_students.append(stu)

        # 8. Create Timetable Slots
        TimetableSlot.objects.get_or_create(
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            subject=subj_dsa,
            defaults={'faculty': fac1, 'room_number': 'Lab 301', 'section': 'A'}
        )
        TimetableSlot.objects.get_or_create(
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(10, 15),
            end_time=time(11, 15),
            subject=subj_db,
            defaults={'faculty': fac2, 'room_number': 'Hall 102', 'section': 'A'}
        )
        TimetableSlot.objects.get_or_create(
            day_of_week=DayOfWeek.TUESDAY,
            start_time=time(11, 30),
            end_time=time(12, 30),
            subject=subj_cloud,
            defaults={'faculty': fac1, 'room_number': 'Lab 402', 'section': 'A'}
        )

        # 9. Create Attendance Sessions
        session1, _ = AttendanceSession.objects.get_or_create(
            subject=subj_dsa,
            date=date.today(),
            section='A',
            defaults={'faculty': fac1, 'slot_time': '09:00 AM - 10:00 AM', 'remarks': 'Topic: Binary Search Trees'}
        )
        for idx, stu in enumerate(created_students):
            status_val = AttendanceStatus.PRESENT if idx != 2 else AttendanceStatus.ABSENT
            AttendanceRecord.objects.get_or_create(session=session1, student=stu, defaults={'status': status_val})

        # 10. Create Notices
        Notice.objects.get_or_create(
            title='Mid-Semester Examination Schedule Announced',
            defaults={
                'content': 'The Mid-Semester examinations for 3rd and 5th Semester students will commence from October 15th. Detailed timetable is posted on the notice board.',
                'author': college_admin,
                'target_role': TargetAudience.ALL,
                'priority': PriorityLevel.HIGH,
                'is_pinned': True
            }
        )
        Notice.objects.get_or_create(
            title='Multi-Cloud Architecture Hackathon 2026',
            defaults={
                'content': 'Join the annual college cloud computing hackathon! Build production-ready workloads on AWS & Azure. Exciting prizes for top teams.',
                'author': fac1,
                'target_role': TargetAudience.STUDENT,
                'target_department': dept_cse,
                'priority': PriorityLevel.NORMAL,
                'is_pinned': False
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded all demo data!'))
