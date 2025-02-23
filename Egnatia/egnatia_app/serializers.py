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

from .models import BasicInfo


class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = '__all__'

    def validate(self, data):
        required_fields = ["first_name", "last_name", "father_name", "location", "gender", "marital_status"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]

        if missing_fields:
            raise serializers.ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        return data


from rest_framework import serializers
from .models import Department, GroupDepartment, Role, Employee, BasicInfo


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for the Department model."""

    class Meta:
        model = Department
        fields = ['id', 'name']


class GroupDepartmentSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = GroupDepartment
        fields = ['id', 'group', 'department', 'total_cost']

    def get_total_cost(self, obj):
        return obj.total_department_cost()


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
                  'safety_passport', 'safety_passport_date', 'safety_passport_renewal_date', 'certifications_seminars','total_pay']


    def get_total_pay(self, obj):
        # Get the total pay from BasicInfo model
        return obj.total_pay()


class EmployeeSerializer(serializers.ModelSerializer):
    basic_info = BasicInfoSerializer()
    role_name = serializers.CharField(source='role.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    photo = serializers.ImageField()
    total_pay = serializers.ReadOnlyField(source='basic_info.total_pay')  # Get the total pay

    class Meta:
        model = Employee
        fields = ['id', 'basic_info', 'role_name', 'department_name', 'photo', 'total_pay']  # No salary field


    def get_total_pay(self, obj):
        # Access the total_pay method from the BasicInfo instance
        return obj.basic_info.total_pay() if obj.basic_info else 0



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ensure the photo field contains a full URL to the image
        if instance.photo:
            representation['photo'] = instance.photo.url
        else:
            representation['photo'] = None
        return representation


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