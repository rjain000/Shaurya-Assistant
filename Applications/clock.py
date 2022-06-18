import time
from datetime import datetime, date
import sqlite3
#################################-GLOBAL VARIABLES/FUNCTIONS-###################

#######################################-FUNCTIONS-##############################
def day_of_week():
    days={0:"Mon", 1:"Tues",2:"Wed", 3:"Thur",4:"Fri", 5:"Sat",6:"Sun"}
    present_date = date.today()
    day_of_week = present_date.weekday()
    return days[day_of_week]


def check_terminate():
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()
    cur_obj.execute("select status from device_control where device_name = 'terminate'; ")
    value = cur_obj.fetchone()
    value = value[0]
    cur_obj.close()
    instance.commit()
    instance.close()
    return value
  

def real_time(time_label=None, fetchone=False):
    status_return = True
    while status_return:
        try:
            real_time = time.strftime("%I:%M %p")
            if fetchone == True:
                return real_time
            time_label.config(text = real_time)
            time.sleep(1)
        except:
            pass
        finally:
            if check_terminate() == "on":
                print("time function end")
                status_return = False 
                return ""


def real_date(date_label=None, fetchone = False):
    status_return = True
    while status_return:
        try:
            day = day_of_week()
            date = datetime.now()
            present_date = date.strftime(f"%d/%m/%y {day}")
            if fetchone == True:
                return present_date
            date_label.config(text=present_date)
            time.sleep(3)
        except:
            pass
        finally:
            if check_terminate() == "on":
                print("date function end")
                status_return = False
                return ""


def actual_date():
    date = datetime.now()
    present_date = date.strftime(f"%d/%m/{date.year}")
    return present_date

def actual_time():
    return real_time(fetchone= True)

def fetch_time():
    return real_time(fetchone= True)

def fetch_date():
    return real_date(fetchone= True)

def fetch_hour():
    hour = time.strftime("%I")
    return hour

def fetch_min():
    min = time.strftime("%M")
    return min

def fetch_day():
    date = datetime.now()
    present_day = date.strftime(f"%d")
    return present_day

def fetch_month():
    date = datetime.now()
    present_month = date.strftime(f"%m")
    return present_month

def fetch_year():
    todays_date = date.today()
    year= todays_date.year
    return year