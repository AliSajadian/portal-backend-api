from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from knox.models import AuthToken
import re

from django.contrib.auth.models import User, Group
from .serializers import PasswordSerializer, LoginSerializer, UserSerializer, UserGroupSerializer, GroupPermissionSerializer, \
    UserPermissionSerializer, RegisterSerializer, UserExSerializer
from baseInfo.models import Employee
# from doctor_appointments.models import DocPatientsFiles, Doctors
from .services import get_LDAP_user


class PasswordAPIView(APIView):
    def get_object(self, userid):
        user = get_object_or_404(User, id=userid)
        return user

    def put(self, request):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            userid = serializer.data['userid']
            username = serializer.data['username']
            user = self.get_object(userid)
            oldpassword = serializer.data['currentpassword']
            is_same_as_old = user.check_password(oldpassword)
            if (not is_same_as_old):
                """
                old password and new user passwords should be the same
                """
                return Response({"password": ["You enter wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)            
            new_password = serializer.data['newpassword']
            is_same_as_old = user.check_password(new_password)
            if is_same_as_old:
                """
                old password and new passwords should not be the same
                """
                return Response({"password": ["It should be different from your last password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            if user.username != username:
                user.username = username
            user.set_password(new_password)
            user.save()
            return Response({'success':True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
# User 
class UserCreateAPI(generics.GenericAPIView):
    permission_classes = [
    permissions.IsAuthenticated
    ] 

    def post(self,request):
        try:
            user = User.objects.create(
                            password = 'pbkdf2_sha256$180000$Nsew4fOfrQ0C$4moGTA3Uz40WflCIqb7efNP/9/rlTzBd3wf1msgAIQI=',
                            username = request.data["username"],
                            first_name = request.data["first_name"],
                            last_name = request.data["last_name"],
                            email = '',
                            is_active = request.data["is_active"],
                            )
            user.save()
            user.set_password(request.data["password"])

            employee = Employee.objects.create(
                            first_name = request.data["first_name"],
                            last_name = request.data["last_name"],
                            phone = None,
                            personel_code = request.data["personel_code"],
                            email = '',
                            department = None,
                            jobPosition = None, 
                            project = None, 
                            user = user,
                            is_active = request.data["is_active"],
                            gender = 1,
                            )       
            employee.save()

            return Response(UserExSerializer(user, context=self.get_serializer_context()).data)             
        except Exception as e:
            return Response(
                {
                    # "Failure": e
                    'user and employee creating failed!' 
                },
                status=status.HTTP_400_BAD_REQUEST
            )                                              


class UserDeleteAPI(generics.GenericAPIView):
    permission_classes = [
    permissions.IsAuthenticated
    ] 

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk = pk)
            employee = Employee.objects.get(user_id=user.id)       

            employee.delete()
            user.delete()

            return Response(
                {
                    "user and employee deleted successfully" 
                },
            )         
        except Exception as e:
            return Response(
                {
                    "Failure": str(e) 
                },
                status=status.HTTP_400_BAD_REQUEST
            ) 


# User Group
class UserGroupsAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ] 

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserGroupSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {
                    "Failure": 'user not found!' 
                },
                status=status.HTTP_400_BAD_REQUEST
            ) 

    def put(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserGroupSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Group Permission
class GroupPermissionsAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ] 

    def get(self, request, pk, format=None):
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupPermissionSerializer(group)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {
                    "Failure": 'group not fount!' 
                },
                status=status.HTTP_400_BAD_REQUEST
            ) 

    def put(self, request, pk, format=None):
        group = Group.objects.get(pk=pk)
        serializer = GroupPermissionSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Permission
class UserPermissionsAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ] 

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserPermissionSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {
                    "Failure": 'user not fount!' 
                },
                status=status.HTTP_400_BAD_REQUEST
            ) 

    def put(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserPermissionSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    _, token = AuthToken.objects.create(user)
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })

#/////////////////////////////////////////////////////////////////////////////////////////////

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data["username"]
        password = data["password"]

        if(not 'a' in username):
            try:
                username_ad =  get_LDAP_user(username, password)
                user = User.objects.filter(username=username_ad)[0] if(len(User.objects.filter(username=username_ad))>0) else ''
                _, token = AuthToken.objects.create(user)

                employee_id = Employee.objects.filter(user = user.id).values('id')[0]['id'] if (Employee.objects != None and Employee.objects.filter(user = user.id).count() > 0) else 0
            except Exception as e:
                return Response({'error': 1})

        # ---------------------------------------------------------------
            emp = Employee.objects.get(user = user.id)
            if(emp == None or not re.search(re.compile('^[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ ي ی]+$'), emp.first_name) or 
                not re.search(re.compile('^[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ ي ی]+$'), emp.last_name) or 
                emp.personel_code == None or (emp.department == None and emp.project == None) or emp.jobPosition == None):
                # raise Exception("اطلاعات پرسنلی ناقص میباشد، لطفا با راهبر سامانه تماس بگیرید.")
                return Response({'error': 2})
        # ---------------------------------------------------------------
            usergrouppermissions = []
            usergroups = []
            for group in user.groups.all():
                if(group not in usergroups):
                        usergroups.append(group.id)
                for permission in group.permissions.all():
                    if(permission not in usergrouppermissions):
                        usergrouppermissions.append(permission.codename)
            
            for permission in user.user_permissions.all():
                if(permission not in usergrouppermissions):
                    usergrouppermissions.append(permission.codename)

            if((1 not in usergroups) and (2 not in usergroups) and (usergroups == None or usergroups == [] or usergrouppermissions == None or usergrouppermissions == [])):
                # "دسترسی به سیستم به شما اختصاص داده نشده است، لطفا با راهبر سامانه تماس بگیرید."
                return Response({'error': 3})
        # ---------------------------------------------------------------
            return Response({
                "error": 0,
                "user": UserSerializer(user, context=self.get_serializer_context()).data, 
                "token": token,
                "employee": Employee.objects.filter(user = user.id).values('id', 'first_name', 'last_name', 'picture') if Employee.objects != None else None,
                # "isDoctor": Doctors.objects.filter(employee_id=employee_id).count() > 0,
                "permissions": usergrouppermissions,
                "groups": usergroups,
            })         
        else:
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data
                _, token = AuthToken.objects.create(user)
            except Exception as e:
                return Response({'error': 1})
            # _user = UserSerializer(user, context=self.get_serializer_context()).data

            employee_id = Employee.objects.filter(user = user.id).values('id')[0]['id'] if (Employee.objects != None and Employee.objects.filter(user = user.id).count() > 0) else 0
            if(employee_id == 0):
                emp = Employee.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email, user_id=user.id, gender=False) 
                employee_id = emp.id
        # ---------------------------------------------------------------
            # emp = Employee.objects.get(user = user.id)
            # if(emp == None or not re.search(re.compile('^[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ ي ی ]+$'), emp.first_name) or 
            #     not re.search(re.compile('^[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ ي ی ]+$'), emp.last_name) or 
            #     emp.personel_code == None or (emp.department == None and emp.project == None) or emp.jobPosition == None):
            #     # raise Exception("اطلاعات پرسنلی ناقص میباشد، لطفا با راهبر سامانه تماس بگیرید.")
            #     return Response({'error': 2})
        # ---------------------------------------------------------------
            usergrouppermissions = []
            usergroups = []
            # for group in user.groups.all():
            #     if(group not in usergroups):
            #             usergroups.append(group.id)
            #     for permission in group.permissions.all():
            #         if(permission not in usergrouppermissions):
            #             usergrouppermissions.append(permission.codename)
            
            # for permission in user.user_permissions.all():
            #     if(permission not in usergrouppermissions):
            #         usergrouppermissions.append(permission.codename)

            # if((1 not in usergroups) and (2 not in usergroups) and (usergroups == None or usergroups == [] or usergrouppermissions == None or usergrouppermissions == [])):
            #     # "دسترسی به سیستم به شما اختصاص داده نشده است، لطفا با راهبر سامانه تماس بگیرید."
            #     return Response({'error': 3})
        # ---------------------------------------------------------------
            return Response({
                "error": 0,
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token,
                "employee": Employee.objects.filter(user = user.id).values('id', 'first_name', 'last_name', 'picture') if Employee.objects != None else None,
                # "isDoctor": Doctors.objects.filter(employee_id=employee_id).count() > 0,
                "permissions": usergrouppermissions,
                "groups": usergroups,
            })
