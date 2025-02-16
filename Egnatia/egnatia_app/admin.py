from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BasicInfo, Studies, WorkExperience, SeminarTraining,   OtherKnowledge ,OtherLanguages,GroupDepartment
from django.utils.html import format_html
from django.utils import timezone

# Registering BasicInfo model

from django.contrib import admin
from .models import BasicInfo
from .forms import BasicInfoForm  # Import the custom form

@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    form = BasicInfoForm  # Use the custom form
    list_display = ('first_name', 'last_name', 'email', 'salary', 'total_pay')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('gender', 'department', 'employee_status')

    def total_pay(self, obj):
        return obj.total_pay()

    total_pay.short_description = 'Total Pay'


# Registering Studies model
@admin.register(Studies)
class StudiesAdmin(admin.ModelAdmin):
    list_display = ('period_1', 'study_1', 'period_2', 'study_2', 'period_3', 'study_3')
    search_fields = ('study_1', 'study_2', 'study_3')  # Enable search by study topics
    list_filter = ('period_1', 'period_2', 'period_3')  # Filter by periods

# Registering WorkExperience model
@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('period_1_start', 'period_1_end', 'period_2_start', 'period_2_end', 'period_3_start', 'period_3_end', 'period_4_start', 'period_4_end', 'period_5_start', 'period_5_end')
    search_fields = ('work_1', 'work_2', 'work_3', 'work_4', 'work_5')  # Enable search by work description
    list_filter = ('period_1_start', 'period_2_start', 'period_3_start', 'period_4_start', 'period_5_start')  # Filter by periods

# Registering SeminarTraining model
@admin.register(SeminarTraining)
class SeminarTrainingAdmin(admin.ModelAdmin):
    list_display = (
        'period_1_start', 'period_1_end', 'seminar_1',
        'period_2_start', 'period_2_end', 'seminar_2',
        'period_3_start', 'period_3_end', 'seminar_3',
        'period_4_start', 'period_4_end', 'seminar_4',
        'period_5_start', 'period_5_end', 'seminar_5'
    )
    search_fields = ('seminar_1', 'seminar_2', 'seminar_3', 'seminar_4', 'seminar_5')
    list_filter = ('period_1_start', 'period_2_start', 'period_3_start', 'period_4_start', 'period_5_start')


@admin.register(OtherKnowledge)
class OtherKnowledgeAdmin(admin.ModelAdmin):
    list_display = ('basic_info', 'skill_name', 'skill_2_name', 'skill_3_name')  # Fields to display in the list view
    search_fields = ('skill_name', 'skill_2_name', 'skill_3_name')  # Searchable fields

    fields = ('basic_info', 'skill_name', 'skill_2_name', 'skill_3_name')  # Fields to display in the form





# Registering OtherLanguages model
@admin.register(OtherLanguages)
class OtherLanguagesAdmin(admin.ModelAdmin):
    list_display = ('basic_info', 'language_name', 'comment')  # Display language name and comment in the list view
    search_fields = ('language_name', 'comment')  # Enable search by language name and comment
    list_filter = ('basic_info',)


from .models import DailyAttendance,AttendanceReport


# Inline model for DailyAttendance in AttendanceReport
class DailyAttendanceInline(admin.TabularInline):
    model = DailyAttendance
    fields = ('basic_info', 'presence', 'quantity', 'po_number', 'site_id', 'site_name')
    extra = 0  # Avoid showing extra blank rows

# Custom action to mark all attendance as present
def mark_all_as_present(modeladmin, request, queryset):
    queryset.update(presence='YES')

mark_all_as_present.short_description = "Mark all selected attendance as present"
# Custom action to mark all attendance as present


# AttendanceReportAdmin for managing attendance per group
@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ('group', 'date', 'get_total_attendance')
    inlines = [DailyAttendanceInline]
    actions = [mark_all_as_present]  # Custom action to bulk mark attendance as present

    def get_total_attendance(self, obj):
        total_present = obj.daily_attendances.filter(presence='YES').count()
        return total_present
    get_total_attendance.short_description = 'Total Present'

# DailyAttendanceAdmin for managing individual attendance records
@admin.register(DailyAttendance)
class DailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('basic_info', 'date', 'presence', 'quantity', 'po_number', 'site_id', 'site_name')
    list_filter = ('presence', 'date')
    search_fields = ('basic_info__first_name', 'basic_info__last_name', 'site_name')
    date_hierarchy = 'date'  # Allows filtering by date hierarchy

    # Automatically set today's date for new DailyAttendance
    def save_model(self, request, obj, form, change):
        if not obj.date:
            obj.date = timezone.now().date()  # Ensure that date is set to today's date
        obj.save()
from django.db.models import Sum


from .models import Region, Group, Department, Role, Employee, BasicInfo

