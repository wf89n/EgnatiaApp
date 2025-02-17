# Generated by Django 4.2.18 on 2025-01-25 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('egnatia_app', '0009_department_region_role_group_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='egnatia_app.role', verbose_name='Role'),
        ),
    ]
