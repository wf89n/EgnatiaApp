from rest_framework import serializers
from .models import Region

from .models import Region, Group,AttendanceReport, DailyAttendance

class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the Group model."""

    class Meta:
        model = Group
        fields = ['id', 'name', 'total_meters_assigned', 'total_freatio_assigned', 'total_cabins_assigned', 'total_catheta_assigned',
                  'total_meters_done', 'total_freatio_done', 'total_cabins_done', 'total_catheta_done', 'total_expenses']

class RegionSerializer(serializers.ModelSerializer):
    """Serializer for the Region model, including nested Groups."""

    groups = GroupSerializer(many=True, read_only=True)  # Include related groups

    class Meta:
        model = Region
        fields = ['id', 'name', 'groups']  # Include other fields as needed


from rest_framework import serializers
from .models import Department, GroupDepartment, Role, Employee, BasicInfo


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for the Department model."""

    class Meta:
        model = Department
        fields = ['id', 'name']


class GroupDepartmentSerializer(serializers.ModelSerializer):
    """Serializer for the GroupDepartment model."""
    group_name = serializers.CharField(source='group.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = GroupDepartment
        fields = ['id', 'group', 'department', 'group_name', 'department_name']


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for the Role model."""
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'department', 'name', 'parent', 'department_name']


class BasicInfoSerializer(serializers.ModelSerializer):
    """Serializer for the BasicInfo model."""

    class Meta:
        model = BasicInfo
        fields = ['id', 'first_name', 'last_name', 'father_name', 'location', 'gender', 'marital_status',
                  'date_of_birth',
                  'mobile_phone', 'landline_phone', 'email', 'tax_id', 'address', 'department', 'responsibilities',
                  'specialization', 'degree_available', 'salary', 'iban', 'hiring_date', 'employee_status',
                  'termination_date', 'medical_exams', 'medical_exams_date', 'medical_exams_renewal_date',
                  'safety_passport', 'safety_passport_date', 'safety_passport_renewal_date', 'certifications_seminars']


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for the Employee model."""
    basic_info = BasicInfoSerializer()
    role_name = serializers.CharField(source='role.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'basic_info', 'role', 'role_name', 'department', 'department_name', 'group', 'group_name']


from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for the Customer model."""

    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'total_meters_assigned',
            'total_freatio_assigned',
            'total_cabins_assigned',
            'total_catheta_assigned',
            'total_meters_done',
            'total_freatio_done',
            'total_cabins_done',
            'total_catheta_done',
        ]


class AttendanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceReport
        fields = '__all__'

class DailyAttendanceSerializer(serializers.ModelSerializer):
    basic_info = BasicInfoSerializer()

    class Meta:
        model = DailyAttendance
        fields = '__all__'