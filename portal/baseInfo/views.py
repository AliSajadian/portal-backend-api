from rest_framework import generics, viewsets, permissions
from datetime import datetime, date
from django.db.models import Q, F
from rest_framework.response import Response 

# from django.db.models import Count, Q, F, Window, Value, IntegerField

from django.contrib.auth.models import User, Group, Permission, ContentType
from baseInfo.models import Company, Department, Project, JobPosition, Employee, SurveyType, DoctorType, Notification
from .serializers import CompanySerializer, DepartmentSerializer, ProjectSerializer, JobPositionSerializer, EmployeeSerializer, \
    EmployeeCodeSerializer, UsersSerializer, SurveyTypeSerializer, DoctorTypeSerializer, GroupSerializer, UserGroupsSerializer, \
        PermissionSerializer, UserPermissionsSerializer, GroupPermissionsSerializer, ContentTypeSerializer, NotificationSerializer, \
            EmployeeExSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = CompanySerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = DepartmentSerializer

class BaseInfo_Get_DepartmentsExViewAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ] 

    def get(self, request, *args, **kwargs):
        return Response(Department.objects.all().annotate(
            company_name=F('company__name')
        ).values('id', 'name', 'company', 'company_name'))

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = ProjectSerializer

class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = JobPositionSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 
    serializer_class = EmployeeSerializer

class EmployeeExViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 
    serializer_class = EmployeeExSerializer   

class EmployeeCodeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 
    serializer_class = EmployeeCodeSerializer
    # def perform_update(self, serializer):
    #     employee = Employee.objects.get(pk=self.kwargs['pk'])
    #     employee.picture.delete()
    #     EmployeeSerializer.save()

class DoctorEmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ] 
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        return Employee.objects.filter(jobPosition__name__icontains = 'پزشک')

class UsersViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()

  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = UsersSerializer 

class SurveyTypeViewSet(viewsets.ModelViewSet):
    queryset = SurveyType.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = SurveyTypeSerializer


class DoctorTypeViewSet(viewsets.ModelViewSet):
    queryset = DoctorType.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = DoctorTypeSerializer    


# Group API
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = GroupSerializer

class UserGroupsViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()

  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = UserGroupsSerializer 

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = PermissionSerializer

class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = ContentTypeSerializer    

class UserPermissionsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserPermissionsSerializer 

class GroupPermissionsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = GroupPermissionsSerializer 

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = NotificationSerializer 

class FilteredNotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ] 
    serializer_class = NotificationSerializer

    def get_queryset(self):
        userID = self.kwargs['id']
        today = date.today()
        c1 = Q(read_status__exact=False) 
        c2 = Q(expired_date__gte=today)
        c3 = Q(notifier_user__exact=userID)
        return Notification.objects.filter(c1, c2, c3)

# class UsersViewSet_(viewsets.ModelViewSet):
#     queryset = User.objects.all()

#     permission_classes = [
#         permissions.IsAuthenticated
#     ] 

#     serializer_class = UserSerializer_

#     # def put(self, request, *args, **kwargs):
#     #     return self.update(request, *args, **kwargs)

#     # def perform_update(self, serializer):
#     #     serializer.save(updated_by_user=self.request.user)
#     def put(self, request, pk, format=None):
#         post = Post.objects.get(pk=pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)