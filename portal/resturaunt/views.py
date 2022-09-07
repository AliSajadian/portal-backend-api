from rest_framework.response import Response 
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count, Q, F, Window, Value, CharField, SmallIntegerField, Sum
from django.db.models.functions import RowNumber
from datetime import date, datetime ,timedelta
from django_pivot.pivot import pivot

from baseInfo.models import Employee, Department, Project
from resturaunt.models import Restaurant_Meal, Restaurant_Day_Meal, Restaurant_Employee_Day_Meal, \
                              Restaurant_Guest_Day_Meal_Junction, Restaurant_Guest_Day_Meal
from .serializers import Restaurant_MealSerializer, Restaurant_Day_MealSerializer, Restaurant_Day_MealExSerializer, \
    Restaurant_Served_MealSerializer, Restaurant_Employee_Day_MealSerializer, Restaurant_Employee_Day_MealExSerializer, \
    Restaurant_Guest_Day_MealSerializer, Restaurant_Guest_Day_MealExSerializer, Restaurant_Project_Guest_Day_MealSerializer, \
    Restaurant_Served_Guest_MealSerializer, Restaurant_Served_Guest_MealExSerializer, Restaurant_Guest_Day_Meal_JunctionSerializer, \
    Restaurant_Guest_Day_Meal_JunctionExSerializer, Restaurant_Report_MealsDailyListSerializer, Restaurant_Report_MealsDailyListSerializer, \
    Restaurant_Report_DayMealsStatisticsSerializer, Restaurant_Report_SectionsDayMealsStatisticsSerializer, \
    Restaurant_Report_ContractorMonthlyMealsStatisticsSerializer, Restaurant_Report_ControlMonthlyMealsStatisticsSerializer, \
    ContractorDailySectionMealsStatisticsTotalNoSerializer, PersonalsWhoDidNotSelectMealsSerializer
from .services import getCurrentMonthRange, getCurrentMonthRangeEx, getCurrentMonthRangePro, getNextMonthRange


# meal api ++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Restaurant_MealViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_Meal.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = Restaurant_MealSerializer
# meal api ++++++++++++++++++++++++++++++++++++++++++++++++++++++

# day_meal api ++++++++++++++++++++++++++++++++++++++++++++++++++
class Restaurant_Day_MealViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_Day_Meal.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = Restaurant_Day_MealSerializer
class Restaurant_Day_MealApi(generics.GenericAPIView):
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_mealsDayByDate(request, selectedDate):
        mealDate = datetime.strptime(selectedDate, '%Y-%m-%d').date()

        results = Restaurant_Day_Meal.objects.filter(date__exact=mealDate).values(
                                                'id', 'date', 'restaurant_meal__name', 'totalNo')
        return Response(results)    
    
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_currentMonthMealsDays(request):
        currentdate = date.today()
        startdate, enddate = getCurrentMonthRange(currentdate)
        return Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate, isActive__in=[False])

    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_nextMonthMealsDays(request):
        currentdate = date.today()
        startdate, enddate = getNextMonthRange(currentdate)
        return Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate , isActive__in=[False])

    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_currentMonthMealsDays_SelectedNos(request, selectedDate):
        startdate, enddate = getCurrentMonthRangeEx(selectedDate)

        results = Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate).annotate(                    
            selectedNo=Count('RestaurantDayMeal_RestaurantEmployeeDayMeal'))
            # .values('id', 'date', 'totalNo', 'isActive', 'totalNoConfirmation', 'restaurant_meal', 'selectedNo')
        serializer = Restaurant_Day_MealExSerializer(data=results)
        return Response(serializer.data)    

    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    def add_mealsDays_get_nextMonthMealsDays(request):
        data = request.data
        date = data['date']
        restaurant_meal = data['restaurant_meal']
        totalNo = data['totalNo']
        isActive = data['isActive']

        rdm = Restaurant_Meal.objects.get(pk=restaurant_meal)
        obj = Restaurant_Day_Meal.objects.create(date=date, totalNo=totalNo, restaurant_meal=rdm, isActive=isActive) 
        obj.save()

        startdate, enddate = getNextMonthRange(date)

        results = Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate).annotate(                    
            selectedNo=Count('RestaurantDayMeal_RestaurantEmployeeDayMeal'))
            # .values('id', 'date', 'totalNo', 'isActive', 'restaurant_meal', 'selectedNo')
        serializer = Restaurant_Day_MealExSerializer(data=results)
        return Response(serializer.data)   

    @api_view(['PUT'])
    @permission_classes([permissions.IsAuthenticated])
    def edit_mealsDays_get_nextMonthMealsDays(request):
        data = request.data
        id = data['id']
        date = data['date']
        restaurant_meal = data['restaurant_meal']
        totalNo = data['totalNo']
        # isActive = data['isActive']

        meal = Restaurant_Meal.objects.get(pk=restaurant_meal)
        obj = Restaurant_Day_Meal.objects.get(pk=id)
        obj.restaurant_meal = meal
        obj.totalNo = totalNo
        obj.save()

        startdate, enddate = getNextMonthRange(date)

        results = Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate).annotate(                    
            selectedNo=Count('RestaurantDayMeal_RestaurantEmployeeDayMeal'))
            # .values('id', 'date', 'totalNo', 'isActive', 'restaurant_meal', 'selectedNo')
        serializer = Restaurant_Day_MealExSerializer(data=results)
        return Response(serializer.data)   

    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    def activate_mealsDays_get_currentMonthMealsDays(request, date, flag):
        startdate, enddate = getCurrentMonthRange(date)

        results = Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate).values('id')

        objs = []
        if(flag == 1):
            for dm in results:
                obj = Restaurant_Day_Meal.objects.get(id=dm['id'])
                obj.isActive = False
                objs.append(obj)         
            Restaurant_Day_Meal.objects.bulk_update(objs, ['isActive'])              
        else:
            for dm in results:
                obj = Restaurant_Day_Meal.objects.get(id=dm['id'])
                obj.totalNoConfirmation = False
                objs.append(obj)   
            Restaurant_Day_Meal.objects.bulk_update(objs, ['totalNoConfirmation'])
     

        result = Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate).annotate(
                selectedNo=Count('RestaurantDayMeal_RestaurantEmployeeDayMeal'))
                # .values('id', 'date', 'totalNo', 'isActive', 'totalNoConfirmation', 'restaurant_meal', 'selectedNo')
        serializer = Restaurant_Day_MealExSerializer(data=result, many=True)
        return Response(serializer.data)   