# Register Region
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'total_meters_assigned', 'total_meters_done',
        'total_freatio_assigned', 'total_freatio_done',
        'total_cabins_assigned', 'total_cabins_done',
        'total_catheta_assigned', 'total_catheta_done', 'department_expenses_summary'
    )

    search_fields = ('name',)

    readonly_fields = (
        'total_meters_assigned', 'total_meters_done',
        'total_freatio_assigned', 'total_freatio_done',
        'total_cabins_assigned', 'total_cabins_done',
        'total_catheta_assigned', 'total_catheta_done'
    )

    def department_expenses_summary(self, obj):
        """Displays the total expenses for all departments in all groups within the region."""
        groups_in_region = obj.groups.all()  # Get all groups within the region
        if not groups_in_region.exists():
            return "No Groups in Region"

        total_expenses = 0  # Initialize the total expenses

        summary_html = "<ul>"
        # Iterate over each group in the region
        for group in groups_in_region:
            group_departments = GroupDepartment.objects.filter(group=group)
            if not group_departments.exists():
                continue  # If no departments for this group, skip it

            # Iterate over each department in the group and sum their expenses
            for group_department in group_departments:
                department_name = group_department.department.name
                total_cost = group_department.total_department_cost() or 0
                summary_html += f"<li><strong>{department_name}:</strong> {total_cost:.2f}</li>"

                # Add to the total expenses
                total_expenses += total_cost

        summary_html += "</ul>"
        summary_html += f"<strong>Total Expenses for Region:</strong> {total_expenses:.2f}"  # Display total expenses for the region
        return format_html(summary_html)

    department_expenses_summary.short_description = "Department Expenses Summary for Region"

# Register Group

from django.contrib import admin
from django.utils.html import format_html
from .models import Group, GroupDepartment,   Customer, AssignJob, DailyProgram

from django.contrib import admin
from django.utils.html import format_html

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'region',
        'department_expenses_summary',
        'total_meters_assigned',
        'total_meters_done',
        'total_freatio_assigned',
        'total_freatio_done',
        'total_cabins_assigned',
        'total_cabins_done',
        'total_catheta_assigned',
        'total_catheta_done'
    )

    readonly_fields = (
        'total_expenses',  # Make the total_expenses field read-only
        'total_meters_assigned',
        'total_meters_done',
        'total_freatio_assigned',
        'total_freatio_done',
        'total_cabins_assigned',
        'total_cabins_done',
        'total_catheta_assigned',
        'total_catheta_done'
    )

    list_filter = ('region',)
    search_fields = ('name', 'region__name')

    def department_expenses_summary(self, obj):
        """Displays the total expenses for each department in the group."""
        group_departments = GroupDepartment.objects.filter(group=obj)
        if not group_departments.exists():
            return "No Departments"

        total_expenses = 0  # Initialize the total expenses

        summary_html = "<ul>"
        for group_department in group_departments:
            department_name = group_department.department.name
            total_cost = group_department.total_department_cost() or 0
            summary_html += f"<li><strong>{department_name}:</strong> {total_cost:.2f}</li>"

            # Add to the total expenses
            total_expenses += total_cost

        summary_html += "</ul>"
        summary_html += f"<strong>Total Expenses:</strong> {total_expenses:.2f}"  # Display total expenses
        return format_html(summary_html)

    department_expenses_summary.short_description = "Department Expenses Summary"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)  # Define search fields for department
    list_filter = ('name',)

@admin.register(GroupDepartment)
class GroupDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'department')
# Register Role
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'parent')
    search_fields = ('name', 'department__name', 'department__group__name')
    list_filter = ('department',)  # Filter roles by department

    def get_queryset(self, request):
        # Override the default queryset to filter roles by the selected department
        queryset = super().get_queryset(request)
        department_id = request.GET.get('department')  # Get the selected department ID from the URL params
        if department_id:
            queryset = queryset.filter(department_id=department_id)  # Filter by department
        return queryset


# Register Employee model with filtering on Region, Group, Department, Role
from django.db.models import Q

import logging
from django.contrib import admin
from .models import Employee, Region, Group, Department, Role



from django.utils.safestring import mark_safe



class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('basic_info', 'region', 'group', 'department', 'role')
    list_filter = ('region', 'group', 'department', 'role')

    class Media:
        js = ('js/admin_filter.js',)  # Link to your custom JavaScript file

admin.site.register(Employee, EmployeeAdmin)


from .models import CloseBC

@admin.register(CloseBC)
class CloseBCAdmin(admin.ModelAdmin):
    list_display = ('source_id', 'sub', 'date', 'rol', 'building_task_type', 'area')  # Display these fields
    list_filter = ('date', 'rol', 'building_task_type', 'area')  # Add filters
    search_fields = ('source_id', 'rol', 'sub')  # Enable searching by specific fields
    autocomplete_fields = ('area',)  # Enable autocomplete for the area field


