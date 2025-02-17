# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EgnatiaAppBasicinfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_phone = models.CharField(max_length=15, blank=True, null=True)
    landline_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    tax_id = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    degree_available = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    iban = models.CharField(max_length=34, blank=True, null=True)
    hiring_date = models.DateField(blank=True, null=True)
    employee_status = models.CharField(max_length=50, blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    medical_exams = models.CharField(max_length=50, blank=True, null=True)
    medical_exams_date = models.DateField(blank=True, null=True)
    medical_exams_renewal_date = models.DateField(blank=True, null=True)
    safety_passport = models.CharField(max_length=50, blank=True, null=True)
    safety_passport_date = models.DateField(blank=True, null=True)
    safety_passport_renewal_date = models.DateField(blank=True, null=True)
    certifications_seminars = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egnatia_app_basicinfo'


class EgnatiaAppDailyattendance(models.Model):
    date = models.DateField()
    presence = models.CharField(max_length=3)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    po_number = models.CharField(max_length=255, blank=True, null=True)
    site_id = models.CharField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    basic_info = models.ForeignKey(EgnatiaAppBasicinfo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'egnatia_app_dailyattendance'
        unique_together = (('basic_info', 'date'),)


class EgnatiaAppOtherknowledge(models.Model):
    skill_name = models.CharField(max_length=255)
    basic_info = models.ForeignKey(EgnatiaAppBasicinfo, models.DO_NOTHING, blank=True, null=True)
    skill_2_name = models.CharField(max_length=255)
    skill_3_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'egnatia_app_otherknowledge'


class EgnatiaAppOtherlanguages(models.Model):
    language_name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True, null=True)
    basic_info = models.ForeignKey(EgnatiaAppBasicinfo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'egnatia_app_otherlanguages'


class EgnatiaAppSeminartraining(models.Model):
    basic_info = models.ForeignKey(EgnatiaAppBasicinfo, models.DO_NOTHING)
    period_1_end = models.DateField(blank=True, null=True)
    period_1_start = models.DateField(blank=True, null=True)
    period_2_end = models.DateField(blank=True, null=True)
    period_2_start = models.DateField(blank=True, null=True)
    period_3_end = models.DateField(blank=True, null=True)
    period_3_start = models.DateField(blank=True, null=True)
    period_4_end = models.DateField(blank=True, null=True)
    period_4_start = models.DateField(blank=True, null=True)
    period_5_end = models.DateField(blank=True, null=True)
    period_5_start = models.DateField(blank=True, null=True)
    seminar_1 = models.TextField(blank=True, null=True)
    seminar_2 = models.TextField(blank=True, null=True)
    seminar_3 = models.TextField(blank=True, null=True)
    seminar_4 = models.TextField(blank=True, null=True)
    seminar_5 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egnatia_app_seminartraining'


class EgnatiaAppStudies(models.Model):
    period_1 = models.CharField(max_length=50)
    study_1 = models.TextField(blank=True, null=True)
    period_2 = models.CharField(max_length=50)
    study_2 = models.TextField(blank=True, null=True)
    period_3 = models.CharField(max_length=50)
    study_3 = models.TextField(blank=True, null=True)
    basic_info = models.ForeignKey(EgnatiaAppBasicinfo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'egnatia_app_studies'


class EgnatiaAppWorkexperience(models.Model):
    period_1_start = models.DateField(blank=True, null=True)
    period_1_end = models.DateField(blank=True, null=True)
    work_1 = models.TextField(blank=True, null=True)
    period_2_start = models.DateField(blank=True, null=True)
    period_2_end = models.DateField(blank=True, null=True)
    work_2 = models.TextField(blank=True, null=True)
    period_3_start = models.DateField(blank=True, null=True)
    period_3_end = models.DateField(blank=True, null=True)
    work_3 = models.TextField(blank=True, null=True)
    period_4_start = models.DateField(blank=True, null=True)
    period_4_end = models.DateField(blank=True, null=True)
    work_4 = models.TextField(blank=True, null=True)
    period_5_start = models.DateField(blank=True, null=True)
    period_5_end = models.DateField(blank=True, null=True)
    work_5 = models.TextField(blank=True, null=True)
    basic_info = models.ForeignKey(EgnatiaAppBasicinfo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'egnatia_app_workexperience'