# day_meal api ++++++++++++++++++++++++++++++++++++++++++++++++++

# employee_day_meal api +++++++++++++++++++++++++++++++++++++++++
class Restaurant_Employee_Day_MealViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_Employee_Day_Meal.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = Restaurant_Employee_Day_MealExSerializer
class Restaurant_Employee_Day_MealApi(generics.GenericAPIView):
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_currentMonthEmployeeMealsDays(request, employee_id):
        currentdate = date.today()
        startdate, enddate = getCurrentMonthRange(currentdate)
            
        result = Restaurant_Employee_Day_Meal.objects.filter(employee=employee_id, 
            restaurant_day_meal__date__gte=startdate, restaurant_day_meal__date__lte=enddate)
        return Response(result)

    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_nextMonthEmployeeMealsDays(request, employee_id):
        currentdate = date.today()
        startdate, enddate = getNextMonthRange(currentdate)

        result = Restaurant_Employee_Day_Meal.objects.filter(employee=employee_id, 
            restaurant_day_meal__date__gte=startdate, restaurant_day_meal__date__lte=enddate)
        return Response(result)

    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    def save_get_currentMonthEmployeeMealsDays(request):
        try:
            import json
            data = request.data
            personnelMealDays = data["personelMealDays"]
            editMood = data["editMood"]

            employee_id = personnelMealDays[0]['employee']

            currentdate = datetime.today()
            startdate, enddate = getCurrentMonthRange(currentdate)

            if(editMood):
                dt = currentdate + timedelta(days=3)
                next3DaysDate = dt.date()

                result = Restaurant_Employee_Day_Meal.objects.filter(
                    employee=employee_id, 
                    restaurant_day_meal__date__gte=startdate, 
                    restaurant_day_meal__date__lte=enddate)

                mealDays = Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate).filter(date__gt=next3DaysDate)
                mealDayNo = mealDays.count()
                firstMealDay = mealDays.first()
                mealsDayNo =  Restaurant_Day_Meal.objects.filter(date__exact=firstMealDay.date).count()
                mealSelectedNo = (mealDayNo // mealsDayNo)
                # and len(personnelMealDays) == mealSelectedNo
                if(len(result) == 0 ):
                    objs = []
                    for pmd in personnelMealDays:
                        obj = Restaurant_Employee_Day_Meal(employee_id=pmd['employee'], restaurant_day_meal_id=pmd['restaurant_day_meal'])
                        objs.append(obj)
                    Restaurant_Employee_Day_Meal.objects.bulk_create(objs)   

                result = Restaurant_Employee_Day_Meal.objects.filter(employee=employee_id, 
                    restaurant_day_meal__date__gte=startdate, restaurant_day_meal__date__lte=enddate)
                    # .values('id', 'employee', 'restaurant_day_meal'))
                serializer = Restaurant_Employee_Day_MealSerializer(data=result)
                return Response(serializer.data)

            else:
                objs = []
                for pmd in personnelMealDays:
                    obj = Restaurant_Employee_Day_Meal.objects.get(id=pmd['id'])
                    obj.restaurant_day_meal_id = pmd['restaurant_day_meal']
                    objs.append(obj)
                Restaurant_Employee_Day_Meal.objects.bulk_update(objs, ['restaurant_day_meal'])     

                result = Restaurant_Employee_Day_Meal.objects.filter(employee=employee_id, 
                    restaurant_day_meal__date__gte=startdate, restaurant_day_meal__date__lte=enddate)
                    # .values('id', 'employee', 'restaurant_day_meal'))
                serializer = Restaurant_Employee_Day_MealSerializer(data=result)
                return Response(serializer.data)                    

        except Exception as e:
            return Response(e)     

    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    def save_get_nextMonthEmployeeMealsDays(request):
        try:
            import json
            data = request.data
            personnelMealDays = data["personelMealDays"]
            editMood = data["editMood"]

            employee_id = personnelMealDays[0]['employee']

            currentdate = datetime.today()
            startdate, enddate = getNextMonthRange(currentdate)

            if(editMood):
                dt = currentdate + timedelta(days=3)
                next3DaysDate = dt.date()

                result = Restaurant_Employee_Day_Meal.objects.filter(
                    employee=employee_id, 
                    restaurant_day_meal__date__gte=startdate, 
                    restaurant_day_meal__date__lte=enddate)

                mealDays = Restaurant_Day_Meal.objects.filter(date__gte=startdate, date__lte=enddate).filter(date__gt=next3DaysDate)
                mealDayNo = mealDays.count()
                firstMealDay = mealDays.first()
                mealsDayNo =  Restaurant_Day_Meal.objects.filter(date__exact=firstMealDay.date).count()
                mealSelectedNo = (mealDayNo // mealsDayNo)
                if(len(result) == 0  and len(personnelMealDays) == mealSelectedNo):
                    objs = []
                    for pmd in personnelMealDays:
                        obj = Restaurant_Employee_Day_Meal(employee_id=pmd['employee'], restaurant_day_meal_id=pmd['restaurant_day_meal'])
                        objs.append(obj)
                    Restaurant_Employee_Day_Meal.objects.bulk_create(objs)   

                result = Restaurant_Employee_Day_Meal.objects.filter(employee=employee_id, 
                    restaurant_day_meal__date__gte=startdate, restaurant_day_meal__date__lte=enddate)
                    #.values('id', 'employee', 'restaurant_day_meal'))
                serializer = Restaurant_Employee_Day_MealSerializer(data=result)
                return Response(serializer.data)
            else:
                objs = []
                for pmd in personnelMealDays:
                    obj = Restaurant_Employee_Day_Meal.objects.get(id=pmd['id'])
                    obj.restaurant_day_meal_id = pmd['restaurant_day_meal']
                    objs.append(obj)
                Restaurant_Employee_Day_Meal.objects.bulk_update(objs, ['restaurant_day_meal'])     

                result = Restaurant_Employee_Day_Meal.objects.filter(employee=employee_id, 
                    restaurant_day_meal__date__gte=startdate, restaurant_day_meal__date__lte=enddate)
                    #.values('id', 'employee', 'restaurant_day_meal'))                         
                serializer = Restaurant_Employee_Day_MealSerializer(data=result)
                return Response(serializer.data)
        except Exception as e:
            return Response(e)
# employee_day_meal api +++++++++++++++++++++++++++++++++++++++++

# restaurant serve api ++++++++++++++++++++++++++++++++++++++++++
class Restaurant_Serve_MealApi(viewsets.ModelViewSet):
    @api_view(['Get'])
    def get_employeeFishMealState(request, pk):
        currentdate = date.today()

        emps = Employee.objects.filter(personel_code__exact=pk)
        if(emps.exists() and len(emps) == 1):
            empid = emps[0].id

            # ****************************************************************************
            if(str(p_code) in ('11111111', '22222222', '33333333', '44444444', '55555555')):
                redms = Restaurant_Employee_Day_Meal.objects.filter(employee__exact=empid, restaurant_day_meal__date__exact=currentdate)
                rdm_id = redms[0].restaurant_day_meal.id

                aggregate = Restaurant_Day_Meal.objects.filter(date=currentdate, id__lte=rdm_id).exclude(
                    Q(restaurant_meal__name__exact='عدم انتخاب') |
                    Q(restaurant_meal__name__exact='عدم حضور')).aggregate(meal_no=Count('id'))
                mealNo = aggregate['meal_no']     

                return Response(
                    Restaurant_Employee_Day_Meal.objects.filter(employee__exact=empid, restaurant_day_meal__date__exact=currentdate, served__in=[False]
                    ).annotate(meal_no=Value(mealNo, output_field=CharField())).values('id', 'meal_no', 'restaurant_day_meal__restaurant_meal__name', 
                            'employee__first_name', 'employee__last_name', 'employee__department__company__name'))
            # ****************************************************************************

            notselected = Restaurant_Employee_Day_Meal.objects.filter(employee__exact=empid, 
                restaurant_day_meal__date__exact=currentdate, restaurant_day_meal__restaurant_meal__name__exact='عدم انتخاب')
            if(notselected.exists() and len(notselected) == 1):
                return Response(
                    3
                    # گزینه عدم انتخاب
                )
            notpresent = Restaurant_Employee_Day_Meal.objects.filter(employee__exact=empid, 
                restaurant_day_meal__date__exact=currentdate, restaurant_day_meal__restaurant_meal__name__exact='عدم حضور')
            if(notpresent.exists() and len(notpresent) == 1):
                return Response(
                    4
                    # گزینه عدم حضور
                )
            redms = Restaurant_Employee_Day_Meal.objects.filter(employee__exact=empid, restaurant_day_meal__date__exact=currentdate)
            if(redms.exists() and len(redms) == 1):
                if(redms[0].served == True):
                    return Response(
                        5
                        # غذا گرفته است
                    )
                else:
                    rdm_id = redms[0].restaurant_day_meal.id

                    aggregate = Restaurant_Day_Meal.objects.filter(date=currentdate, id__lte=rdm_id).exclude(
                        Q(restaurant_meal__name__exact='عدم انتخاب') |
                        Q(restaurant_meal__name__exact='عدم حضور')).aggregate(meal_no=Count('id'))
                    mealNo = aggregate['meal_no']     

                    return Response(
                        Restaurant_Employee_Day_Meal.objects.filter(employee__exact=empid, restaurant_day_meal__date__exact=currentdate, served__in=[False]
                        ).annotate(meal_no=Value(mealNo, output_field=CharField())).values('id', 'meal_no', 'restaurant_day_meal__restaurant_meal__name', 
                                'employee__first_name', 'employee__last_name', 'employee__department__company__name')
                    )
            else:
                return Response(
                    2 
                    # فاقد انتخاب
                )
        else:
            return Response(
                1
                # موجود نمیباشد
            )

    @api_view(['Get'])
    def get_dayMealsStatistics(request):
        currentdate = date.today()
        result = Restaurant_Day_Meal.objects.filter(date__exact=currentdate).exclude(
            Q(restaurant_meal__name__exact='عدم انتخاب') |
            Q(restaurant_meal__name__exact='عدم حضور')).annotate(
                selectedNo=Count('RestaurantDayMeal_RestaurantEmployeeDayMeal')).annotate(
                servedNo=Count('RestaurantDayMeal_RestaurantEmployeeDayMeal', 
                        filter=Q(RestaurantDayMeal_RestaurantEmployeeDayMeal__served=True))).annotate(
                meal_no=Window(expression=RowNumber(), order_by=F('id').asc())).order_by('meal_no', 'id')

        serializer = Restaurant_Served_MealSerializer(data=result)
        return Response(serializer.data)

    @api_view(['Get'])
    def Get_GuestMealsNo(request):
        currentdate = date.today()
        result = Restaurant_Day_Meal.objects.filter(date__exact=currentdate).exclude(
            Q(restaurant_meal__name__exact='عدم انتخاب') |
            Q(restaurant_meal__name__exact='عدم حضور')).annotate(
                guestMealNo=Sum('RestaurantDayMeal_RestaurantGuestDayMealJunction__qty'))
        serializer  = Restaurant_Served_Guest_MealSerializer(data = result, many=True)
        return Response(serializer.data)

    @api_view(['Post'])
    def patch_serveEmployeeDayMeals(request, pk):
        currentdate = date.today()
        redm = Restaurant_Employee_Day_Meal.objects.get(id=pk)
        emp_id = redm.employee_id
        emp = Employee.objects.get(pk=emp_id)
        p_code = 0

        if(emp is not None):
            p_code = emp.personel_code

        if(str(p_code) not in ('11111111', '22222222', '33333333', '44444444', '55555555')):
            redm.served = True
            redm.save()
        else:
            departmentId = 1
            projectId = None
            description = 'temprary'
            guestMealId = 0
            dayMealId = redm.restaurant_day_meal_id

            rgdm_filter = Restaurant_Guest_Day_Meal.objects.filter(date__exact=currentdate, department_id = departmentId, project_id = projectId, description = description)
            if(rgdm_filter is None or len(rgdm_filter) == 0):
                add_rgdm = Restaurant_Guest_Day_Meal.objects.create(date = currentdate, department_id = departmentId, project_id = projectId, description = description)
                add_rgdm.save()
                guestMealId = add_rgdm.id
                add_rgdmj = Restaurant_Guest_Day_Meal_Junction.objects.create(restaurant_day_meal_id = dayMealId, restaurant_guest_day_meal_id = guestMealId, qty = 1)
                add_rgdmj.save()
            else:
                guestMealId = rgdm_filter[0].id
                rgdmj_filter = Restaurant_Guest_Day_Meal_Junction.objects.filter(restaurant_day_meal_id = dayMealId, restaurant_guest_day_meal_id = guestMealId)
                if(rgdmj_filter is None or len(rgdmj_filter) == 0):
                    add_rgdmj = Restaurant_Guest_Day_Meal_Junction.objects.create(restaurant_day_meal_id = dayMealId, restaurant_guest_day_meal_id = guestMealId, qty = 1)
                    add_rgdmj.save()
                else:
                    edit_rgdmj = rgdmj_filter[0]
                    edit_rgdmj.qty = edit_rgdmj.qty + 1
                    edit_rgdmj.save()                        

        return Response(
            'Meal Served'
        )
# restaurant serve api ++++++++++++++++++++++++++++++++++++++++++

# guest_day_meal api ++++++++++++++++++++++++++++++++++++++++++++
class Restaurant_Guest_Day_MealViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_Guest_Day_Meal.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ] 

    serializer_class = Restaurant_Guest_Day_MealSerializer
class Restaurant_Guest_Day_MealApi(generics.GenericAPIView):
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_guestMealsDayList(request, selectedDate):
        try:
            date = selectedDate
            mealDate = datetime.strptime(date, '%Y-%m-%d').date()

            result = Restaurant_Guest_Day_Meal.objects.filter(
                                        date__exact=mealDate).values('id', 'department', 'departmentName', 'project', 'projectName', 'description')
            serializer = Restaurant_Guest_Day_MealExSerializer(data=result, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)

    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_projectGuestMealsDayList(request, selectedDate, projectId):
        mealDate = datetime.strptime(selectedDate, '%Y-%m-%d').date()

        result = Restaurant_Guest_Day_Meal.objects.filter(date__exact=mealDate,
                                    project__exact=projectId).annotate(
                                    restaurant_day_meal_id = F('RestaurantGuestDayMeal_RestaurantGuestDayMealJunction__restaurant_day_meal__id')
                                    ).values('id', 'department', 'project', 'description', 'restaurant_day_meal_id', 'date')
        serializer = Restaurant_Project_Guest_Day_MealSerializer(data=result, many=True)
        return Response(serializer.data)

    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_guestJunctionList(request, selectedDate):
        try:
            mealDate = datetime.strptime(selectedDate, '%Y-%m-%d').date()

            result = Restaurant_Guest_Day_Meal_Junction.objects.filter(
                                        restaurant_guest_day_meal__date__exact=mealDate).values('id', 
                                        'restaurant_day_meal', 'restaurant_guest_day_meal', 'qty')
            serializer = Restaurant_Guest_Day_Meal_JunctionSerializer(data=result, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)

    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    def create_guestDayMeals(request):
        try:
            data = request.data
            id = data["id"]
            date = data["date"]
            departmentId = data["departmentId"]
            projectId = data["projectId"]
            description = data["description"]
            guestDayMeals = data["guestDayMeals"]
            editMode = data["editMode"]

            rgdm = Restaurant_Guest_Day_Meal.objects.update_or_create(date=date, department_id = departmentId, project_id = projectId, description = description)
            rgdm.save()
            guestMealId = rgdm.id

            objs = []
            for gdm in guestDayMeals:
                obj = Restaurant_Guest_Day_Meal_Junction(restaurant_day_meal_id = gdm['restaurant_day_meal'], restaurant_guest_day_meal_id = guestMealId, qty = gdm['qty'])
                objs.append(obj)
            Restaurant_Guest_Day_Meal_Junction.objects.bulk_create(objs) 

            return Response('ok')
        except Exception as e:
            return Response(e) 

    @api_view(['PUT'])
    @permission_classes([permissions.IsAuthenticated])
    def update_guestDayMeals(request):
        try:
            data = request.data
            id = data["id"]
            departmentId = data["departmentId"]
            description = data["description"]

            guest_day_meal = Restaurant_Guest_Day_Meal.objects.get(pk=id)
            guest_day_meal.department_id = departmentId
            guest_day_meal.description = description
            guest_day_meal.save()

            result = Restaurant_Guest_Day_Meal.objects.filter(id__exact=id).annotate(
                            restaurant_day_meal_id = F('RestaurantGuestDayMeal_RestaurantGuestDayMealJunction__restaurant_day_meal__id')
                            ).values('id', 'department', 'project', 'description', 'restaurant_day_meal_id', 'date')
            serializer = Restaurant_Project_Guest_Day_MealSerializer(data=result)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)  
    
    @api_view(['PUT'])
    @permission_classes([permissions.IsAuthenticated])
    def update_guestDayMealsJunction(request):
        data = request.data
        departmentId = data["departmentId"]
        mealDayId = data["mealDayId"]
        guestMealDayId = data["guestMealDayId"]
        qty = data["qty"]
        mood = data["mood"]

        day_meal = Restaurant_Day_Meal.objects.get(pk=mealDayId)
        mealDate = day_meal.date

        if(mood == 1):
            guest_day_meal = Restaurant_Guest_Day_Meal(department_id=departmentId, description='')
            guest_day_meal.save()
            guestMealDayId = guest_day_meal.id

            guest_day_meal_junction = Restaurant_Guest_Day_Meal_Junction(restaurant_day_meal_id=mealDayId, 
                                                                        restaurant_guest_day_meal_id=guestMealDayId,
                                                                        qty=qty)
            guest_day_meal_junction.save()
        elif(mood == 2):
            guest_day_meal_junction = Restaurant_Guest_Day_Meal_Junction(restaurant_day_meal_id=mealDayId, 
                                                                        restaurant_guest_day_meal_id=guestMealDayId,
                                                                        qty=qty)
            guest_day_meal_junction.save()
        elif(mood == 3):
            guest_day_meal_junction = Restaurant_Guest_Day_Meal_Junction.objects.get(restaurant_day_meal_id=mealDayId, 
                                                                        restaurant_guest_day_meal_id=guestMealDayId)
            guest_day_meal_junction.qty = qty
            guest_day_meal_junction.save()

        results1 = Restaurant_Day_Meal.objects.filter(date__exact=mealDate,
                                                restaurant_guest_day_meal__id__exact=guestMealDayId)
        results2 = Restaurant_Day_Meal.objects.filter(date__exact=mealDate,
                                                restaurant_guest_day_meal__id__exact=guestMealDayId).annotate(
                                                restaurant_guest_day_meal_junction_id = F('RestaurantDayMeal_RestaurantGuestDayMealJunction__id'),
                                                qty = F('RestaurantDayMeal_RestaurantGuestDayMealJunction__qty')
                                                ).values('id', 'date', 'restaurant_meal__name', 'totalNo', 'restaurant_guest_day_meal_junction_id', 'qty')


        results3 = Restaurant_Day_Meal.objects.filter(date__exact=mealDate).exclude(id__in=results1).annotate(
                                                restaurant_guest_day_meal_junction_id = F('RestaurantDayMeal_RestaurantGuestDayMealJunction__id'),
                                                qty = F('RestaurantDayMeal_RestaurantGuestDayMealJunction__qty')
                                                ).values('id', 'date', 'restaurant_meal__name', 'totalNo', 'restaurant_guest_day_meal_junction_id', 'qty')
        results4 = results3.union(results2)
        serializer = Restaurant_Guest_Day_Meal_JunctionExSerializer(data=results4, many=True)
        return Response(serializer.data) 

    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    def save_guestDayMeals(request):
        try:
            data = request.data

            guestMealId = data["id"]
            date = data["date"]
            departmentId = data["department"]
            projectId = data["project"]
            description = data["description"]
            guestDayMealsJunction = data["guestDayMeals"]

            objs = []
            if(guestMealId == -1):
                add_rgdm = Restaurant_Guest_Day_Meal.objects.create(
                    date = date, 
                    department_id = departmentId if(departmentId != 0) else None, 
                    project_id = projectId if(projectId != 0) else None, 
                    description = description)
                add_rgdm.save()

                guestMealId = add_rgdm.id
                for gdm in guestDayMealsJunction:
                    if(gdm["qty"] is not None and gdm["qty"] > 0):
                        obj = Restaurant_Guest_Day_Meal_Junction(
                            restaurant_day_meal_id = gdm["restaurant_day_meal"], 
                            restaurant_guest_day_meal_id = guestMealId, 
                            qty = gdm["qty"])
                        objs.append(obj)
                if(len(objs) > 0):
                    Restaurant_Guest_Day_Meal_Junction.objects.bulk_create(objs) 
            else:
                rgdm_edit = Restaurant_Guest_Day_Meal.objects.get(pk=guestMealId)
                rgdm_edit.department_id = departmentId if(departmentId != 0) else None
                rgdm_edit.project_id = projectId if(projectId != 0) else None
                rgdm_edit.description = description
                rgdm_edit.save()
            
                Restaurant_Guest_Day_Meal_Junction.objects.filter(restaurant_guest_day_meal_id = guestMealId).delete()
                
                for gdm in guestDayMealsJunction:
                    if(gdm['qty'] is not None and gdm['qty'] > 0):
                        obj = Restaurant_Guest_Day_Meal_Junction(
                            restaurant_day_meal_id = gdm['restaurant_day_meal'], 
                            restaurant_guest_day_meal_id = guestMealId, 
                            qty = gdm['qty'])
                        objs.append(obj)
                if(len(objs) > 0):
                    Restaurant_Guest_Day_Meal_Junction.objects.bulk_create(objs) 
            return Response('ok')
        except Exception as e:
            return Response('error: ', str(e)) 
                
    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])# not used
    def save_guestDayMealsJunction(request):
        data = request.data
        departmentId = data["departmentId"]
        projectId = data["projectId"]
        description = data["description"]
        mealDayId = data["mealDayId"]
        mealsNo = data["mealsNo"]

        day_meal = Restaurant_Day_Meal.objects.get(pk=mealDayId)
        mealDate = day_meal.date

        if(mood == 1):
            guest_day_meal = Restaurant_Guest_Day_Meal(department_id=departmentId, description=description)
            guest_day_meal.save()
            guestMealDayId = guest_day_meal.id

            guest_day_meal_junction = Restaurant_Guest_Day_Meal_Junction(restaurant_day_meal_id=mealDayId, 
                                                                        restaurant_guest_day_meal_id=guestMealDayId,
                                                                        qty=qty)
            guest_day_meal_junction.save()
        elif(mood == 2):
            guest_day_meal_junction = Restaurant_Guest_Day_Meal_Junction(restaurant_day_meal_id=mealDayId, 
                                                                        restaurant_guest_day_meal_id=guestMealDayId,
                                                                        qty=qty)
            guest_day_meal_junction.save()
        elif(mood == 3):
            guest_day_meal_junction = Restaurant_Guest_Day_Meal_Junction.objects.get(restaurant_day_meal_id=mealDayId, 
                                                                        restaurant_guest_day_meal_id=guestMealDayId)
            guest_day_meal_junction.qty = qty
            guest_day_meal_junction.save()

        results1 = Restaurant_Day_Meal.objects.filter(date__exact=mealDate,
                                                restaurant_guest_day_meal__id__exact=guestMealDayId)
        results2 = Restaurant_Day_Meal.objects.filter(date__exact=mealDate,
                                                restaurant_guest_day_meal__id__exact=guestMealDayId).values(
                                                'id', 'date', 'restaurant_meal__name', 'totalNo', 
                                                'RestaurantDayMeal_RestaurantGuestDayMealJunction__id',
                                                'RestaurantDayMeal_RestaurantGuestDayMealJunction__qty')


        results3 = Restaurant_Day_Meal.objects.filter(date__exact=mealDate).exclude(id__in=results1).values(
                                                'id', 'date', 'restaurant_meal__name', 'totalNo', 
                                                'RestaurantDayMeal_RestaurantGuestDayMealJunction__id',
                                                'RestaurantDayMeal_RestaurantGuestDayMealJunction__qty')
        reuslts3 = results3.union(results2)

        return Response(reuslts3) 

    @api_view(['DELETE'])
    @permission_classes([permissions.IsAuthenticated])
    def remove_guestDayMeals(request, pk):
        guest_meals = Restaurant_Guest_Day_Meal.objects.get(id=pk)
        guestMealId = guest_meals.id
        Restaurant_Guest_Day_Meal_Junction.objects.filter(restaurant_guest_day_meal_id = guestMealId).delete()
        guest_meals.delete()
        return Response('ok')
