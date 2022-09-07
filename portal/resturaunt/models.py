from django.db import models
from datetime import datetime, date
from django.db.models import Count

from baseInfo.models import Department, Project, Employee


class Restaurant_Meal(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField(null=True)
    picture = models.FileField(upload_to='meal_pix', null=True)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_restaurant_meal"

class Restaurant_Day_Meal(models.Model):
    restaurant_meal = models.ForeignKey(Restaurant_Meal, 
        related_name="RestaurantMeal_RestaurantDayMeal", on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    totalNo = models.IntegerField(null=True)
    monthID = models.SmallIntegerField(null=True)
    isActive = models.BooleanField(default=False, null=True)
    totalNoConfirmation = models.BooleanField(default=False, null=True)
    objects = models.Manager()  

    class Meta:
        unique_together = ('restaurant_meal', 'date')
        db_table = "tbl_restaurant_day_meal"

class Restaurant_Employee_Day_Meal(models.Model):
    restaurant_day_meal = models.ForeignKey(Restaurant_Day_Meal, 
        related_name="RestaurantDayMeal_RestaurantEmployeeDayMeal", on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, 
        related_name="Employee_RestaurantEmployeeDayMeal", on_delete=models.PROTECT)
    served = models.BooleanField(default=False)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_restaurant_employee_day_meal"  

class Restaurant_Guest_Day_Meal(models.Model):
    date = models.DateField(default=datetime.now, blank=True)
    department = models.ForeignKey(Department, 
        related_name="Department_RestaurantGuestDayMeal", on_delete=models.PROTECT, null=True) 
    project = models.ForeignKey(Project, 
        related_name="Project_RestaurantGuestDayMeal", on_delete=models.PROTECT, null=True)   
    restaurant_day_meals=models.ManyToManyField(Restaurant_Day_Meal, through='Restaurant_Guest_Day_Meal_junction')
    # date = models.DateField(default=datetime.now, blank=True)
    description=models.CharField(max_length=500, blank=True, null=True)
    objects = models.Manager()  

    class Meta:
        db_table = "tbl_restaurant_guest_day_meal"  

class Restaurant_Guest_Day_Meal_Junction(models.Model):
    restaurant_day_meal = models.ForeignKey(Restaurant_Day_Meal, 
        related_name="RestaurantDayMeal_RestaurantGuestDayMealJunction", on_delete=models.PROTECT)
    restaurant_guest_day_meal = models.ForeignKey(Restaurant_Guest_Day_Meal, 
        related_name="RestaurantGuestDayMeal_RestaurantGuestDayMealJunction", on_delete=models.PROTECT)
    qty = models.PositiveSmallIntegerField()
    objects = models.Manager()  

    class Meta:
        unique_together = [['restaurant_day_meal', 'restaurant_guest_day_meal']]
        db_table = "tbl_restaurant_guest_day_meal_junction"