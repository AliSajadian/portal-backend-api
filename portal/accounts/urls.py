from django.urls import path, include
from knox import views as knox_views

from .views import PasswordAPIView, RegisterAPI, LoginAPI, LoginExAPI, UserAPI, UserCreateAPI, UserDeleteAPI, \
    EmployeeImageDownloadListAPIView, UserGroupsAPI, GroupPermissionsAPI, UserPermissionsAPI, FileDownloadListAPIView
       

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/resturauntservelogin', LoginExAPI.as_view()),
    ### path('api/auth/loginEx', LoginAPIEx.as_view()),
    path("api/auth/change_password/", PasswordAPIView.as_view(), name="change_password"),
    
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path("api/auth/filesdownload/<int:id>/", FileDownloadListAPIView.as_view(), name="filesdownload/<id>/"),
    path("api/auth/employeeimagedownload/<int:id>/", EmployeeImageDownloadListAPIView.as_view(), name="employeeimagedownload/<id>/"),

    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/userex', UserCreateAPI.as_view()),
    path('api/auth/userex/<int:pk>', UserDeleteAPI.as_view(), name="userex/<pk>/"),
    path('api/auth/usergroups/<int:pk>', UserGroupsAPI.as_view(), name="usergroups/<pk>/"),
    path('api/auth/grouppermissions/<int:pk>', GroupPermissionsAPI.as_view(), name="grouppermissions/<pk>/"),
    path('api/auth/userpermissions/<int:pk>', UserPermissionsAPI.as_view(), name="userpermissions/<pk>/"),
]

# urlpatterns.extend(router)  , name="guestmealdays/(?P<selectedDate>[\w\-]+)/$"