# guest_day_meal api ++++++++++++++++++++++++++++++++++++++++++++

# report api ++++++++++++++++++++++++++++++++++++++++++++++++++++
# ------------- controlMonthlyMealsStatics report ---------------
class Restaurant_ReportsApi(viewsets.ModelViewSet):
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_controlMonthlyMealsStatics(request):
        currentdate = date.today()
        startdate,_ = getNextMonthRange(currentdate)

        result = Restaurant_Day_Meal.objects.filter(date__gte=startdate,date__lte=currentdate).exclude(
            Q(restaurant_meal__name__exact='عدم انتخاب') |
            Q(restaurant_meal__name__exact='عدم حضور')).annotate(
                guestMealNo=Sum('RestaurantDayMeal_RestaurantGuestDayMealJunction__qty'))
        serializer = Restaurant_Served_Guest_MealExSerializer(data=result, many=True)
        return Response(serializer.data)
# ------------------- mealsDailyList report ---------------------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_departmentMealsDailyList(request, departmentId):
        try:
            currentdate = date.today()

            result1 = Restaurant_Day_Meal.objects.filter(date__exact=currentdate)
            result = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__in=result1, employee__department_id__exact=departmentId).annotate(
                                employee_firstname = F('employee__first_name'),
                                employee_lastname = F('employee__last_name'),
                                employee_personelcode = F('employee__personel_code'),
                                meal_name = F('restaurant_day_meal__restaurant_meal__name'),
                                ).values(
                                'employee_firstname', 'employee_lastname', 'employee_personelcode', 'meal_name').order_by('meal_name')
            serializer = Restaurant_Report_MealsDailyListSerializer(data=result, many=True)
            return Response(serializer.data)                   
        except Exception as e:
            return Response(e)    
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_projectMealsDailyList(request, projectId):
        try:
            currentdate = date.today()

            result1 = Restaurant_Day_Meal.objects.filter(date__exact=currentdate)
            result = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__in=result1, employee__project_id__exact=projectId).annotate(
                                employee_firstname = F('employee__first_name'),
                                employee_lastname = F('employee__last_name'),
                                employee_personelcode = F('employee__personel_code'),
                                meal_name = F('restaurant_day_meal__restaurant_meal__name'),
                                ).values(
                                'employee_firstname', 'employee_lastname', 'employee_personelcode', 'meal_name').order_by('meal_name')
            serializer = Restaurant_Report_MealsDailyListSerializer(data=result, many=True)
            return Response(serializer.data)                   
        except Exception as e:
            return Response(e)  
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_departmentDayMealsStatistics(request, departmentId):
        currentdate = date.today()

        results = Restaurant_Employee_Day_Meal.objects.filter(
            restaurant_day_meal__date__exact=currentdate,  
            employee__department__exact=departmentId).values(
            'employee__department').order_by('employee__department__name').annotate(
            section=F('employee__department__name'), 
            meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
            meal_no=Count('restaurant_day_meal__restaurant_meal__name')).values(
            'section', 'meal_name', 'meal_no')

        serializer = Restaurant_Report_SectionsDayMealsStatisticsSerializer(data=results, many=True)
        return Response(serializer.data)        
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_projectDayMealsStatistics(request, projectId):
        currentdate = date.today()

        results = Restaurant_Employee_Day_Meal.objects.filter(
            restaurant_day_meal__date__exact=currentdate,  
            employee__project__exact=projectId).values(
            'employee__project').order_by('employee__project__name').annotate(
            section=F('employee__project__name'), 
            meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
            meal_no=Count('restaurant_day_meal__restaurant_meal__name')).values(
            'section', 'meal_name', 'meal_no')

        serializer = Restaurant_Report_SectionsDayMealsStatisticsSerializer(data=results, many=True)
        return Response(serializer.data)        

