from django.urls import path, re_path
from rest_framework import routers

from .views import Restaurant_MealViewSet, Restaurant_Day_MealViewSet, Restaurant_Employee_Day_MealViewSet, \
        Restaurant_ReportsApi, Restaurant_Guest_Day_MealViewSet, Restaurant_Employee_Day_MealApi, \
        Restaurant_Guest_Day_MealApi, Restaurant_Serve_MealApi, Restaurant_Day_MealApi
        
router = routers.DefaultRouter()
router.register('api/meals', Restaurant_MealViewSet, 'meals')
router.register('api/mealdays', Restaurant_Day_MealViewSet, 'mealdays')
router.register('api/personnelmealdays', Restaurant_Employee_Day_MealViewSet, 'personnelmealdays')
router.register('api/guestmealsdays', Restaurant_Guest_Day_MealViewSet, 'guestmealsdays')

urlpatterns = [
    # day_meal urls ++++++++++++++++++++++++++++++++++++++++++++++++++  
    path('api/getmealsday/<str:selectedDate>', Restaurant_Day_MealApi.get_mealsDayByDate, name='getmealsday/<selectedDate>'),
    path('api/mealdayscurrentmonth', Restaurant_Day_MealApi.get_currentMonthMealsDays, name='mealdayscurrentmonth'),
    path('api/mealdaysnextmonth', Restaurant_Day_MealApi.get_nextMonthMealsDays, name='mealdaysnextmonth'),
    re_path(r'^api/mealdaysex/(?P<date>\d{4}-\d{2}-\d{2})$', Restaurant_Day_MealApi.get_currentMonthMealsDays_SelectedNos, 
        name=r'^api/mealdaysex/(?P<date>\d{4}-\d{2}-\d{2})$'),
    re_path(r'^api/activatepersonelmealdayselection/(?P<date>\d{4}-\d{2}-\d{2})/(?P<flg>\d+)$', Restaurant_Day_MealApi.activate_mealsDays_get_currentMonthMealsDays, 
        name=r'^api/activatepersonelmealdayselection/(?P<date>\d{4}-\d{2}-\d{2})/(?P<flg>\d+)$'),
    path('api/addmealdays', Restaurant_Day_MealApi.add_mealsDays_get_nextMonthMealsDays, name='addmealdays'),
    path('api/editmealdays', Restaurant_Day_MealApi.edit_mealsDays_get_nextMonthMealsDays, name='editmealdays'),

    # employee_day_meal urls +++++++++++++++++++++++++++++++++++++++++
    path('api/personelmealdayscurrentmonth/<int:employee_id>)', Restaurant_Employee_Day_MealApi.get_currentMonthEmployeeMealsDays, name='personelmealdayscurrentmonth/<employee_id>'),
    path('api/personelmealdaysnextmonth/<int:employee_id>)', Restaurant_Employee_Day_MealApi.get_nextMonthEmployeeMealsDays, name='personelmealdaysnextmonth/<employee_id>'),
    path('api/savebulkcurrentmonthpersonelmealdays', Restaurant_Employee_Day_MealApi.save_get_currentMonthEmployeeMealsDays, name='savebulkcurrentmonthpersonelmealdays'),
    path('api/savebulknextmonthpersonelmealdays', Restaurant_Employee_Day_MealApi.save_get_nextMonthEmployeeMealsDays, name='savebulknextmonthpersonelmealdays'),

    # restaurant serve meal urls +++++++++++++++++++++++++++++++++++++++++
    path("api/fishmeal/<int:pk>/", Restaurant_Serve_MealApi.get_employeeFishMealState, name="fishmeal/<pk>/"),
    path("api/servemeal/<int:pk>/", Restaurant_Serve_MealApi.patch_serveEmployeeDayMeals, name="servemeal/<pk>/"),
    path('api/servedmeals', Restaurant_Serve_MealApi.get_dayMealsStatistics, name='servedmeals'),
    path('api/servedguestmeals', Restaurant_Serve_MealApi.Get_GuestMealsNo, name='servedguestmeals'),

    # guest_day_meal urls ++++++++++++++++++++++++++++++++++++++++++++
    path('api/getguestmealsday/<str:selectedDate>', Restaurant_Guest_Day_MealApi.get_guestMealsDayList, name='getguestmealsday/<selectedDate>'),
    path('api/getguestjunction/<str:selectedDate>', Restaurant_Guest_Day_MealApi.get_guestJunctionList, name='getguestjunction/<selectedDate>'),
    path('api/projectguestsmealsdaylist/<str:selectedDate>/<int:projectId>/', Restaurant_Guest_Day_MealApi.get_projectGuestMealsDayList, name='projectguestsmealsdaylist/<selectedDate>/<projectId>/'),
    path('api/addguestsmealsday/', Restaurant_Guest_Day_MealApi.create_guestDayMeals, name='addguestsmealsday/'),
    path('api/updateguestmealsday/', Restaurant_Guest_Day_MealApi.update_guestDayMeals, name='updateguestmealsday/'),
    path("api/guestmealdayjunction/", Restaurant_Guest_Day_MealApi.update_guestDayMealsJunction, name="guestmealdayjunction/"),
    path('api/saveguestsmealsday/', Restaurant_Guest_Day_MealApi.save_guestDayMeals, name='saveguestsmealsday/'),
    path('api/removeguestmealsday/<int:pk>/', Restaurant_Guest_Day_MealApi.remove_guestDayMeals, name='removeguestmealsday/<pk>/'),

    # report urls ++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ------------- controlMonthlyMealsStatics report ---------------
    path('api/servedguestmealsex', Restaurant_ReportsApi.get_controlMonthlyMealsStatics, name='servedguestmealsex'), #report controlMonthlyMealsStatics
    # ------------------- mealsDailyList report ---------------------
    path('api/departmentsmealsdailylist/<int:departmentId>/', Restaurant_ReportsApi.get_departmentMealsDailyList, name='departmentsmealsdailylist/<departmentId>/'),
    path('api/projectsmealsdailylist/<int:projectId>/', Restaurant_ReportsApi.get_projectMealsDailyList, name='projectsmealsdailylist/<projectId>/'),
    path('api/departmentdaymealsstatistics/<int:departmentId>/', Restaurant_ReportsApi.get_departmentDayMealsStatistics, name='departmentdaymealsstatistics/<departmentId>/'),    
    path('api/projectdaymealsstatistics/<int:projectId>/', Restaurant_ReportsApi.get_projectDayMealsStatistics, name='projectdaymealsstatistics/<projectId>/'),    
    # ---------------- sectionMealsDailyList report -----------------
    path('api/sectionsmealsdailylist/<int:employeeId>/', Restaurant_ReportsApi.get_sectionMealsDailyList, name='sectionsmealsdailylist/<employeeId>/'),
    path('api/sectionname/<int:employeeId>/', Restaurant_ReportsApi.get_sectionName, name='sectionname/<employeeId>/'),
    path('api/sectiondaymealsstatistics/<int:employeeId>/', Restaurant_ReportsApi.get_sectionDayMealsStatistics, name='sectiondaymealsstatistics/<employeeId>/'),    
    # -------------- CurrentMonthSelectedMeal report ----------------
    path('api/currentmonthselectedmeals/<int:employeeId>/', Restaurant_ReportsApi.get_currentMonthSelectedMeal, name='currentmonthselectedmeals/<employeeId>/'),    
    # --------------- asftDayMealsStatistics report -----------------
    re_path(r'api/asftdaymealsstatistics/(?P<date>\d{4}-\d{2}-\d{2})$', Restaurant_ReportsApi.get_asftDayMealsStatistics, name=r'api/asftdaymealsstatistics/(?P<date>\d{4}-\d{2}-\d{2})$'),    
    # ------------- CompaniesDayMealsStatistics report --------------
    re_path(r'^api/companysdaymealsstatistics/(?P<date>\d{4}-\d{2}-\d{2})$', Restaurant_ReportsApi.get_companiesDayMealsStatistics, name=r'^api/companysdaymealsstatistics/(?P<date>\d{4}-\d{2}-\d{2})$'),
    # ----------- ContractorMonthlyMealsStatistics & ControlMonthlyMealsStatistics reports -----------
    path('api/contractormonthlymealsstatistics/', Restaurant_ReportsApi.get_contractorMonthlyMealsStatistics, name='contractormonthlymealsstatistics/'),   
    path('api/controlmonthlymealsstatistics/', Restaurant_ReportsApi.get_controlMonthlyMealsStatistics, name='controlmonthlymealsstatistics/'),   
    path('api/mealsstatisticsdateslist/', Restaurant_ReportsApi.get_mealsStatisticsDatesList, name='mealsstatisticsdateslist/'),
    # -------- ContractorDailySectionMealsStatistics report ---------
    path('api/contractorsectionsdailymealsstatistics/', Restaurant_ReportsApi.get_contractorDailySectionMealsStatistics, name='api/contractorsectionsdailymealsstatistics/'),
    path('api/todaymealsnames/', Restaurant_ReportsApi.get_todayMealsNames, name='api/todaymealsnames/'),
    path('api/todaymealstotalno/', Restaurant_ReportsApi.get_todayMealsTotalNo, name='api/todaymealstotalno/'),
    # -------- PersonalsWhoDidNotSelectMeals report ---------
    path('api/personelwhodidnotselectmeals/<int:currentMonth>', Restaurant_ReportsApi.get_personalsWhoDidNotSelectMeals, name='api/personelwhodidnotselectmeals/<currentMonth>'),
    path('api/sectionnames/', Restaurant_ReportsApi.get_sectionNames, name='api/sectionnames'),
]

urlpatterns += router.urls
