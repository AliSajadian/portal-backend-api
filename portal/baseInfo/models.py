from django.db import models
from datetime import datetime

from django.contrib.auth.models import User, Group


# class GroupEx(Group):
#     parent = models.ForeignKey(Group, related_name='children', on_delete=models.CASCADE, null=True, blank=True)
#     objects = models.Manager()  

#     class Meta:
#         db_table = "auth_GroupEx"    
    
    
class Company(models.Model):
    name = models.CharField(max_length=100)
    # owner = models.ForeignKey(User, related_name="departments",
    # on_delete=models.CASCADE, null=True)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_base_company"


class Project(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, 
    related_name="Company_Project",on_delete=models.PROTECT, null=True)    
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_base_project"


class Department(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, 
    related_name="Company_Department", on_delete=models.PROTECT, null=True)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_base_department"


class JobPosition(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_base_jobPosition"


class Employee(models.Model):
    personel_code = models.CharField(max_length=10, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    gender = models.BooleanField(default=False)
    picture = models.FileField(upload_to='employee_pix', null=True)
    # photo = models.BinaryField(default=b'', editable=False, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=256, blank=True)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    department = models.ForeignKey(Department, 
        related_name="Department_Employee", on_delete=models.PROTECT, null=True)
    project = models.ForeignKey(Project, 
        related_name="Project_Employee", on_delete=models.PROTECT, null=True)
    jobPosition = models.ForeignKey(JobPosition, 
        related_name="JobPosition_Employee", on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True, null=True)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_base_employee" 


class SurveyType(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_surveyType"


class DoctorType(models.Model):
    name = models.CharField(max_length=100)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_doctorType"        

class Notification(models.Model):
    notifier_user = models.ForeignKey(User,
        related_name="User_Notification", on_delete=models.CASCADE, null=True)
    notifier_group = models.ForeignKey(Group,
        related_name="Group_Notification", on_delete=models.CASCADE, null=True)
    type = models.PositiveSmallIntegerField(null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    created_date = models.DateField(default=datetime.now, blank=True)
    expired_date = models.DateField(default=datetime.now, blank=True)
    read_status = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = "tbl_base_notification"     