# ---------------- sectionMealsDailyList report -----------------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_sectionMealsDailyList(request, employeeId):
        try:
            currentdate = date.today()

            departmentId = Employee.objects.get(pk=employeeId).department_id
            projectId = Employee.objects.get(pk=employeeId).project_id

            if(projectId == None):
                result1 = Restaurant_Day_Meal.objects.filter(date__exact=currentdate)
                result = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__in=result1, employee__department_id__exact=departmentId).annotate(
                                employee_firstname = F('employee__first_name'),
                                employee_lastname = F('employee__last_name'),
                                employee_personelcode = F('employee__personel_code'),
                                meal_name = F('restaurant_day_meal__restaurant_meal__name'),
                                ).values(
                                'employee_firstname', 'employee_lastname', 'employee_personelcode', 'meal_name').order_by('meal_name')
            elif(departmentId == None):
                result1 = Restaurant_Day_Meal.objects.filter(date__exact=currentdate)
                result = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__in=result1, employee__project_id__exact=projectId).annotate(
                                employee_firstname = F('employee__first_name'),
                                employee_lastname = F('employee__last_name'),
                                employee_personelcode = F('employee__personel_code'),
                                meal_name = F('restaurant_day_meal__restaurant_meal__name'),
                                ).values(
                                'employee_firstname', 'employee_lastname', 'employee_personelcode', 'meal_name').order_by('meal_name')

            serializer = Restaurant_Report_MealsDailyListSerializer(data=result, many=True)
            return Response(serializer.data)                   
        except Exception as e:
            return Response(e)   
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_sectionName(request, employeeId):
        try:
            departmentId = Employee.objects.get(pk=employeeId).department_id
            projectId = Employee.objects.get(pk=employeeId).project_id

            if(projectId == None):
                section_name = Department.objects.get(pk=departmentId).name
            elif(departmentId == None):
                section_name = Project.objects.get(pk=projectId).name

            return Response(section_name)                   
        except Exception as e:
            return Response(e)   
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_sectionDayMealsStatistics(request, employeeId):
        currentdate = date.today()

        emp = Employee.objects.get(pk=employeeId)
        department_id = emp.department
        project_id = emp.project

        results = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__date__exact=currentdate,  
            employee__department__exact=department_id, employee__project__exact=project_id).values(
            'employee__department').order_by('employee__department__name').annotate(
            section=F('employee__department__name'), 
            meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
            meal_no=Count('restaurant_day_meal__restaurant_meal__name')).values(
            'section', 'meal_name', 'meal_no')
        serializer = Restaurant_Report_SectionsDayMealsStatisticsSerializer(data=results, many=True)
        return Response(serializer.data) 

