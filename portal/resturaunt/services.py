from datetime import date, datetime ,timedelta


def getCurrentMonthRange(date):
    currentdate = datetime.strptime(date, '%Y-%m-%d').date()

    y = currentdate.year if(currentdate.month != 1) else currentdate.year - 1
    m = currentdate.month - 1 if(currentdate.month != 1) else 12
    d = currentdate.day 
    startdate = ""
    enddate = ""
    if(m == 1):
        startdate += str(y) 
        startdate += "-01" if (d < 21) else "-02" 
        startdate += "-21" if (d < 21) else "-20"
        enddate += str(y) 
        enddate += "-02" if (d < 21) else "-03" 
        enddate += "-19" if (d < 21) else "-20"
    elif(m == 2):
        startdate += str(y) 
        startdate += "-02" if (d < 20) else "-03" 
        startdate += "-20" if (d < 20) else "-21"
        enddate += str(y) 
        enddate += "-03" if (d < 20) else "-04" 
        enddate += "-20" if (d < 20) else "-20"
    elif(m == 3):
        startdate += str(y) 
        startdate += "-03" if (d < 21) else "-04" 
        startdate += "-21" if (d < 21) else "-21"
        enddate += str(y) 
        enddate += "-04" if (d < 21) else "-05" 
        enddate += "-21" if (d < 21) else "-21"
    elif(m == 4):
        startdate += str(y) 
        startdate += "-04" if (d < 21) else "-05" 
        startdate += "-21" if (d < 21) else "-22"
        enddate += str(y) 
        enddate += "-05" if (d < 21) else "-06" 
        enddate += "-21" if (d < 21) else "-21"            
    elif(m == 5):
        startdate += str(y) 
        startdate += "-05" if (d < 22) else "-06" 
        startdate += "-22" if (d < 22) else "-22" 
        enddate += str(y) 
        enddate += "-06" if (d < 22) else "-07" 
        enddate += "-21" if (d < 22) else "-22"            
    elif(m == 6):
        startdate += str(y) 
        startdate += "-06" if (d < 22) else "-07" 
        startdate += "-22" if (d < 22) else "-23" 
        enddate += str(y) 
        enddate += "-07" if (d < 22) else "-08" 
        enddate += "-22" if (d < 22) else "-22"            
    elif(m == 7):
        startdate += str(y) 
        startdate += "-07" if (d < 23) else "-08" 
        startdate += "-23" if (d < 23) else "-23" 
        enddate += str(y) 
        enddate += "-08" if (d < 23) else "-09" 
        enddate += "-22" if (d < 23) else "-22"            
    elif(m == 8):
        startdate += str(y) 
        startdate += "-08" if (d < 23) else "-09" 
        startdate += "-23" if (d < 23) else "-23" 
        enddate += str(y) 
        enddate += "-09" if (d < 23) else "-10" 
        enddate += "-22" if (d < 23) else "-22"
    elif(m == 9):
        startdate = str(y) 
        startdate += "-09" if (d < 23) else "-10" 
        startdate += "-23" if (d < 23) else "-23" 
        enddate += str(y) 
        enddate += "-10" if (d < 23) else "-11" 
        enddate += "-22" if (d < 23) else "-21"            
    elif(m == 10):
        startdate += str(y) 
        startdate += "-10" if (d < 23) else "-11" 
        startdate += "-23" if (d < 23) else "-22" 
        enddate += str(y) 
        enddate += "-11" if (d < 23) else "-12" 
        enddate += "-21" if (d < 23) else "-21"            
    elif(m == 11):
        startdate += str(y) 
        startdate += "-11" if (d < 22) else "-12" 
        startdate += "-22" if (d < 22) else "-22" 
        enddate += str(y) 
        enddate += "-12" if (d < 22) else "-01" 
        enddate += "-21" if (d < 22) else "-20"
    elif(m == 12):
        startdate += str(y) 
        startdate += "-12" if (d < 22) else "-01" 
        startdate += "-22" if (d < 22) else "-21"
        enddate += str(y) 
        enddate += "-01" if (d < 22) else "-02" 
        enddate += "-20" if (d < 22) else "-19"             
    return {startdate, enddate}