# /////////////////////////////////////////////////////////////////////////////////////////////

class LoginExAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
      data = request.data
      username = data["username"]
      password = data["password"]

      if(not '_' in username):
        username_ad =  get_LDAP_user(username, password)
        user = User.objects.filter(username=username_ad)[0] if(len(User.objects.filter(username=username_ad))>0) else ''
        _, token = AuthToken.objects.create(user)
# ---------------------------------------------------------------
        havePermission = False
        for group in user.groups.all():
            if(group.name == 'Resturaunt Service Admin'):
                 havePermission = True
                 break   
        
        if(not havePermission):
            return Response({
                "token": None,
            }) 
# ---------------------------------------------------------------
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
        })        
      else:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
# ---------------------------------------------------------------
        havePermission = False
        for group in user.groups.all():
            if(group.name == 'Resturaunt Service Admin'):
                 havePermission = True
                 break   
        
        if(not havePermission):
            return Response({
                "token": None,
            }) 
# ---------------------------------------------------------------
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token,
        })

# /////////////////////////////////////////////////////////////////////////////////////////////

# Login API
# class LoginAPI_(generics.GenericAPIView):
#   serializer_class = LoginSerializer

#   def post(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data
#     _, token = AuthToken.objects.create(user)
#     # _user = UserSerializer(user, context=self.get_serializer_context()).data
#     employee_id = Employee.objects.filter(user = user.id).values('id')[0]['id'] if (Employee.objects != None and Employee.objects.filter(user = user.id).count() > 0) else 0
#     return Response({
#       "user": UserSerializer(user, context=self.get_serializer_context()).data,
#       "token": token,
#       "employee": Employee.objects.filter(user = user.id).values('id', 'picture') if Employee.objects != None else None,
#       "isDoctor": Doctors.objects.filter(employee_id=employee_id).count() > 0
#     })

# Get User API
class UserAPI(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user

class FileDownloadListAPIView(generics.ListAPIView):
    permission_classes = [
        permissions.AllowAny]

    def get(self, request, id, format=None):
        queryset = DocPatientsFiles.objects.get(id=id)
        file_handle = 'files//' +  str(queryset.file)
        # 
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type = 'application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % str(queryset.file).find('/')
        return response       

class EmployeeImageDownloadListAPIView(generics.ListAPIView):
    permission_classes = [
        permissions.AllowAny]

    def get(self, request, id, format=None):
        queryset = Employee.objects.get(id=id)
        file_handle = 'files//' +  str(queryset.picture)
        # 
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type = 'image/*')
        response['Content-Disposition'] = 'attachment; filename="%s"' % str(queryset.picture).find('/')
        return response 


       