# -------------- CurrentMonthSelectedMeal report ----------------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_currentMonthSelectedMeal(request, employee_id):
        currentdate = date.today()
        startdate,_ = getCurrentMonthRangePro(currentdate)

        result = Restaurant_Employee_Day_Meal.objects.filter( 
            employee=employee_id, restaurant_day_meal__date__gte=startdate
            ).order_by('-restaurant_day_meal__date').values('restaurant_day_meal__date', 
            'restaurant_day_meal__restaurant_meal__name')[::-1]
        serializer = Restaurant_Report_MealsDailyListSerializer(data=result)
        return Response(serializer.data)

# --------------- asftDayMealsStatistics report -----------------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_asftDayMealsStatistics(request, date):
        results1 = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__date__exact=date, 
                employee__department__company__name__exact='آسفالت طوس').exclude(
                employee__department__exact=None).values('employee__department').annotate(
                _id=F('restaurant_day_meal__id'),                    
                section=F('employee__department__name'), 
                meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
                meal_no=Count('restaurant_day_meal__restaurant_meal__name'),
                section_type=Value(1, output_field=SmallIntegerField())).values('_id', 'section_type', 'section', 'meal_name', 'meal_no')

        results2 = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__date__exact=date).exclude(
                employee__project__exact=None).values('employee__project').annotate(
                _id=F('restaurant_day_meal__id'),
                section=F('employee__project__name'), 
                meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
                meal_no=Count('restaurant_day_meal__restaurant_meal__name'),
                section_type=Value(2, output_field=SmallIntegerField())).values('_id', 'section_type', 'section', 'meal_name', 'meal_no')

        results = results1.union(results2).order_by('section_type', 'section', 'meal_name', '_id')
        serializer = Restaurant_Report_DayMealsStatisticsSerializer(results, many=True)
        return Response(serializer.data)

