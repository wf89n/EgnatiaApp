from django.db import models

# Create your models here.
from django.db import models


class Region(models.Model):
    """Represents a geographical or organizational region."""
    name = models.CharField(max_length=100, unique=True)

    # Assigned work (read-only)
    total_meters_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_freatio_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_cabins_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_catheta_assigned = models.PositiveIntegerField(default=0, editable=False)

    # Completed work (read-only)
    total_meters_done = models.PositiveIntegerField(default=0, editable=False)
    total_freatio_done = models.PositiveIntegerField(default=0, editable=False)
    total_cabins_done = models.PositiveIntegerField(default=0, editable=False)
    total_catheta_done = models.PositiveIntegerField(default=0, editable=False)

    def total_cost(self):
        """Calculate the total cost for the region by summing the cost of all related groups."""
        total_cost = AssignJob.objects.filter(region=self).aggregate(
            total=Sum('group__cost'))['total'] or 0
        return total_cost

    def update_totals(self):
        """Calculate and update total assigned and completed work for this region."""
        job_totals = self.assignments.aggregate(
            total_meters_assigned=Sum('meters'),
            total_freatio_assigned=Sum('freatio'),
            total_cabins_assigned=Sum('cabins'),
            total_catheta_assigned=Sum('katheta'),
            total_meters_done=Sum('meters_done'),
            total_freatio_done=Sum('freatio_done'),
            total_cabins_done=Sum('cabins_done'),
            total_catheta_done=Sum('katheta_done'),
        )

        program_totals = self.daily_programs.aggregate(
            total_meters_assigned=Sum('total_meters_assigned'),
            total_freatio_assigned=Sum('total_freatio_assigned'),
            total_cabins_assigned=Sum('total_cabins_assigned'),
            total_catheta_assigned=Sum('total_catheta_assigned'),
            total_meters_done=Sum('total_meters_done'),
            total_freatio_done=Sum('total_freatio_done'),
            total_cabins_done=Sum('total_cabins_done'),
            total_catheta_done=Sum('total_catheta_done'),
        )

        # Assign totals from AssignJobs & DailyPrograms
        self.total_meters_assigned = (job_totals['total_meters_assigned'] or 0) + (program_totals['total_meters_assigned'] or 0)
        self.total_freatio_assigned = (job_totals['total_freatio_assigned'] or 0) + (program_totals['total_freatio_assigned'] or 0)
        self.total_cabins_assigned = (job_totals['total_cabins_assigned'] or 0) + (program_totals['total_cabins_assigned'] or 0)
        self.total_catheta_assigned = (job_totals['total_catheta_assigned'] or 0) + (program_totals['total_catheta_assigned'] or 0)

        self.total_meters_done = (job_totals['total_meters_done'] or 0) + (program_totals['total_meters_done'] or 0)
        self.total_freatio_done = (job_totals['total_freatio_done'] or 0) + (program_totals['total_freatio_done'] or 0)
        self.total_cabins_done = (job_totals['total_cabins_done'] or 0) + (program_totals['total_cabins_done'] or 0)
        self.total_catheta_done = (job_totals['total_catheta_done'] or 0) + (program_totals['total_catheta_done'] or 0)

        self.save()

    def __str__(self):
        return self.name


