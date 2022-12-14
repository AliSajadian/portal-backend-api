# Generated by Django 4.1 on 2022-09-06 06:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseInfo', '0001_initial'),
        ('resturaunt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant_Day_Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('totalNo', models.IntegerField(null=True)),
                ('monthID', models.SmallIntegerField(null=True)),
                ('isActive', models.BooleanField(default=False, null=True)),
                ('totalNoConfirmation', models.BooleanField(default=False, null=True)),
            ],
            options={
                'db_table': 'tbl_restaurant_day_meal',
            },
        ),
        migrations.CreateModel(
            name='Restaurant_Employee_Day_Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('served', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Employee_RestaurantEmployeeDayMeal', to='baseInfo.employee')),
                ('restaurant_day_meal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='RestaurantDayMeal_RestaurantEmployeeDayMeal', to='resturaunt.restaurant_day_meal')),
            ],
            options={
                'db_table': 'tbl_restaurant_employee_day_meal',
            },
        ),
        migrations.CreateModel(
            name='Restaurant_Guest_Day_Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Department_RestaurantGuestDayMeal', to='baseInfo.department')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Project_RestaurantGuestDayMeal', to='baseInfo.project')),
            ],
            options={
                'db_table': 'tbl_restaurant_guest_day_meal',
            },
        ),
        migrations.CreateModel(
            name='Restaurant_Guest_Day_Meal_Junction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField()),
                ('restaurant_day_meal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='RestaurantDayMeal_RestaurantGuestDayMealJunction', to='resturaunt.restaurant_day_meal')),
                ('restaurant_guest_day_meal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='RestaurantGuestDayMeal_RestaurantGuestDayMealJunction', to='resturaunt.restaurant_guest_day_meal')),
            ],
            options={
                'db_table': 'tbl_restaurant_guest_day_meal_junction',
                'unique_together': {('restaurant_day_meal', 'restaurant_guest_day_meal')},
            },
        ),
        migrations.CreateModel(
            name='Restaurant_Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('calories', models.IntegerField(null=True)),
                ('picture', models.FileField(null=True, upload_to='meal_pix')),
            ],
            options={
                'db_table': 'tbl_restaurant_meal',
            },
        ),
        migrations.RemoveField(
            model_name='resturaunt_employee_day_meal',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='resturaunt_employee_day_meal',
            name='resturaunt_day_meal',
        ),
        migrations.RemoveField(
            model_name='resturaunt_guest_day_meal',
            name='department',
        ),
        migrations.RemoveField(
            model_name='resturaunt_guest_day_meal',
            name='project',
        ),
        migrations.RemoveField(
            model_name='resturaunt_guest_day_meal',
            name='resturaunt_day_meals',
        ),
        migrations.AlterUniqueTogether(
            name='resturaunt_guest_day_meal_junction',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='resturaunt_guest_day_meal_junction',
            name='resturaunt_day_meal',
        ),
        migrations.RemoveField(
            model_name='resturaunt_guest_day_meal_junction',
            name='resturaunt_guest_day_meal',
        ),
        migrations.DeleteModel(
            name='Resturaunt_Day_Meal',
        ),
        migrations.DeleteModel(
            name='Resturaunt_Employee_Day_Meal',
        ),
        migrations.DeleteModel(
            name='Resturaunt_Guest_Day_Meal',
        ),
        migrations.DeleteModel(
            name='Resturaunt_Guest_Day_Meal_Junction',
        ),
        migrations.DeleteModel(
            name='Resturaunt_Meal',
        ),
        migrations.AddField(
            model_name='restaurant_guest_day_meal',
            name='restaurant_day_meals',
            field=models.ManyToManyField(through='resturaunt.Restaurant_Guest_Day_Meal_Junction', to='resturaunt.restaurant_day_meal'),
        ),
        migrations.AddField(
            model_name='restaurant_day_meal',
            name='restaurant_meal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RestaurantMeal_RestaurantDayMeal', to='resturaunt.restaurant_meal'),
        ),
        migrations.AlterUniqueTogether(
            name='restaurant_day_meal',
            unique_together={('restaurant_meal', 'date')},
        ),
    ]
