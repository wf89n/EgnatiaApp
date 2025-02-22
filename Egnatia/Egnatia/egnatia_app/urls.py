# egnatia_app/urls.py or your main urls.py (depending on your setup)
from django.urls import path,re_path
from . import views
from .views import (
    people_by_group,
    attendance_reports_by_group,
    submit_attendance
)
from django.views.generic import TemplateView
import os
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Other URLs...
    path('admin/filter/groups/', views.filter_groups, name='filter_groups'),
    path('admin/filter/departments/', views.filter_departments, name='filter_departments'),
    path('admin/filter/roles/', views.filter_roles, name='filter_roles'),
    path('regions/', views.region_list),
    path('departments/', views.department_list, name='department-list'),
    path('group-departments/', views.group_department_list, name='group-department-list'),
    path('roles/', views.role_list, name='role-list'),
    path('employees/', views.employee_list, name='employee-list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee-detail'),
    path('groups/', views.group_list, name='group-list'),
    path('groups/<int:pk>/', views.group_detail, name='group-detail'),
    path('customers/', views.customer_list, name='customer-list'),
    path('people/<int:group_id>/', people_by_group, name='people-by-group'),
    path('attendance-reports/<int:group_id>/', attendance_reports_by_group, name='attendance-reports-by-group'),
    path('submit-attendance/', submit_attendance, name='submit-attendance'),
    path('add-basic-info/', views.create_basic_info, name='create-basic-info'),
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html"), name="home"),
]



from django.conf import settings
from django.conf.urls.static import static
import os


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)