# ------------- CompaniesDayMealsStatistics report --------------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_companiesDayMealsStatistics(request, date):
        results = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__date__exact=date).exclude(
            employee__department__company__name__exact='آسفالت طوس').exclude(employee__department__exact=None).values(
                'employee__department').order_by('employee__department__name').annotate(
            section=F('employee__department__name'), 
            meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
            meal_no=Count('restaurant_day_meal__restaurant_meal__name')).values(
                'section', 'meal_name', 'meal_no').order_by('restaurant_day_meal__id')
        serializer = Restaurant_Report_SectionsDayMealsStatisticsSerializer(data=results, many=True)
        return Response(serializer.data)        

# ----------- ContractorMonthlyMealsStatistics report -----------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_contractorMonthlyMealsStatistics(request):
        currentdate = date.today()
        startdate,_ = getCurrentMonthRangePro(currentdate)

        results = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__date__gte=startdate).exclude(
            Q(restaurant_day_meal__restaurant_meal__name__exact='عدم انتخاب') |
            Q(restaurant_day_meal__restaurant_meal__name__exact='عدم حضور')).values(
            'restaurant_day_meal__restaurant_meal').order_by('restaurant_day_meal__date', 'restaurant_day_meal__restaurant_meal__name').annotate(
                date=F('restaurant_day_meal__date'), 
                meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
                total_no=F('restaurant_day_meal__totalNo'),
                meal_no=Count('restaurant_day_meal__restaurant_meal__name')).values('date', 'meal_name', 'total_no', 'meal_no').order_by('date', 'restaurant_day_meal__id')
        serializer = Restaurant_Report_ContractorMonthlyMealsStatisticsSerializer(data=results, many=True)
        return Response(serializer.data)                   