def getCurrentMonthRangeEx(date):
    currentdate = datetime.strptime(date, '%Y-%m-%d').date()
    y = currentdate.year 
    m = currentdate.month
    d = currentdate.day

    startdate = ""
    enddate = ""
    if(m == 1):
        startdate += str(y - 1) 
        startdate += "-12-22" 
        enddate += str(y) 
        enddate += "-01-20" 
    elif(m == 2):
        startdate += str(y) 
        startdate += "-01-21"
        enddate += str(y) 
        enddate += "-02-19"
    elif(m == 3):
        startdate += str(y) 
        startdate += "-02-20"
        enddate += str(y) 
        enddate += "-03-20"
    elif(m == 4):
        startdate += str(y) 
        startdate += "-03-21"
        enddate += str(y) 
        enddate += "-04-20"          
    elif(m == 5):
        startdate += str(y) 
        startdate += "-04-21"  
        enddate += str(y) 
        enddate += "-05-21"             
    elif(m == 6):
        startdate += str(y) 
        startdate += "-05-22"  
        enddate += str(y) 
        enddate += "-06-21"             
    elif(m == 7):
        startdate += str(y) 
        startdate += "-06-22"  
        enddate += str(y) 
        enddate += "-07-22"             
    elif(m == 8):
        startdate += str(y) 
        startdate += "-07-23"  
        enddate += str(y) 
        enddate += "-08-22" 
    elif(m == 9):
        startdate = str(y) 
        startdate += "-08-23"  
        enddate += str(y) 
        enddate += "-09-22"             
    elif(m == 10):
        startdate += str(y) 
        startdate += "-09-23"  
        enddate += str(y) 
        enddate += "-10-22"             
    elif(m == 11):
        startdate += str(y) 
        startdate += "-10-23"  
        enddate += str(y) 
        enddate += "-11-21" 
    elif(m == 12):
        startdate += str(y) 
        startdate += "-11-22" 
        enddate += str(y) 
        enddate += "-12-21"    
    return {startdate, enddate}

def getCurrentMonthRangePro(date):
    currentdate = datetime.strptime(date, '%Y-%m-%d').date()

    y = currentdate.year
    m = currentdate.month
    d = currentdate.day
    startdate = ""
    enddate = ""
    if(m == 1):
        startdate += str(y-1) if (d < 21) else str(y)  
        startdate += "-12" if (d < 21) else "-01" 
        startdate += "-22" if (d < 21) else "-21"
        
        enddate += str(y)  
        enddate += "-01" if (d < 21) else "-02" 
        enddate += "-20" if (d < 21) else "-19"
    elif(m == 2):
        startdate += str(y) 
        startdate += "-01" if (d < 20) else "-02" 
        startdate += "-21" if (d < 20) else "-20"
            
        enddate += str(y)  
        enddate += "-02" if (d < 20) else "-03" 
        enddate += "-19" if (d < 20) else "-20"
    elif(m == 3):
        startdate += str(y) 
        startdate += "-02" if (d < 21) else "-03" 
        startdate += "-20" if (d < 21) else "-21"
            
        enddate += str(y)  
        enddate += "-03" if (d < 21) else "-04" 
        enddate += "-20" if (d < 21) else "-20"
    elif(m == 4):
        startdate += str(y) 
        startdate += "-03" if (d < 21) else "-04" 
        startdate += "-21" if (d < 21) else "-21"
            
        enddate += str(y)  
        enddate += "-04" if (d < 21) else "-05" 
        enddate += "-20" if (d < 21) else "-21"
    elif(m == 5):
        startdate += str(y) 
        startdate += "-04" if (d < 22) else "-05" 
        startdate += "-21" if (d < 22) else "-22" 
            
        enddate += str(y)  
        enddate += "-05" if (d < 22) else "-06" 
        enddate += "-21" if (d < 22) else "-21"
    elif(m == 6):
        startdate += str(y) 
        startdate += "-05" if (d < 22) else "-06" 
        startdate += "-22" if (d < 22) else "-22" 
            
        enddate += str(y)  
        enddate += "-06" if (d < 22) else "-06" 
        enddate += "-21" if (d < 22) else "-22"
    elif(m == 7):
        startdate += str(y) 
        startdate += "-06" if (d < 23) else "-07" 
        startdate += "-23" if (d < 23) else "-23" 
            
        enddate += str(y)  
        enddate += "-07" if (d < 23) else "-08" 
        enddate += "-22" if (d < 23) else "-22"
    elif(m == 8):
        startdate += str(y) 
        startdate += "-07" if (d < 23) else "-08" 
        startdate += "-23" if (d < 23) else "-23" 
            
        enddate += str(y)  
        enddate += "-08" if (d < 23) else "-09" 
        enddate += "-22" if (d < 23) else "-22"
    elif(m == 9):
        startdate = str(y) 
        startdate += "-08" if (d < 23) else "-09" 
        startdate += "-23" if (d < 23) else "-23" 
            
        enddate += str(y)  
        enddate += "-09" if (d < 23) else "-10" 
        enddate += "-22" if (d < 23) else "-22"
    elif(m == 10):
        startdate += str(y) 
        startdate += "-09" if (d < 23) else "-10" 
        startdate += "-23" if (d < 23) else "-23" 
            
        enddate += str(y)  
        enddate += "-10" if (d < 23) else "-11" 
        enddate += "-22" if (d < 23) else "-21"
    elif(m == 11):
        startdate += str(y) 
        startdate += "-10" if (d < 22) else "-11" 
        startdate += "-23" if (d < 22) else "-22" 
            
        enddate += str(y)  
        enddate += "-11" if (d < 22) else "-12" 
        enddate += "-21" if (d < 22) else "-21"
    elif(m == 12):
        startdate += str(y) 
        startdate += "-11" if (d < 22) else "-12" 
        startdate += "-22" if (d < 22) else "-22" 
            
        enddate += str(y) if (d < 22) else str(y+1)
        enddate += "-12" if (d < 22) else "-01" 
        enddate += "-21" if (d < 22) else "-20"
    return {startdate, enddate}

