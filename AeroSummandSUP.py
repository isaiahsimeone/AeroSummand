from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
import time
import datetime
import calendar

### Settings - only Mondays For Start/End Date ###
START_DATE  = "2017-01-16" 
END_DATE    = "2020-02-17"  
EMP_NAME    = ""
EMP_IDENT   = ""

WD_PATH     = "/usr/local/bin/chromedriver"

### Credentials ###
USERNAME    = ""
PASSWORD    = ""

shifts = []

### Initialise Webdriver ###
driver = webdriver.Chrome(WD_PATH)

#############################
###                 Functions
#############################

"""
Returns shifts for a specified week
Args:
    week {String}: The week to retrieve employee shifts for.
Returns:
    {Object}: A 2D array containing shift data 
"""
def getRoster(week):
    # Inject week value into 3rd index of dropdown
    driver.execute_script("document.getElementsByName('Week')[0][2].value = '" + str(week) + "';")
    # Select injected option
    driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[4]/select/option[3]")[0].click()
    # Select desired employee
    setEmployee()
    # Show roster for injected week and employee
    driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[5]/input")[0].click()

    rosterElem = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td/table")[0].get_attribute("innerHTML")
    soup = BeautifulSoup(rosterElem, 'html.parser')

    weekShifts = []

    for ROW in soup.find_all("tr", {'class' : 'dataTableRow'}):
        shift = []
        for CELL in ROW.find_all("td", {'class' : 'dataTableContent'}):
            shift.append(CELL.getText().replace("\t","").replace("\n",""))
        weekShifts.append(shift)
    weekShifts.pop(-1) # delete total hours row
    return weekShifts

"""
Returns the date of the same day next week in AeroNet suitable format.
Args:
    previousWeek {String}: The date of the previous week in AeroNet suitable format.
Returns:
    {String} : The date of the same day following the previousWeek (in suitable format)
"""       
def getNextWeek(previousWeek):
    day     = int(previousWeek[-2:])
    month   = int(previousWeek[5:7])
    year    = int(previousWeek[:4])

    # Is this year a leap year?
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        daysInFeb = 29
    else:
        daysInFeb = 28
        
    daysInMonth = [0, 31, daysInFeb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    daysInThisMonth = daysInMonth[month]
    if day + 7 > daysInThisMonth:
        remainder = (day + 7) - daysInThisMonth
        month += 1
        day = remainder
    else:
        day += 7

    if month > 12:
        month = 1
        year += 1
        
    monthString = str(month)
    dayString   = str(day)
    yearString  = str(year)
    
    # Put into format suitable for AeroNet
    if month < 10:
        monthString = "0" + str(month)

    if day < 10:
        dayString   = "0" + str(day)

    return str(yearString + "-" + monthString + "-" + dayString)

"""
Selects the employee specified in the EMP_IDENT field and manipulates the DOM accordingly
"""
def setEmployee():
    # Set 2nd index to value of EMP_IDENT
    driver.execute_script("document.getElementsByName('emp')[0][1].value = '" + EMP_IDENT + "';")
    # Select injected option for the employee (2nd index)
    driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/select/option[2]")[0].click()

"""
Returns the number of weeks between START_DATE and END_DATE
Returns:
    {Int} : number of weeks difference between START_DATE and END_DATE 
"""
def getWeekDelta():
    day1     = int(START_DATE[-2:])
    month1   = int(START_DATE[5:7])
    year1    = int(START_DATE[:4])

    day2     = int(END_DATE[-2:])
    month2   = int(END_DATE[5:7])
    year2    = int(END_DATE[:4])

    d1 = date(year1, month1, day1)
    d2 = date(year2, month2, day2)
    return (d2 - d1).days // 7

#############################
###                  Get Data
#############################

### Perform Login ###
driver.get("https://www.aerocare.com.au/AeroNet2/aeronet/auth/login/redirect/")
driver.find_element_by_id("username").send_keys(USERNAME)
driver.find_element_by_id("password").send_keys(PASSWORD)
driver.find_element_by_id("login").click()

### Open Roster Page ###
driver.get("https://www.aerocare.com.au/AeroNet/index.php?-module=Roster_employee")

### Get Roster Data ###
weekCount = getWeekDelta()
currentWeek = START_DATE
for i in range(0, weekCount):
    time.sleep(0.01)
    print(str(round((i+1)/weekCount * 100, 3)) + "% Complete")
    shifts += getRoster(currentWeek)
    currentWeek = getNextWeek(currentWeek)

#############################
###              Process Data
#############################

### Get Shift Area Types ###
observedShiftAreas = []

for i in range(0, len(shifts)):
    if shifts[i][5] not in observedShiftAreas:
        observedShiftAreas.append(shifts[i][5])

### Get Number of Shift Occurrences ###
shiftOccurrences = [0] * len(shifts)

for i in range(0, len(shifts)):
    index = observedShiftAreas.index(shifts[i][5])
    shiftOccurrences[index] += 1

### Get Total Time of Shift Occurrences ###
shiftTimings = [0] * len(shifts)

for i in range(0, len(shifts)):
    index = observedShiftAreas.index(shifts[i][5])
    if shifts[i][4] not in ["---"]:
        shiftTimings[index] += float(shifts[i][4])

#############################
###              Display Data
#############################  
print("\n" * 3)
print(EMP_NAME + " - "+ START_DATE + " to " + END_DATE)
print('{:>22}  {:>8}  {:>11}'.format("ROSTERED AREA", "OCCURRENCES", "TOT. HOURS"))
print("-" * 55)
for i in range(0, len(observedShiftAreas)):
    line_new = '{:>22}  {:>8}  {:>11}'.format(str(observedShiftAreas[i]), str(shiftOccurrences[i]), str(round(shiftTimings[i], 1)))
    print(line_new)
    
print("-"*55)
print('{:>22}  {:>8}  {:>10}'.format("", round(sum(shiftOccurrences), 1), round(sum(shiftTimings), 1)))