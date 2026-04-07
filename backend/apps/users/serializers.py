from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from apps.users.models import StudentProfile, FacultyProfile, StaffProfile, Role
from apps.academic.models import Department

User = get_user_model()

class DepartmentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'code', 'name']

class StudentProfileSerializer(serializers.ModelSerializer):
    department_details = DepartmentMinimalSerializer(source='department', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'enrollment_number', 'department', 'department_details', 'batch_year', 'semester', 'guardian_name', 'guardian_phone', 'address']

class FacultyProfileSerializer(serializers.ModelSerializer):
    department_details = DepartmentMinimalSerializer(source='department', read_only=True)

    class Meta:
        model = FacultyProfile
        fields = ['id', 'employee_id', 'department', 'department_details', 'designation', 'specialization', 'joining_date']

class StaffProfileSerializer(serializers.ModelSerializer):
    department_details = DepartmentMinimalSerializer(source='department', read_only=True)

    class Meta:
        model = StaffProfile
        fields = ['id', 'employee_id', 'department', 'department_details', 'designation']

class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)
    faculty_profile = FacultyProfileSerializer(read_only=True)
    staff_profile = StaffProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'role', 'phone_number', 'avatar_url', 'is_active', 'student_profile', 'faculty_profile', 'staff_profile', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    # Profile specific fields
    enrollment_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    employee_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    department_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    batch_year = serializers.IntegerField(write_only=True, required=False, default=2026)
    semester = serializers.IntegerField(write_only=True, required=False, default=1)
    designation = serializers.CharField(write_only=True, required=False, default='')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'first_name', 'last_name', 
            'role', 'phone_number', 'avatar_url', 'enrollment_number', 
            'employee_id', 'department_id', 'batch_year', 'semester', 'designation'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.get('role', Role.STUDENT)
        enrollment_number = validated_data.pop('enrollment_number', None)
        employee_id = validated_data.pop('employee_id', None)
        department_id = validated_data.pop('department_id', None)
        batch_year = validated_data.pop('batch_year', 2026)
        semester = validated_data.pop('semester', 1)
        designation = validated_data.pop('designation', '')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        dept = None
        if department_id:
            dept = Department.objects.filter(id=department_id).first()

        if role == Role.STUDENT:
            enr = enrollment_number or f"STU{user.id:05d}"
            StudentProfile.objects.create(
                user=user,
                enrollment_number=enr,
                department=dept,
                batch_year=batch_year,
                semester=semester
            )
        elif role == Role.FACULTY:
            emp = employee_id or f"FAC{user.id:04d}"
            FacultyProfile.objects.create(
                user=user,
                employee_id=emp,
                department=dept,
                designation=designation or 'Assistant Professor'
            )
        elif role == Role.STAFF:
            emp = employee_id or f"STF{user.id:04d}"
            StaffProfile.objects.create(
                user=user,
                employee_id=emp,
                department=dept,
                designation=designation or 'Administrative Officer'
            )

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user)
        data['user'] = serializer.data
        return data
