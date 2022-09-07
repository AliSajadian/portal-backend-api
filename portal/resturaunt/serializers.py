from django.db import models
from rest_framework import serializers
from rest_framework.response import Response 

from resturaunt.models import Restaurant_Meal, Restaurant_Day_Meal, Restaurant_Employee_Day_Meal, \
    Restaurant_Guest_Day_Meal, Restaurant_Guest_Day_Meal_Junction
from baseInfo.models import Company, Department, Employee



# Meal ===========================================================
class Restaurant_MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_Meal
        fields = '__all__'

# Day Meal =======================================================
class Restaurant_Day_MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_Day_Meal
        fields = '__all__'
class Restaurant_Day_MealExSerializer(serializers.ModelSerializer):
    selectedNo = serializers.IntegerField()   
    # selectedNo = serializers.SerializerMethodField() 

    class Meta:
        model = Restaurant_Day_Meal
        fields = ('id', 'date', 'totalNo', 'isActive', 'totalNoConfirmation', 'restaurant_meal', 'selectedNo')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = Restaurant_Day_MealExSerializer(instance=instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = Restaurant_Day_MealExSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Employee Day Meal ==============================================
class Restaurant_Employee_Day_MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('id', 'employee', 'restaurant_day_meal')
class Restaurant_Employee_Day_MealExSerializer(serializers.ModelSerializer):
    restaurant_meal = serializers.SlugRelatedField(
        read_only=True,
        slug_field='restaurant_meal'
     )
    date = serializers.SlugRelatedField(
        read_only=True,
        slug_field='date'
     )
    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('id', 'employee', 'restaurant_day_meal', 'restaurant_meal', 'date')

# Guest Day Meal =================================================
class Restaurant_Guest_Day_MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_Guest_Day_Meal
        fields = '__all__'
class Restaurant_Guest_Day_MealExSerializer(serializers.ModelSerializer):
    departmentName = serializers.CharField() 
    projectName = serializers.CharField() 
    class Meta:
        model = Restaurant_Guest_Day_Meal
        fields = ('id', 'department', 'departmentName', 'project', 'projectName', 'description')
class Restaurant_Project_Guest_Day_MealSerializer(serializers.ModelSerializer):
    restaurant_day_meal_id = serializers.IntegerField() 
    class Meta:
        model = Restaurant_Guest_Day_Meal
        fields = ('id', 'department', 'project', 'description', 'restaurant_day_meal_id', 'date')
class Restaurant_Guest_Day_Meal_JunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_Guest_Day_Meal_Junction
        fields = '__all__'
class Restaurant_Guest_Day_Meal_JunctionExSerializer(serializers.ModelSerializer):
    mealName = serializers.CharField() 
    restaurant_guest_day_meal_junction_id = serializers.IntegerField() 
    qty = serializers.IntegerField() 
    class Meta:
        model = Restaurant_Day_Meal
        fields = ('id', 'date', 'totalNo', 'mealName', 'restaurant_guest_day_meal_junction_id', 'qty')

# Serve =========================================================
class Restaurant_Served_MealSerializer(serializers.ModelSerializer):
    restaurant_meal = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    meal_no = serializers.IntegerField()
    selectedNo = serializers.IntegerField()    
    servedNo = serializers.IntegerField()  

    class Meta:
        model = Restaurant_Day_Meal
        fields = ('id', 'meal_no', 'restaurant_meal', 'totalNo', 'selectedNo', 'servedNo')        
class Restaurant_Served_Guest_MealSerializer(serializers.ModelSerializer):
    guestMealNo = serializers.IntegerField() 

    class Meta:
        model = Restaurant_Day_Meal
        fields = ('id', 'guestMealNo')  

# Reports =======================================================
class Restaurant_Served_Guest_MealExSerializer(serializers.ModelSerializer):
    guestMealNo = serializers.IntegerField() 
    meal_name = serializers.CharField(source='restaurant_meal.name', default='')

    class Meta:
        model = Restaurant_Day_Meal
        fields = ('date', 'meal_name', 'guestMealNo')  
class Restaurant_Report_MealsDailyListSerializer(serializers.ModelSerializer):
    meal_ame = serializers.CharField() 
    employee_firstname = serializers.CharField() 
    employee_lastname = serializers.CharField() 
    employee_personnelcode = serializers.CharField() 

    qty = serializers.IntegerField() 
    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('employee_firstname', 'employee_lastname', 'employee_personnelcode', 'meal_ame')
class Restaurant_Report_MealsDailyListSerializer(serializers.ModelSerializer):
    meal_ame = serializers.CharField() 
    meal_date = serializers.CharField() 

    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('meal_ame', 'meal_date')
class Restaurant_Report_DayMealsStatisticsSerializer(serializers.ModelSerializer):
    section_type = serializers.IntegerField() 
    section = serializers.CharField() 
    meal_ame = serializers.CharField() 
    meal_no = serializers.IntegerField() 

    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('section_type', 'section', 'meal_name', 'meal_no')
class Restaurant_Report_SectionsDayMealsStatisticsSerializer(serializers.ModelSerializer):
    section = serializers.CharField() 
    meal_ame = serializers.CharField() 
    meal_no = serializers.IntegerField() 

    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('section', 'meal_name', 'meal_no')
class Restaurant_Report_ContractorMonthlyMealsStatisticsSerializer(serializers.ModelSerializer):
    date = serializers.CharField() 
    section = serializers.CharField() 
    meal_ame = serializers.CharField() 
    meal_no = serializers.IntegerField() 

    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('date', 'section', 'meal_name', 'meal_no')
class Restaurant_Report_ControlMonthlyMealsStatisticsSerializer(serializers.ModelSerializer):
    date = serializers.CharField() 
    meal_ame = serializers.CharField() 
    meal_no = serializers.IntegerField() 
    served_no = serializers.IntegerField() 
    total_no = serializers.IntegerField() 

    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('date', 'meal_name', 'meal_no', 'served_no', 'total_no')
class ContractorDailySectionMealsStatisticsTotalNoSerializer(serializers.ModelSerializer):
    meal_ame = serializers.CharField() 
    meal_no = serializers.IntegerField() 

    class Meta:
        model = Restaurant_Employee_Day_Meal
        fields = ('meal_name', 'meal_no')
class PersonalsWhoDidNotSelectMealsSerializer(serializers.ModelSerializer):
    section = serializers.CharField() 

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'phone', 'section')