# ------------ ControlMonthlyMealsStatistics report -------------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_controlMonthlyMealsStatistics(self, request, *args, **kwargs):
        currentdate = date.today()
        startdate,_ = getCurrentMonthRangePro(currentdate)

        results = Restaurant_Employee_Day_Meal.objects.filter(
            restaurant_day_meal__date__gte=startdate, 
            restaurant_day_meal__date__lte=currentdate,
            served__exact=1).exclude(
            Q(restaurant_day_meal__restaurant_meal__name__exact='عدم انتخاب') |
            Q(restaurant_day_meal__restaurant_meal__name__exact='عدم حضور')).values(
            'restaurant_day_meal__restaurant_meal').order_by('restaurant_day_meal__date', 'restaurant_day_meal__restaurant_meal__name').annotate(
                date=F('restaurant_day_meal__date'), 
                meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
                meal_no=Count('restaurant_day_meal__restaurant_meal__name'),
                served_no=Count('served', filter=Q(served=True)),
                total_no=F('restaurant_day_meal__totalNo')).values('date', 'meal_name', 'meal_no', 'served_no', 'total_no')
        serializer = Restaurant_Report_ControlMonthlyMealsStatisticsSerializer(data=results, many=True)
        return Response(serializer.data)                   
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_mealsStatisticsDatesList(request):
        currentdate = date.today()
        startdate,_ = getCurrentMonthRangePro(currentdate)

        results = Restaurant_Employee_Day_Meal.objects.filter(restaurant_day_meal__date__gte=startdate).values(
            'restaurant_day_meal__date').annotate(
                date=F('restaurant_day_meal__date')
                # ,date_no=Count('restaurant_day_meal__date')
                ).values('date').order_by('restaurant_day_meal__date')

        return Response(results)  

