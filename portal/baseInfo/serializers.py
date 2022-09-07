from rest_framework import serializers

from django.contrib.auth.models import User, Group, Permission, ContentType
from baseInfo.models import Company, Department, Project, JobPosition, Employee, SurveyType, DoctorType, Notification



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
                
class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeExSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', default='')
    department_name = serializers.CharField(source='department.name', default='')
    project_name = serializers.CharField(source='project.name', default='')    
    jobPosition_name = serializers.CharField(source='jobPosition.name', default='')    
    
    class Meta:
        model = Employee
        fields = ('id', 'personel_code', 'username', 'first_name', 'last_name', 'gender', 'picture', 
                'phone', 'email', 'is_active', 'department_name', 'project_name', 'jobPosition_name')    

class EmployeeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'personel_code')

# Users Serializer EmployeeCodeSerializer
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active')

class SurveyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyType
        fields = '__all__'        

class DoctorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorType
        fields = '__all__'      

class GroupSerializer(serializers.ModelSerializer):
    # id = serializers.ModelField(model_field=Group()._meta.get_field('id'))
    class Meta:
        model = Group
        fields = ('id', 'name') 

class UserGroupsSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    # serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'groups')       

class PermissionSerializer(serializers.ModelSerializer):
    # id = serializers.ModelField(model_field=Group()._meta.get_field('id'))
    class Meta:
        model = Permission
        fields = '__all__'      

class ContentTypeSerializer(serializers.ModelSerializer):
    # id = serializers.ModelField(model_field=Group()._meta.get_field('id'))
    class Meta:
        model = ContentType
        fields = '__all__'      

class PermissionExSerializer(serializers.ModelSerializer):
    # id = serializers.ModelField(model_field=Group()._meta.get_field('id'))
    class Meta:
        model = Permission
        fields = ('id', 'name') 

class UserPermissionsSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'user_permissions')    

class GroupPermissionsSerializer(serializers.ModelSerializer):
    permissions = PermissionExSerializer(many=True)
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')    

class NotificationSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format="%Y-%m-%d")
    expired_date = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Notification
        fields = '__all__'        
        
# class UserSerializer_(serializers.ModelSerializer):
#     groups = GroupSerializer(many=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'groups']
        
#     def update(self, instance, validated_data):
#         try:
#             data = validated_data.copy()
#             # print('data: ', data)
#             groups = data.pop('groups', [])
#             for key, val in data.items():
#                 setattr(instance, key, val)
#             instance.save()
#             group_ids = [g['id'] for g in groups]
#             instance.groups.clear()
#             instance.groups.add(*group_ids)
#             # print('group_ids: ', group_ids)
#             # for group in groups:
#             #     instance.groups.add(group)
#             return instance
#         except Exception as e:
#             return e

#     def create(self, validated_data):
#         try:
#             data = validated_data.copy()
#             groups = data.pop('groups', [])
#             instance = self.Meta.model.objects.create(**data)
#             for group in groups:
#                 instance.groups.add(group)
#             return instance
#         except Exception as e:
#             return e
