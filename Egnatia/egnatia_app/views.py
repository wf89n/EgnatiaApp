from django.shortcuts import render
from django.http import JsonResponse
from .models import Group, Department, Role

def filter_groups(request):
    region_id = request.GET.get('region_id')
    if not region_id:
        return JsonResponse({'error': 'region_id is required'}, status=400)

    groups = Group.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse({'groups': list(groups)})

def filter_departments(request):
    region_id = request.GET.get('region_id')
    if not region_id:
        return JsonResponse({'error': 'region_id is required'}, status=400)

    departments = Department.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse({'departments': list(departments)})

def filter_roles(request):
    region_id = request.GET.get('region_id')
    if not region_id:
        return JsonResponse({'error': 'region_id is required'}, status=400)

    roles = Role.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse({'roles': list(roles)})




from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Region
from .serializers import RegionSerializer,GroupSerializer


@api_view(['GET'])
def region_list(request):
    """Fetch all regions with their assigned and completed work details."""
    regions = Region.objects.all()
    data = []

    for region in regions:
        # Get the details for each region, similar to how you handle groups
        region_data = {
            'id': region.id,
            'name': region.name,
            'groups': []  # Initialize an empty list for groups
        }

        # Assuming each region has associated groups, let's fetch the details for those groups
        for group in region.groups.all():  # Iterate through the groups associated with the region
            department_costs = group.get_departments_costs()  # Method for getting department costs
            group_data = {
                'id': group.id,
                'name': group.name,
                'total_expenses': group.total_expenses,
                'total_meters_assigned': group.total_meters_assigned,
                'total_meters_done': group.total_meters_done,
                'departments_costs': department_costs,  # Add department costs here
            }
            region_data['groups'].append(group_data)  # Append the group data to the region data

        # Add the region data to the main data list
        data.append(region_data)

    return JsonResponse(data, safe=False)

from django.shortcuts import render
from django.http import JsonResponse
from .models import BasicInfo
from .forms import BasicInfoForm  # You will need to create this form
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BasicInfoSerializer  # You'll need to create this serializer

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@ensure_csrf_cookie  # Ensures CSRF token is set
@csrf_protect  # Enforces CSRF protection
@api_view(['POST'])
def create_basic_info(request):
    serializer = BasicInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
def group_list(request):
    groups = Group.objects.all()
    data = []

    for group in groups:
        # Make sure total_expenses is updated
        group.save()  # This will trigger the calculation of total_expenses

        # Get department costs
        department_costs = group.get_departments_costs()

        group_data = {
            'id': group.id,
            'name': group.name,
            'total_expenses': float(group.total_expenses),  # Ensure this is returned as a float
            'total_meters_assigned': group.total_meters_assigned,
            'total_meters_done': group.total_meters_done,
            'departments_costs': department_costs,  # Add department costs here
        }
        data.append(group_data)

    return JsonResponse(data, safe=False)

@api_view(['GET'])
def group_detail(request, pk):
    """Fetch details of a single group."""
    try:
        group = Group.objects.get(pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=404)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Department, GroupDepartment, Role, Employee, BasicInfo
from .serializers import DepartmentSerializer, GroupDepartmentSerializer, RoleSerializer, EmployeeSerializer, BasicInfoSerializer

@api_view(['GET'])
def department_list(request):
    """Fetch all departments."""
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def group_department_list(request):
    """Fetch all group-department relationships."""
    group_departments = GroupDepartment.objects.all()
    serializer = GroupDepartmentSerializer(group_departments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def role_list(request):
    """Fetch all roles."""
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def employee_list(request):
    """Fetch all employees."""
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def employee_detail(request, pk):
    """Fetch details of a single employee."""
    try:
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)



from .models import Customer
from .serializers import CustomerSerializer

@api_view(['GET'])
def customer_list(request):
    """Fetch all customers with their assigned and completed work details."""
    customers = Customer.objects.all()
    data = []

    for customer in customers:
        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'total_meters_assigned': customer.total_meters_assigned,
            'total_freatio_assigned': customer.total_freatio_assigned,
            'total_cabins_assigned': customer.total_cabins_assigned,
            'total_catheta_assigned': customer.total_catheta_assigned,
            'total_meters_done': customer.total_meters_done,
            'total_freatio_done': customer.total_freatio_done,
            'total_cabins_done': customer.total_cabins_done,
            'total_catheta_done': customer.total_catheta_done,
        }
        data.append(customer_data)

    return Response(data)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Region, Group, BasicInfo, AttendanceReport, DailyAttendance
from .serializers import (
    RegionSerializer,
    GroupSerializer,
    BasicInfoSerializer,
    AttendanceReportSerializer
)


# ✅ Fetch People By Group (For Attendance)
@api_view(['GET'])
def people_by_group(request, group_id):
    """Fetch all people in a specific group."""
    people = BasicInfo.objects.filter(group_id=group_id)
    serializer = BasicInfoSerializer(people, many=True)
    return Response(serializer.data)


# ✅ Fetch Attendance Reports By Group
@api_view(['GET'])
def attendance_reports_by_group(request, group_id):
    """Fetch attendance reports for a given group."""
    reports = AttendanceReport.objects.filter(group_id=group_id).order_by('-date')
    serializer = AttendanceReportSerializer(reports, many=True)
    return Response(serializer.data)


import logging

logger = logging.getLogger(__name__)

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DailyAttendance, AttendanceReport, BasicInfo
from datetime import date


@api_view(['POST'])
def submit_attendance(request):
    try:
        data = request.data

        # Validate the incoming data
        group_id = data.get('group_id')
        attendance_data = data.get('attendance')

        if not group_id:
            return Response({"error": "Missing group_id"}, status=400)

        if not attendance_data:
            return Response({"error": "Missing attendance data"}, status=400)

        # Try to fetch or create the AttendanceReport for the given group_id
        attendance_report, created = AttendanceReport.objects.get_or_create(
            group_id=group_id,
            date=date.today()
        )

        # Loop through each attendance entry and create DailyAttendance objects
        for entry in attendance_data:
            employee_id = entry.get('employee_id')
            presence = entry.get('presence')

            if not employee_id or not presence:
                continue  # Skip if any data is missing, or handle it as needed

            # Get the employee (BasicInfo instance) by employee_id
            try:
                employee = BasicInfo.objects.get(id=employee_id)
            except BasicInfo.DoesNotExist:
                continue  # Skip if the employee doesn't exist

            # Check if the DailyAttendance already exists for this employee and report
            existing_attendance = DailyAttendance.objects.filter(
                attendance_report=attendance_report,
                basic_info=employee
            )

            if existing_attendance.exists():
                continue  # Skip if attendance already exists

            # Create the DailyAttendance record
            DailyAttendance.objects.create(
                attendance_report=attendance_report,
                basic_info=employee,
                presence=presence,
                date=date.today()
            )

        return Response({"message": "Attendance submitted successfully"}, status=200)

    except Exception as e:
        return Response({"error": f"Something went wrong: {str(e)}"}, status=500)