from django.db.models import Sum
class Group(models.Model):
    """Represents a group within a region."""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=100)
    departments = models.ManyToManyField('Department', related_name='groups', through='GroupDepartment')

    total_expenses = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        editable=False,  # Prevent manual editing
        verbose_name="Total Expenses"
    )

    # Assigned work (read-only, updated via AssignJob & DailyProgram)
    total_meters_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_freatio_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_cabins_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_catheta_assigned = models.PositiveIntegerField(default=0, editable=False)

    # Completed work (read-only, updated via AssignJob & DailyProgram)
    total_meters_done = models.PositiveIntegerField(default=0, editable=False)
    total_freatio_done = models.PositiveIntegerField(default=0, editable=False)
    total_cabins_done = models.PositiveIntegerField(default=0, editable=False)
    total_catheta_done = models.PositiveIntegerField(default=0, editable=False)

    def calculate_total_expenses(self):
        """Calculate total expenses for a group, considering both departments and the relationship with groups."""
        # Filter the expenses of all departments within the current group
        group_expenses = GroupDepartment.objects.filter(group=self)

        # Create a dictionary to store total expenses for each department within this group
        department_expenses = {}

        for group_department in group_expenses:
            department = group_department.department
            department_expenses.setdefault(department, 0)
            department_expenses[department] += group_department.total_department_cost()

        # Sum the costs for the current group
        return sum(department_expenses.values())


    def update_totals(self):
        """Update totals based on assignments and daily programs."""
        job_totals = self.assignments.aggregate(
            total_meters_assigned=Sum('meters'),
            total_freatio_assigned=Sum('freatio'),
            total_cabins_assigned=Sum('cabins'),
            total_catheta_assigned=Sum('katheta'),
            total_meters_done=Sum('meters_done'),
            total_freatio_done=Sum('freatio_done'),
            total_cabins_done=Sum('cabins_done'),
            total_catheta_done=Sum('katheta_done'),
        )

        program_totals = self.daily_programs.aggregate(
            total_meters_assigned=Sum('total_meters_assigned'),
            total_freatio_assigned=Sum('total_freatio_assigned'),
            total_cabins_assigned=Sum('total_cabins_assigned'),
            total_catheta_assigned=Sum('total_catheta_assigned'),
            total_meters_done=Sum('total_meters_done'),
            total_freatio_done=Sum('total_freatio_done'),
            total_cabins_done=Sum('total_cabins_done'),
            total_catheta_done=Sum('total_catheta_done'),
        )

        # Assign totals from AssignJobs & DailyPrograms
        self.total_meters_assigned = (job_totals['total_meters_assigned'] or 0) + (program_totals['total_meters_assigned'] or 0)
        self.total_freatio_assigned = (job_totals['total_freatio_assigned'] or 0) + (program_totals['total_freatio_assigned'] or 0)
        self.total_cabins_assigned = (job_totals['total_cabins_assigned'] or 0) + (program_totals['total_cabins_assigned'] or 0)
        self.total_catheta_assigned = (job_totals['total_catheta_assigned'] or 0) + (program_totals['total_catheta_assigned'] or 0)

        self.total_meters_done = (job_totals['total_meters_done'] or 0) + (program_totals['total_meters_done'] or 0)
        self.total_freatio_done = (job_totals['total_freatio_done'] or 0) + (program_totals['total_freatio_done'] or 0)
        self.total_cabins_done = (job_totals['total_cabins_done'] or 0) + (program_totals['total_cabins_done'] or 0)
        self.total_catheta_done = (job_totals['total_catheta_done'] or 0) + (program_totals['total_catheta_done'] or 0)

        self.save()

    def save(self, *args, **kwargs):
        """Override save to update expenses, but prevent manual total updates."""
        self.total_expenses = self.calculate_total_expenses()
        super().save(*args, **kwargs)  # Only save expenses here

    def __str__(self):
        return f"{self.name} ({self.region.name})"

    def get_departments_costs(self):
        """Return the total cost per department for this group."""
        # Call the static method from GroupDepartment to get department costs for this group
        department_costs = GroupDepartment.calculate_department_costs_for_group(self)

        # Debug: Print the resulting costs dictionary
        print(f"Department costs for group {self.name}: {department_costs}")

        return department_costs

class Department(models.Model):
    """Represents a department that can exist across multiple groups."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class GroupDepartment(models.Model):
    """Intermediate model linking Groups and Departments for payment calculations."""
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department.name} ({self.group.name})"

    def total_department_cost(self):
        """
        Calculate the total cost for this department in the current group
        by summing up salaries based on attendance.
        This now filters employees directly from the Employee model by department and group.
        """
        # Filtering employees by department and group directly via the Employee model
        employees = Employee.objects.filter(department=self.department, group=self.group)

        total = 0
        for employee in employees:
            print(f"Employee: {employee.basic_info.first_name} {employee.basic_info.last_name}")
            if employee.basic_info:
                employee_pay = employee.basic_info.total_pay()
                print(f"Employee Pay: {employee_pay}")
                total += employee_pay

        return total

    @staticmethod
    def calculate_department_costs_for_group(group):
        """Calculate department costs for all departments in a given group."""
        department_costs = {}

        # Get all GroupDepartment instances linked to the group
        group_departments = GroupDepartment.objects.filter(group=group)

        # Iterate through each group-department relation and calculate the cost
        for group_department in group_departments:
            # For each department, calculate the cost and add it to the dictionary
            department_name = group_department.department.name
            department_cost = group_department.total_department_cost()
            department_costs[department_name] = department_cost

        return department_costs


class Role(models.Model):
    """Represents roles within a department, which may have a parent-child hierarchy."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Employee(models.Model):
    """Represents an employee in a specific role."""
    basic_info = models.OneToOneField(
        'BasicInfo', on_delete=models.CASCADE, related_name='employee', verbose_name="Basic Information"
    )
    region = models.ForeignKey(
        'Region', on_delete=models.CASCADE, related_name='employees', verbose_name="Region"
    )
    group = models.ForeignKey(
        'Group', on_delete=models.CASCADE, related_name='employees', verbose_name="Group"
    )
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, related_name='employees', verbose_name="Department"
    )
    role = models.ForeignKey(
        'Role', on_delete=models.CASCADE, related_name='employees', verbose_name="Role"
    )
    photo = models.ImageField(
        upload_to='employee_photos/',  # You can define a folder where images will be stored
        null=True,
        blank=True,
        verbose_name="Employee Photo"
    )

    def __str__(self):
        return f"{self.basic_info.first_name} {self.basic_info.last_name} - {self.role.name}"

    # Existing properties for backward compatibility (optional)
    @property
    def computed_department(self):
        return self.department

    @property
    def computed_group(self):
        return self.group

    @property
    def computed_region(self):
        return self.region


