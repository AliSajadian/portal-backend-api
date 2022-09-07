from rest_framework import routers
from .views import CompanyViewSet, DepartmentViewSet, ProjectViewSet, JobPositionViewSet, EmployeeViewSet, EmployeeCodeViewSet, \
    DoctorEmployeeViewSet, SurveyTypeViewSet, DoctorTypeViewSet, UsersViewSet, GroupViewSet, UserGroupsViewSet, PermissionViewSet, \
        ContentTypeViewSet, UserPermissionsViewSet, GroupPermissionsViewSet, NotificationViewSet, FilteredNotificationViewSet, \
            BaseInfo_Get_DepartmentsExViewAPI, EmployeeExViewSet
from django.urls import path


router = routers.DefaultRouter()
router.register('api/companies', CompanyViewSet, 'companies')
router.register('api/departments', DepartmentViewSet, 'departments')
router.register('api/projects', ProjectViewSet, 'projects')
router.register('api/jobPositions', JobPositionViewSet, 'jobPositions')
router.register('api/employees', EmployeeViewSet, 'employees')
router.register('api/employeesex', EmployeeExViewSet, 'employeesex')
router.register('api/employeecodes', EmployeeCodeViewSet, 'employeecodes')
router.register('api/doctoremployees', DoctorEmployeeViewSet, 'doctoremployees')
router.register('api/surveyTypes', SurveyTypeViewSet, 'surveyTypes')
router.register('api/doctorTypes', DoctorTypeViewSet, 'doctorTypes')

router.register('api/users', UsersViewSet, 'users')
router.register('api/groups', GroupViewSet, 'groups')
router.register('api/usergroups', UserGroupsViewSet, 'usergroups')
router.register('api/permissions', PermissionViewSet, 'permissions')
router.register('api/contenttypes', ContentTypeViewSet, 'contenttypes')
router.register('api/userpermissions', UserPermissionsViewSet, 'userpermissions')
router.register('api/grouppermissions', GroupPermissionsViewSet, 'usergrouppermissions')

router.register('api/notifications', NotificationViewSet, 'notifications')
router.register('api/filterednotifications/(?P<id>\d+)', FilteredNotificationViewSet, 'filterednotifications')
urlpatterns = [
    path('api/departmentsex/', BaseInfo_Get_DepartmentsExViewAPI.as_view(), name='api/sectionnamesex'),
]
urlpatterns += router.urls