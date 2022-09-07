# Generated by Django 4.1 on 2022-08-23 07:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tbl_base_company',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Company_Department', to='baseInfo.company')),
            ],
            options={
                'db_table': 'tbl_base_department',
            },
        ),
        migrations.CreateModel(
            name='DoctorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tbl_doctorType',
            },
        ),
        migrations.CreateModel(
            name='JobPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tbl_base_jobPosition',
            },
        ),
        migrations.CreateModel(
            name='SurveyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tbl_surveyType',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Company_Project', to='baseInfo.company')),
            ],
            options={
                'db_table': 'tbl_base_project',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(null=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('created_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('expired_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('read_status', models.BooleanField(default=False, null=True)),
                ('notifier_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Group_Notification', to='auth.group')),
                ('notifier_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_Notification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_base_notification',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personel_code', models.CharField(max_length=10, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('gender', models.BooleanField(default=False)),
                ('picture', models.FileField(null=True, upload_to='employee_pix')),
                ('phone', models.CharField(max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=256)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Department_Employee', to='baseInfo.department')),
                ('jobPosition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='JobPosition_Employee', to='baseInfo.jobposition')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Project_Employee', to='baseInfo.project')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_base_employee',
            },
        ),
    ]