def getNextMonthRange(date):
    currentdate = datetime.strptime(date, '%Y-%m-%d').date()

    y = currentdate.year
    m = currentdate.month
    d = currentdate.day
    startdate = ""
    enddate = ""
    if(m == 1):
        startdate += str(y)
        startdate += "-01" if (d < 21) else "-02" 
        startdate += "-21" if (d < 21) else "-20"
        enddate += str(y) 
        enddate += "-02" if (d < 21) else "-03" 
        enddate += "-19" if (d < 21) else "-20"
    elif(m == 2):
        startdate += str(y) 
        startdate += "-02" if (d < 20) else "-03" 
        startdate += "-20" if (d < 20) else "-21"
        enddate += str(y) 
        enddate += "-03" if (d < 20) else "-04" 
        enddate += "-20" if (d < 20) else "-20"
    elif(m == 3):
        startdate += str(y) 
        startdate += "-03" if (d < 21) else "-04" 
        startdate += "-21" if (d < 21) else "-21"
        enddate += str(y) 
        enddate += "-04" if (d < 21) else "-05" 
        enddate += "-21" if (d < 21) else "-21"
    elif(m == 4):
        startdate += str(y) 
        startdate += "-04" if (d < 21) else "-05" 
        startdate += "-21" if (d < 21) else "-22"
        enddate += str(y) 
        enddate += "-05" if (d < 21) else "-06" 
        enddate += "-21" if (d < 21) else "-21"            
    elif(m == 5):
        startdate += str(y) 
        startdate += "-05" if (d < 22) else "-06" 
        startdate += "-22" if (d < 22) else "-22" 
        enddate += str(y) 
        enddate += "-06" if (d < 22) else "-07" 
        enddate += "-21" if (d < 22) else "-22"            
    elif(m == 6):
        startdate += str(y) 
        startdate += "-06" if (d < 22) else "-07" 
        startdate += "-22" if (d < 22) else "-23" 
        enddate += str(y) 
        enddate += "-07" if (d < 22) else "-08" 
        enddate += "-22" if (d < 22) else "-22"            
    elif(m == 7):
        startdate += str(y) 
        startdate += "-07" if (d < 23) else "-08" 
        startdate += "-23" if (d < 23) else "-23" 
        enddate += str(y) 
        enddate += "-08" if (d < 23) else "-09" 
        enddate += "-22" if (d < 23) else "-22"            
    elif(m == 8):
        startdate += str(y) 
        startdate += "-08" if (d < 23) else "-09" 
        startdate += "-23" if (d < 23) else "-23" 
        enddate += str(y) 
        enddate += "-09" if (d < 23) else "-10" 
        enddate += "-22" if (d < 23) else "-22"
    elif(m == 9):
        startdate = str(y) 
        startdate += "-09" if (d < 23) else "-10" 
        startdate += "-23" if (d < 23) else "-23" 
        enddate += str(y) 
        enddate += "-10" if (d < 23) else "-11" 
        enddate += "-22" if (d < 23) else "-21"            
    elif(m == 10):
        startdate += str(y) 
        startdate += "-10" if (d < 23) else "-11" 
        startdate += "-23" if (d < 23) else "-22" 
        enddate += str(y) 
        enddate += "-11" if (d < 23) else "-12" 
        enddate += "-21" if (d < 23) else "-21"            
    elif(m == 11):
        startdate += str(y) 
        startdate += "-11" if (d < 22) else "-12" 
        startdate += "-22" if (d < 22) else "-22" 
        enddate += str(y) 
        enddate += "-12" if (d < 22) else "-01" 
        enddate += "-21" if (d < 22) else "-20"
    elif(m == 12):
        startdate += str(y) 
        startdate += "-12" if (d < 22) else "-01" 
        startdate += "-22" if (d < 22) else "-21"
        enddate += str(y) 
        enddate += "-01" if (d < 22) else "-02" 
        enddate += "-20" if (d < 22) else "-19"             
    return {startdate, enddate}