class BasicInfo(models.Model):
    id = models.AutoField(primary_key=True)  # Assuming ID is unique for each record
    first_name = models.CharField(max_length=100, verbose_name="Όνομα")
    last_name = models.CharField(max_length=100, verbose_name="Επώνυμο")
    father_name = models.CharField(max_length=100, verbose_name="Πατρώνυμο")
    location = models.CharField(max_length=100, verbose_name="ΕΔΡΑ")

    gender = models.CharField(max_length=50, verbose_name="Φύλο")
    marital_status = models.CharField(max_length=50, verbose_name="Οικογενειακή Κατάσταση")
    date_of_birth = models.DateField(verbose_name="Ημερομηνία Γέννησης", null=True, blank=True)
    mobile_phone = models.CharField(max_length=15, verbose_name="Τηλέφωνο Κινητό", null=True, blank=True)
    landline_phone = models.CharField(max_length=15, verbose_name="Τηλέφωνο Σταθερό", null=True, blank=True)
    email = models.EmailField(verbose_name="e-mail", null=True, blank=True)
    tax_id = models.CharField(max_length=20, verbose_name="ΑΦΜ", null=True, blank=True)
    address = models.TextField(verbose_name="Διεύθυνση", null=True, blank=True)
    department = models.CharField(max_length=100, verbose_name="Τμήμα", null=True, blank=True)
    responsibilities = models.TextField(verbose_name="Αρμοδιότητες", null=True, blank=True)
    specialization = models.CharField(max_length=100, verbose_name="Ειδικότητα-Πτυχίο", null=True, blank=True)
    degree_available = models.FileField(
        verbose_name="Διαθέσιμο πτυχίο",
        upload_to="degrees/",
        null=True,
        blank=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Μισθός", null=True, blank=True)
    iban = models.CharField(max_length=34, verbose_name="IBAN", null=True, blank=True)
    hiring_date = models.DateField(verbose_name="Ημερομηνία Πρόσληψης", null=True, blank=True)
    employee_status = models.CharField(max_length=50, verbose_name="Κατάσταση Εργαζομένου", null=True, blank=True)
    termination_date = models.DateField(verbose_name="Ημερομηνία Λύσης συνεργασίας", null=True, blank=True)
    medical_exams = models.CharField(max_length=50, verbose_name="Ιατρικές Εξετάσεις", null=True, blank=True)
    medical_exams_date = models.DateField(verbose_name="Ημερομηνία Ιατρικών Εξετάσεων", null=True, blank=True)
    medical_exams_renewal_date = models.DateField(verbose_name="Ημερομηνία Ανανέωσης Ιατρικών Εξετάσεων", null=True, blank=True)
    safety_passport = models.CharField(max_length=50, verbose_name="Safety Passport", null=True, blank=True)
    safety_passport_date = models.DateField(verbose_name="Ημερομηνία Safety Passport", null=True, blank=True)
    safety_passport_renewal_date = models.DateField(verbose_name="Ημερομηνία Ανανέωσης Safety Passport", null=True, blank=True)
    certifications_seminars = models.TextField(verbose_name="Πιστοποιήσεις-Σεμινάρια", null=True, blank=True)

    # Calculate the total pay based on attendance
    def total_pay(self):
        # Fetch all attendance records for this BasicInfo instance where presence is 'YES'
        attendance_days = self.daily_attendance.filter(presence='YES').count()

        # If the employee has a salary, calculate the total pay
        if self.salary is not None:
            return self.salary * attendance_days
        return 0



    @property
    def group(self):
        employee = getattr(self, 'employee', None)
        if employee:
            return employee.group
        return None

    # If you want it to be non-writable in forms and admin, you can explicitly make it readonly
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"







# Studies model, relates to BasicInfo
class Studies(models.Model):
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, related_name="studies")
    period_1 = models.CharField(max_length=50, verbose_name="PERIOD 1")
    study_1 = models.TextField(verbose_name="STUDY 1", blank=True, null=True)
    period_2 = models.CharField(max_length=50, verbose_name="PERIOD 2")
    study_2 = models.TextField(verbose_name="STUDY 2", blank=True, null=True)
    period_3 = models.CharField(max_length=50, verbose_name="PERIOD 3")
    study_3 = models.TextField(verbose_name="STUDY 3", blank=True, null=True)

    def __str__(self):
        return f"Studies: {self.period_1} - {self.period_3}"


