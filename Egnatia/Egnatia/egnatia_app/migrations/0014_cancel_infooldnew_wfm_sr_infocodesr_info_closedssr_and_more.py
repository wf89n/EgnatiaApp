# Generated by Django 4.2.18 on 2025-01-28 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('egnatia_app', '0013_group_total_expenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr', models.CharField(max_length=50, unique=True)),
                ('date_cancelled', models.DateField()),
                ('finished', models.BooleanField(default=False)),
                ('is_checked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='InfoOldNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old', models.CharField(max_length=100)),
                ('new', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WFM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr', models.IntegerField(unique=True)),
                ('ak', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('type', models.CharField(max_length=10)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wfms', to='egnatia_app.region')),
            ],
        ),
        migrations.CreateModel(
            name='Sr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr_code', models.IntegerField()),
                ('unknown1', models.CharField(blank=True, max_length=100, null=True)),
                ('unknown2', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='egnatia_app.region')),
            ],
        ),
        migrations.CreateModel(
            name='InfoCodeSr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_sr', models.CharField(max_length=20)),
                ('type', models.CharField(blank=True, max_length=10, null=True)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='info_codes', to='egnatia_app.region')),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ak', models.CharField(max_length=10)),
                ('roll', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.ManyToManyField(related_name='infos', to='egnatia_app.region')),
            ],
        ),
        migrations.CreateModel(
            name='ClosedSSR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(max_length=50, unique=True)),
                ('sub', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('rollout_engineer', models.CharField(max_length=100)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='closed_ssrs', to='egnatia_app.region')),
            ],
        ),
        migrations.CreateModel(
            name='CloseBC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(max_length=50, unique=True)),
                ('sub', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('rol', models.CharField(max_length=50)),
                ('building_task_type', models.CharField(max_length=1)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='close_bc_tasks', to='egnatia_app.region')),
            ],
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr', models.IntegerField()),
                ('sub', models.CharField(blank=True, max_length=10, null=True)),
                ('roll1', models.CharField(blank=True, max_length=100, null=True)),
                ('roll2', models.CharField(blank=True, max_length=100, null=True)),
                ('check_sr_exist', models.CharField(blank=True, max_length=100, null=True)),
                ('cancel', models.CharField(blank=True, max_length=100, null=True)),
                ('ssr', models.CharField(blank=True, max_length=100, null=True)),
                ('closed', models.CharField(blank=True, max_length=100, null=True)),
                ('wfm', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='egnatia_app.region')),
            ],
        ),
    ]