# -------- ContractorDailySectionMealsStatistics report ---------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_contractorDailySectionMealsStatistics(request):
        currentdate = date.today()    

        result1 = Restaurant_Employee_Day_Meal.objects.filter(
            restaurant_day_meal__date__exact=currentdate).exclude(
            employee__department__exact=None).filter( 
            employee__department__company__name__exact='آسفالت طوس').exclude( 
            restaurant_day_meal__restaurant_meal__name__in=('عدم حضور', 'عدم انتخاب')).values(
            'employee__department__name',
            'restaurant_day_meal__restaurant_meal__name')
        pivot_table1 = pivot(result1, 
                            'employee__department__name', 
                            'restaurant_day_meal__restaurant_meal__name', 
                            'employee__department__name', 
                            aggregation=Count)

        result2 = Restaurant_Employee_Day_Meal.objects.filter(
            restaurant_day_meal__date__exact=currentdate,
            employee__project__company__name__exact='آسفالت طوس').exclude(    
            employee__project__exact=None).exclude(
            restaurant_day_meal__restaurant_meal__name__in=('عدم حضور', 'عدم انتخاب')).values(
            'employee__project__name',
            'restaurant_day_meal__restaurant_meal__name')
        pivot_table2 = pivot(result2, 
                            'employee__project__name', 
                            'restaurant_day_meal__restaurant_meal__name', 
                            'employee__project__name', 
                            aggregation=Count)

        result3 = Restaurant_Employee_Day_Meal.objects.filter(
            restaurant_day_meal__date__exact=currentdate).exclude(
            employee__department__exact=None).exclude(
            employee__department__company__name__exact='آسفالت طوس').exclude(
            restaurant_day_meal__restaurant_meal__name__in=('عدم حضور', 'عدم انتخاب')).values(
            'employee__department__name',
            'restaurant_day_meal__restaurant_meal__name')
        pivot_table3 = pivot(result3, 
                            'employee__department__name', 
                            'restaurant_day_meal__restaurant_meal__name', 
                            'employee__department__name', 
                            aggregation=Count)

        result = pivot_table1.union(pivot_table2).union(pivot_table3)
        return Response(result)
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_todayMealsNames(request):
        try:
            currentdate = date.today() 

            result = Restaurant_Day_Meal.objects.filter(date__exact=currentdate).exclude(
                restaurant_meal__name__in=('عدم انتخاب', 'عدم حضور')).values('restaurant_meal__name').order_by('restaurant_meal__name')   

            return Response(result)
        except Exception as e:
            return Response('error: ', e)   
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_todayMealsTotalNo(request):
        try:
            currentdate = date.today()

            result = Restaurant_Employee_Day_Meal.objects.filter(
                restaurant_day_meal__date__exact=currentdate).exclude( 
                restaurant_day_meal__restaurant_meal__name__in=('عدم حضور', 'عدم انتخاب')).values(
                'restaurant_day_meal__restaurant_meal__name').annotate(
                meal_name=F('restaurant_day_meal__restaurant_meal__name'), 
                meal_no=Count('restaurant_day_meal__restaurant_meal__name')).values(
                'meal_name', 'meal_no')

            serializer = ContractorDailySectionMealsStatisticsTotalNoSerializer(data=result, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return Response('error: ', ex)   

# -------- PersonalsWhoDidNotSelectMeals report ---------
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_personalsWhoDidNotSelectMeals(request, isCurrentMonth):
        try:
            currentdate = date.today()
            startdate, enddate = getCurrentMonthRangePro(currentdate) if(isCurrentMonth == 1) else getNextMonthRange(currentdate)

            tmp1 = Restaurant_Employee_Day_Meal.objects.filter(
                restaurant_day_meal__date__gte=startdate, 
                restaurant_day_meal__date__lte=enddate).exclude(
                employee__department__exact=None).exclude(
                employee__department__exact=18).values('employee').annotate(
                selectedNo=Count('employee'),
                id=F('employee__id')).values_list('id')

            result1 = Employee.objects.filter(is_active__exact=1).exclude(
                department__exact=None).exclude(
                department__exact=18).exclude(
                id__in=tmp1).exclude(
                id__in=(1, 1689, 1471, 1616)).annotate(
                section=F('department__name')).values(
                'id', 'first_name', 'last_name', 'phone', 'section')
            
            tmp2 = Restaurant_Employee_Day_Meal.objects.filter(
                restaurant_day_meal__date__gte=startdate, 
                restaurant_day_meal__date__lte=enddate).exclude(
                employee__project__exact=None).values('employee').annotate(
                selectedNo=Count('employee'),
                id=F('employee__id')).values_list('id')

            result2 = Employee.objects.filter(is_active__exact=1).exclude(
                project__exact=None).exclude(
                id__in=tmp2).annotate(
                section=F('project__name')).values(
                'id', 'first_name', 'last_name', 'phone', 'section')

            result = result1.union(result2).order_by('section')

            serializer = PersonalsWhoDidNotSelectMealsSerializer(data=result, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response('error: ', e)   
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def get_sectionNames(request):
        try:
            result = Department.objects.exclude(id__exact=18).values('name')
            result1 = Project.objects.values('name')
            result = result.union(result1)

            return Response(result)
        except Exception as ex:
            return Response('error: ', ex)
# report api ++++++++++++++++++++++++++++++++++++++++++++++++++++