# WorkExperience model, relates to BasicInfo
class WorkExperience(models.Model):
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, related_name="work_experience")
    period_1_start = models.DateField(verbose_name="PERIOD 1 Start", null=True, blank=True)
    period_1_end = models.DateField(verbose_name="PERIOD 1 End", null=True, blank=True)
    work_1 = models.TextField(verbose_name="WORK 1", blank=True, null=True)

    period_2_start = models.DateField(verbose_name="PERIOD 2 Start", null=True, blank=True)
    period_2_end = models.DateField(verbose_name="PERIOD 2 End", null=True, blank=True)
    work_2 = models.TextField(verbose_name="WORK 2", blank=True, null=True)

    period_3_start = models.DateField(verbose_name="PERIOD 3 Start", null=True, blank=True)
    period_3_end = models.DateField(verbose_name="PERIOD 3 End", null=True, blank=True)
    work_3 = models.TextField(verbose_name="WORK 3", blank=True, null=True)

    period_4_start = models.DateField(verbose_name="PERIOD 4 Start", null=True, blank=True)
    period_4_end = models.DateField(verbose_name="PERIOD 4 End", null=True, blank=True)
    work_4 = models.TextField(verbose_name="WORK 4", blank=True, null=True)

    period_5_start = models.DateField(verbose_name="PERIOD 5 Start", null=True, blank=True)
    period_5_end = models.DateField(verbose_name="PERIOD 5 End", null=True, blank=True)
    work_5 = models.TextField(verbose_name="WORK 5", blank=True, null=True)

    def __str__(self):
        return f"Work Experience: {self.period_1_start} - {self.period_5_end if self.period_5_end else 'Present'}"


# SeminarTraining model, relates to BasicInfo
class SeminarTraining(models.Model):
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, related_name="seminar_training")
    period_1_start = models.DateField(verbose_name="PERIOD 1 Start", null=True, blank=True)
    period_1_end = models.DateField(verbose_name="PERIOD 1 End", null=True, blank=True)
    seminar_1 = models.TextField(verbose_name="Seminar 1 Topics", blank=True, null=True)

    period_2_start = models.DateField(verbose_name="PERIOD 2 Start", null=True, blank=True)
    period_2_end = models.DateField(verbose_name="PERIOD 2 End", null=True, blank=True)
    seminar_2 = models.TextField(verbose_name="Seminar 2 Topics", blank=True, null=True)

    period_3_start = models.DateField(verbose_name="PERIOD 3 Start", null=True, blank=True)
    period_3_end = models.DateField(verbose_name="PERIOD 3 End", null=True, blank=True)
    seminar_3 = models.TextField(verbose_name="Seminar 3 Topics", blank=True, null=True)

    period_4_start = models.DateField(verbose_name="PERIOD 4 Start", null=True, blank=True)
    period_4_end = models.DateField(verbose_name="PERIOD 4 End", null=True, blank=True)
    seminar_4 = models.TextField(verbose_name="Seminar 4 Topics", blank=True, null=True)

    period_5_start = models.DateField(verbose_name="PERIOD 5 Start", null=True, blank=True)
    period_5_end = models.DateField(verbose_name="PERIOD 5 End", null=True, blank=True)
    seminar_5 = models.TextField(verbose_name="Seminar 5 Topics", blank=True, null=True)

    def __str__(self):
        return f"Seminar Training: {self.period_1_start} - {self.period_5_end if self.period_5_end else 'Present'}"