from .models import Cancel

@admin.register(Cancel)
class CancelAdmin(admin.ModelAdmin):
    list_display = ('sr', 'date_cancelled', 'finished', 'is_checked')  # Display related SR, date, and status
    search_fields = ('sr__sr_code', 'sr__code')


from .models import ClosedSSR

@admin.register(ClosedSSR)
class ClosedSSRAdmin(admin.ModelAdmin):
    list_display = ('source_id', 'sub', 'date', 'rollout_engineer', 'area')  # Display these fields in admin
    list_filter = ('date', 'rollout_engineer', 'area')  # Add filters
    search_fields = ('source_id', 'sub', 'rollout_engineer')  # Enable search by key fields
    autocomplete_fields = ('area',)  # Use autocomplete for area field



from .models import WFM

@admin.register(WFM)
class WFMAdmin(admin.ModelAdmin):
    list_display = ('sr', 'ak', 'address', 'date', 'area', 'type')  # Show these fields in the admin list view
    list_filter = ('date', 'area', 'type')  # Add filters for date, area, and type
    search_fields = ('sr', 'ak', 'address')  # Enable searching by SR, AK, or address
    autocomplete_fields = ('area',)  # Use autocomplete for the area field


from .models import Info


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('ak', 'roll', 'get_area')  # Show AK, Roll, and areas in the admin list view
    list_filter = ('roll',)  # Add filters for roll
    search_fields = ('ak', 'area__name')  # Enable searching by AK or area name
    autocomplete_fields = ('area',)  # Use autocomplete for the area field

    def get_area(self, obj):
        # This function will show the names of all selected regions in the admin list
        return ', '.join([region.name for region in obj.area.all()])

    get_area.short_description = 'Area'


from .models import InfoCodeSr


@admin.register(InfoCodeSr)
class InfoCodeSrAdmin(admin.ModelAdmin):
    list_display = ('code_sr', 'type', 'get_area')  # Show CODE SR, TYPE, and AREA in the list view
    list_filter = ('type', 'area')  # Add filters for TYPE and AREA
    search_fields = ('code_sr', 'type', 'area__name')  # Enable searching by CODE SR, TYPE, or AREA
    autocomplete_fields = ('area',)  # Use autocomplete for the area field

    def get_area(self, obj):
        # Return area name or a placeholder if no area is selected
        return obj.area.name if obj.area else 'No Area'

    get_area.short_description = 'Area'


from .models import InfoOldNew

@admin.register(InfoOldNew)
class InfoOldNewAdmin(admin.ModelAdmin):
    list_display = ('old', 'new')  # Show OLD and NEW in the list view
    search_fields = ('old', 'new')  # Enable searching by OLD or NEW


from .models import Assign

@admin.register(Assign)
class AssignAdmin(admin.ModelAdmin):
    list_display = ('sr', 'roll1', 'roll2', 'area', 'wfm')  # Show relevant fields in the admin list view
    list_filter = ('roll1', 'area', 'wfm')  # Add filters for roll1, area, and wfm
    search_fields = ('sr', 'roll1', 'area')  # Enable searching by SR, roll1, or area


from .models import Sr

@admin.register(Sr)
class SrAdmin(admin.ModelAdmin):
    list_display = ('sr_code', 'building_id', 'building_task_type', 'sub', 'sub_old', 'time_created', 'type')
    search_fields = ('sr_code', 'sub', 'building_task_type')




@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_meters_assigned', 'total_meters_done',
                    'total_freatio_assigned', 'total_freatio_done',
                    'total_cabins_assigned', 'total_cabins_done',
                    'total_catheta_assigned', 'total_catheta_done')

    readonly_fields = ('total_meters_assigned', 'total_meters_done',
                       'total_freatio_assigned', 'total_freatio_done',
                       'total_cabins_assigned', 'total_cabins_done',
                       'total_catheta_assigned', 'total_catheta_done')

    search_fields = ('name',)

@admin.register(AssignJob)
class AssignJobAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'region', 'group', 'meters', 'freatio', 'cabins', 'katheta')

    search_fields = ('customer__name', 'region__name', 'group__name')

    # Show only assigned fields in the admin panel
    fields = ('customer', 'region', 'group', 'meters', 'freatio', 'cabins', 'katheta')

    def customer_name(self, obj):
        return obj.customer.name

    customer_name.short_description = "Customer Name"



@admin.register(DailyProgram)
class DailyProgramAdmin(admin.ModelAdmin):
    list_display = ('group', 'region', 'program_pdf_file',
                    'total_meters_assigned', 'total_meters_done',
                    'total_freatio_assigned', 'total_freatio_done',
                    'total_cabins_assigned', 'total_cabins_done',
                    'total_catheta_assigned', 'total_catheta_done')
    search_fields = ('group__name', 'region__name')