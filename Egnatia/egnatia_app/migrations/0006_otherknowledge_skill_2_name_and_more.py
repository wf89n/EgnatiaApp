# Generated by Django 4.2.18 on 2025-01-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egnatia_app', '0005_remove_seminartraining_period_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherknowledge',
            name='skill_2_name',
            field=models.CharField(default=0, max_length=255, verbose_name='Skill 2 Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='otherknowledge',
            name='skill_3_name',
            field=models.CharField(default=0, max_length=255, verbose_name='Skill 3  Name'),
            preserve_default=False,
        ),
    ]