class OtherKnowledge(models.Model):
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, related_name="other_knowledge", null=True)
    skill_name = models.CharField(max_length=255, verbose_name="Skill Name")
    skill_2_name = models.CharField(max_length=255, verbose_name="Skill 2 Name")
    skill_3_name = models.CharField(max_length=255, verbose_name="Skill 3  Name")  # Represents a specific skill or knowledge
    # Represents a specific skill or knowledge
    # Represents a specific skill or knowledge
    # If needed, add other fields specific to the skill

    def __str__(self):
        return f"Other Knowledge: {self.skill_name}"

# OtherLanguages model, relates to BasicInfo

# OtherLanguages model, relates to BasicInfo
class OtherLanguages(models.Model):
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, related_name="other_languages")  # ForeignKey to BasicInfo
    language_name = models.CharField(max_length=255, verbose_name="Language Name")
    comment = models.CharField(max_length=255, verbose_name="Comment", blank=True, null=True)

    def __str__(self):
        return f"{self.language_name} - {self.comment or 'No comment'}"

from datetime import date


class AttendanceReport(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attendance_reports')
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"Attendance Report for {self.group.name} on {self.date}"

from django.utils import timezone


class DailyAttendance(models.Model):
    attendance_report = models.ForeignKey(
        'AttendanceReport',
        on_delete=models.CASCADE,
        related_name="daily_attendances",
        null=True,
        blank=True
    )
    basic_info = models.ForeignKey(
        'BasicInfo',
        on_delete=models.CASCADE,
        related_name="daily_attendance"
    )
    presence = models.CharField(
        max_length=3,
        choices=[('YES', 'YES'), ('NO', 'NO')],
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(blank=True, null=True)
    po_number = models.CharField(max_length=255, blank=True, null=True)
    site_id = models.CharField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(default=timezone.now, verbose_name="ΗΜΕΡΟΜΗΝΙΑ")

    def __str__(self):
        # Check if attendance_report is not None before accessing its attributes
        if self.attendance_report:
            return f"{self.basic_info.first_name} {self.basic_info.last_name} - {self.attendance_report.date}"
        else:
            return f"{self.basic_info.first_name} {self.basic_info.last_name} - No Attendance Report"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['basic_info', 'attendance_report'], name='unique_employee_attendance_report')
        ]

from django.utils import timezone


class Sr(models.Model):
    sr_code = models.IntegerField(unique=True)  # SR (e.g., 134, 138)
    building_id = models.CharField(max_length=100, blank=True, null=True)  # BUILDINGID (e.g., --)
    apartment_floor = models.CharField(max_length=100, blank=True, null=True)  # APPARTMENTFLOOR (e.g., --)
    building_task_type = models.CharField(max_length=100, blank=True, null=True)  # BUILDINGTASKTYPE (e.g., 1166016514)
    sub = models.CharField(max_length=100, blank=True, null=True)  # SUB (e.g., CANCELL)
    sub_old = models.CharField(max_length=100, blank=True, null=True)  # SUB OLD (e.g., --)
    time_created = models.DateTimeField(default=timezone.now)  # TIMECREATED
    type = models.CharField(max_length=10, blank=True, null=True)  # ΤΥΠΕ Β-Β (e.g., Β)

    # Optional: Relationship to Region if you want to link the SR to a region.
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, blank=True)  # REGION (if applicable)

    def __str__(self):
        return f"SR Code: {self.sr_code} - Building Task Type: {self.building_task_type}"


class CloseBC(models.Model):
    source_id = models.CharField(max_length=50, unique=True)  # SOURCEID
    sub = models.CharField(max_length=50)  # SUB
    date = models.DateField()  # date
    rol = models.CharField(max_length=50)  # ROL
    building_task_type = models.CharField(max_length=1)  # BUILDINGTASKTYPE
    area = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='close_bc_tasks')  # AREA

    def __str__(self):
        return f"{self.source_id} - {self.area.name}"




class Cancel(models.Model):
    sr = models.ForeignKey(Sr, on_delete=models.CASCADE)  # Link to Sr model
    date_cancelled = models.DateField()  # DATE CANCELL
    finished = models.BooleanField(default=False)  # FINISHED
    is_checked = models.BooleanField(default=False)  # CHECK

    def __str__(self):
        return f"SR: {self.sr.sr_code} - Cancelled on {self.date_cancelled}"




class ClosedSSR(models.Model):
    source_id = models.CharField(max_length=50, unique=True)  # SOURCEID
    sub = models.CharField(max_length=100)  # SUB
    date = models.DateField()  # DATE
    rollout_engineer = models.CharField(max_length=100)  # ROLLOUTER
    area = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='closed_ssrs')  # AREA

    def __str__(self):
        return f"{self.source_id} - {self.area.name}"






class WFM(models.Model):
    sr = models.ForeignKey(Sr, on_delete=models.CASCADE)  # Link to Sr model
    ak = models.CharField(max_length=10)  # ΑΚ (e.g., ΚΛΜ, ΒΖ)
    address = models.CharField(max_length=255)  # ΔΙΕΥΘΥΝΣΗ (e.g., ΕΛΕΥΘΕΡΙΟΥ ΒΕΝΙΖΕΛΟΥ 3, ΚΥΠΡΟΥ 11)
    date = models.DateField(blank=True, null=True)  # DATE (e.g., "-", stored as null if missing)
    area = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='wfms')  # AREA (e.g., THESSALONIKI)
    type = models.CharField(max_length=10)  # TYPE (e.g., Β)

    def __str__(self):
        return f"{self.sr} - {self.address} ({self.area.name})"


class Info(models.Model):
    ak = models.CharField(max_length=10)  # AK (e.g., ΝΤΡ, ΨΥΧ)
    roll = models.CharField(max_length=100, blank=True, null=True)  # ROLL (e.g., ?, NATASA)
    area = models.ManyToManyField(Region, related_name='infos')  # AREA (many regions can be selected)

    def __str__(self):
        # Join the names of the regions selected for the info entry
        return f"{self.ak} - {self.roll} - {', '.join([region.name for region in self.area.all()])}"




class InfoCodeSr(models.Model):
    code_sr = models.CharField(max_length=20)  # CODE SR (e.g., 1166016516, 1166016512)
    type = models.CharField(max_length=10, blank=True, null=True)  # TYPE (e.g., Γ)
    area = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='info_codes', blank=True, null=True)  # AREA (e.g., ΠΕΡΑΙΑ, THESSALONIKI)

    def __str__(self):
        return f"{self.code_sr} - {self.type} - {self.area.name if self.area else 'No Area'}"


class InfoOldNew(models.Model):
    old = models.CharField(max_length=100)  # OLD (e.g., ΝΕΟ unified, ΝΕΟ katselis)
    new = models.CharField(max_length=100)  # NEW (e.g., UNIFIED, EUROFIBER)

    def __str__(self):
        return f"{self.old} -> {self.new}"

class Assign(models.Model):
    sr = models.ForeignKey('Sr', on_delete=models.SET_NULL, null=True, blank=True)  # SR points to Sr model
    sub = models.CharField(max_length=10, blank=True, null=True)  # SUB (e.g., ?_)
    roll1 = models.CharField(max_length=100, blank=True, null=True)  # ROLL (e.g., STEFANOS)
    roll2 = models.CharField(max_length=100, blank=True, null=True)  # ROLL (e.g., ΩΡ, ΡΟΣ)
    area = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)  # REGION as a ForeignKey to Region model
    check_sr_exist = models.CharField(max_length=100, blank=True, null=True)  # CHECK SR EXIST (e.g., ?_)
    cancel = models.CharField(max_length=100, blank=True, null=True)  # CANCEL (e.g., #N/A)
    ssr = models.CharField(max_length=100, blank=True, null=True)  # SSR (e.g., #N/A)
    closed = models.CharField(max_length=100, blank=True, null=True)  # CLOSED (e.g., #N/A)
    wfm = models.ForeignKey('WFM', on_delete=models.SET_NULL, null=True, blank=True)  # WFM points to WFM model

    def __str__(self):
        return f"SR: {self.sr} - ROLL1: {self.roll1} - AREA: {self.area}"




from django.db.models import Sum

class Customer(models.Model):
    """Represents a customer with assigned and completed work."""
    name = models.CharField(max_length=255, unique=True)

    # Assigned work (READ-ONLY)
    total_meters_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_freatio_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_cabins_assigned = models.PositiveIntegerField(default=0, editable=False)
    total_catheta_assigned = models.PositiveIntegerField(default=0, editable=False)

    # Completed work (READ-ONLY)
    total_meters_done = models.PositiveIntegerField(default=0, editable=False)
    total_freatio_done = models.PositiveIntegerField(default=0, editable=False)
    total_cabins_done = models.PositiveIntegerField(default=0, editable=False)
    total_catheta_done = models.PositiveIntegerField(default=0, editable=False)

    def update_totals(self):
        """Updates the assigned and completed work based on assigned jobs and daily programs."""
        totals = self.assignments.aggregate(
            total_meters_assigned=Sum('meters'),
            total_freatio_assigned=Sum('freatio'),
            total_cabins_assigned=Sum('cabins'),
            total_catheta_assigned=Sum('katheta'),
            total_meters_done=Sum('meters_done'),
            total_freatio_done=Sum('freatio_done'),
            total_cabins_done=Sum('cabins_done'),
            total_catheta_done=Sum('katheta_done'),
        )

        self.total_meters_assigned = totals['total_meters_assigned'] or 0
        self.total_freatio_assigned = totals['total_freatio_assigned'] or 0
        self.total_cabins_assigned = totals['total_cabins_assigned'] or 0
        self.total_catheta_assigned = totals['total_catheta_assigned'] or 0

        self.total_meters_done = totals['total_meters_done'] or 0
        self.total_freatio_done = totals['total_freatio_done'] or 0
        self.total_cabins_done = totals['total_cabins_done'] or 0
        self.total_catheta_done = totals['total_catheta_done'] or 0

        self.save()

    def __str__(self):
        return self.name


class AssignJob(models.Model):
    """Represents an assignment given to a customer within a region and group."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="assignments")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="assignments")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="assignments")

    # Assigned work
    meters = models.PositiveIntegerField(default=0)
    freatio = models.PositiveIntegerField(default=0)
    cabins = models.PositiveIntegerField(default=0)
    katheta = models.PositiveIntegerField(default=0)

    # Work done
    meters_done = models.PositiveIntegerField(default=0)
    freatio_done = models.PositiveIntegerField(default=0)
    cabins_done = models.PositiveIntegerField(default=0)
    katheta_done = models.PositiveIntegerField(default=0)

    assigned_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Override save to update totals in Customer, Group, and Region."""
        super().save(*args, **kwargs)
        self.customer.update_totals()  # Updates Customer totals
        self.group.update_totals()  # Updates Group totals
        self.region.update_totals()  # Updates Region totals

    def __str__(self):
        return f"Assignment for {self.customer.name} - {self.group.name} ({self.region.name})"

class DailyProgram(models.Model):
    """Represents a daily program with assigned tasks and progress tracking."""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="daily_programs")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="daily_programs")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="daily_programs")  # NEW FIELD
    program_pdf_file = models.FileField(upload_to="daily_programs/", blank=True, null=True)

    # Assigned work
    total_meters_assigned = models.PositiveIntegerField(default=0)
    total_freatio_assigned = models.PositiveIntegerField(default=0)
    total_cabins_assigned = models.PositiveIntegerField(default=0)
    total_catheta_assigned = models.PositiveIntegerField(default=0)

    # Completed work
    total_meters_done = models.PositiveIntegerField(default=0)
    total_freatio_done = models.PositiveIntegerField(default=0)
    total_cabins_done = models.PositiveIntegerField(default=0)
    total_catheta_done = models.PositiveIntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)

    def update_assignments(self):
        """Update the assigned job's completed work fields for the specific customer."""
        assignments = AssignJob.objects.filter(region=self.region, group=self.group, customer=self.customer)

        for assign in assignments:
            assign.meters_done = self.total_meters_done
            assign.freatio_done = self.total_freatio_done
            assign.cabins_done = self.total_cabins_done
            assign.katheta_done = self.total_catheta_done
            assign.save()

        # Update the customer's total completed work
        self.customer.update_totals()  # Now calling update_totals() instead of update_total_done

    def save(self, *args, **kwargs):
        """Override save to update AssignJob records when a DailyProgram is saved."""
        super().save(*args, **kwargs)
        self.update_assignments()  # Call update method after saving

    def __str__(self):
        return f"Daily Program - {self.customer.name} - {self.group.name} ({self.region.name}) - {self.date_created.strftime('%Y-%m-%d')}"
