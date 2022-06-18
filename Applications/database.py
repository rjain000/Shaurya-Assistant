###############################-PRE DEFINED MODULES-###################################
import sqlite3
import os
###############################-USER DEFINED MODULES-###################################
from datetime import date, datetime
###############################-GLOBAL VARIABLES-###################################

###############################-USER DEFINED FUNCTIONS-###################################
def set_alarm(datetime):
    """store alarm in database"""
    #datetime[0]        ->alarm name
    #datetime[1]        ->time
    #datetime[2]        ->daylight mode
    #datetime[3]        ->date

    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()
    try:
        cur_obj.execute(f"insert into alarms values (\'{datetime[0]}\', 'on', \'{datetime[1]}\', \'{datetime[2]}\', \'{datetime[3]}\', 'stop');")
        cur_obj.close()
        instance.commit()
        instance.close()
    except:
        print("alarm not saved")



def sort_alarm(result):
    def convert24(str1):
        # Checking if last two elements of time
        # is AM and first two elements are 12
        if str1[-2:] == "AM" and str1[:2] == "12":
            return "00" + str1[2:-2]

        # remove the AM    
        elif str1[-2:] == "AM":
            return str1[:-2]

        # Checking if last two elements of time
        # is PM and first two elements are 12   
        elif str1[-2:] == "PM" and str1[:2] == "12":
            return str1[:-2]

        else:

            # add 12 to hours and remove PM
            return str(int(str1[:2]) + 12) + str1[2:8]


    today = date.today()
    today_date = today.strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%H:%M")


    # result = fetch_alarms()
    today_alarm = []
    # time_of_alarm_today = []

    if(result!=None):

        for item in result:
            if item[4]<today_date:
                delete_alarm_record(alarm_name=item[0], time=item[2], daylight=item[3], date=item[4])
            elif item[4] == today_date:
                time12 = f"{item[2]}:00 {item[3]}"
                time24 = convert24(time12)
                if time24<now_time:
                    delete_alarm_record(alarm_name=item[0], time=item[2], daylight=item[3], date=item[4])
                else:
                    today_alarm.append(list(item))


        # today_alarm.sort(key=lambda y : y[3]) #not required

        AM_List = []
        PM_List = []

        for time in today_alarm:
            if time[3] == "AM":
                AM_List.append(time)
            else:
                PM_List.append(time)

        AM_List.sort(key=lambda y : y[2])
        PM_List.sort(key=lambda y : y[2])

        today_alarm = AM_List + PM_List
        return today_alarm
 



def fetch_alarms(alarm_name=None, status=None,time=None, daylight=None, date=None, operation = "and", state = None):
    """fetch all alarm timings in a list of tuples"""
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()

    Parameter_list = [
         ["alarm_name = ",alarm_name],
         ["status = ",status], 
         ["time = ",time], 
         ["daylight = ",daylight], 
         ["date = ",date],
         ["state = ",state]
     ]

    string_conditions=[]
    conditions = []
    for values in Parameter_list:
         if None not in values:
             values[1] = f"\'{values[1]}\'"
             string = " ".join(values)
             string_conditions.append(string)

    if string_conditions!=[]:
        if operation == "and":
            conditions = " and ".join(string_conditions)
        elif operation == "or":
            conditions = " or ".join(string_conditions)
        else:
            print(f"no operation as {operation}")
            print("doing 'and' operation")

    try:
        if conditions!=[]:
            cur_obj.execute(f"select * from alarms where {conditions} ;")
        else:
            cur_obj.execute("select * from alarms;")

        values = cur_obj.fetchall()

    except:
        print("function call mai dikat hai bhai")

    cur_obj.close()
    instance.commit()
    instance.close()


    if values == []:
        return None

    elif len(values) == 1:
        return values
        
    else:
        ordered_values = sort_alarm(values)
        return ordered_values
        

def delete_alarm_record(alarm_name=None, status=None,time=None, daylight=None, date=None, operation = "and", state=None):
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()

    Parameter_list = [
         ["alarm_name = ",alarm_name],
         ["status = ",status], 
         ["time = ",time], 
         ["daylight = ",daylight], 
         ["date = ",date],
         ["state = ",state]
     ]

    string_conditions=[]
    conditions = []
    for values in Parameter_list:
         if None not in values:
             values[1] = f"\'{values[1]}\'"
             string = " ".join(values)
             string_conditions.append(string)

    if string_conditions!=[]:
        if operation == "and":
            conditions = " and ".join(string_conditions)
        elif operation == "or":
            conditions = " or ".join(string_conditions)
        else:
            print(f"no operation as {operation}")
            print("doing 'and' operation")

    try:
        if conditions!=[]:
            print(f"delete from alarms where {conditions} ;")
            cur_obj.execute(f"delete from alarms where {conditions} ;")
        else:
            print("alarm not found to delete")
            return ""

        print("Alarm deleted")
    except:
        print("function call mai dikat hai bhai")

    cur_obj.close()
    instance.commit()
    instance.close()
    

def change_alarm_status(set_state, alarm_name=None, status=None,time=None, daylight=None, date=None, operation = "and", state = None):
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()

    Parameter_list = [
         ["alarm_name = ",alarm_name],
         ["status = ",status], 
         ["time = ",time], 
         ["daylight = ",daylight], 
         ["date = ",date],
         ["state = ",state]
     ]

    string_conditions=[]
    conditions = []
    for values in Parameter_list:
         if None not in values:
             values[1] = f"\'{values[1]}\'"
             string = " ".join(values)
             string_conditions.append(string)

    if string_conditions!=[]:
        if operation == "and":
            conditions = " and ".join(string_conditions)
        elif operation == "or":
            conditions = " or ".join(string_conditions)
        else:
            print(f"no operation as {operation}")
            print("doing 'and' operation")

    try:
        if conditions!=[]:
            cur_obj.execute(f"update alarms set state = \'{set_state}\' where {conditions} ;")
        else:
            print("no alarms to change its state")
            return ""

        print("Alarm state changed")
    except:
        print("function call mai dikat hai bhai")

    cur_obj.close()
    instance.commit()
    instance.close()


def get_first_alarm():
    alarms = fetch_alarms()
    if alarms !=None:
        return alarms[0]
    else:
        return None



def fetch_device_status(device_name):
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()

    try:
        cur_obj.execute(f"select status from device_control where device_name = \'{device_name}\';")
    except:
        print("Error occur at database.py >> fetch_device_status()")
        os.startfile(r""+os.getcwd()+"\\repair.py")
        return ""

    status = cur_obj.fetchone()
    
    cur_obj.close()
    instance.commit()
    instance.close()
    return status[0]


def set_device_status(device_name, status):
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()

    try:
        cur_obj.execute(f"update device_control set status = \'{status}\' where device_name = \'{device_name}\';")
    except:
        print("Error occur at database.py >> set_device_status()")
        os.startfile(r""+os.getcwd()+"\\repair.py")
        return ""
    
    cur_obj.close()
    instance.commit()
    instance.close()


def fetch_mail(mail_id):
    """return mail id or none to check if mails is available or not"""
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()
    cur_obj.execute(f"select mail_id from mails where mail_id = \'{mail_id}\';")
    mail_val = cur_obj.fetchone()
    cur_obj.close()
    instance.commit()
    instance.close()
    return mail_val

def add_mail(mail_id, password):
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()
    value = fetch_mail(mail_id)
    if value==None:
        cur_obj.execute(f"insert into mails values(\'{mail_id}\', \'{password}\');")
    else:
        cur_obj.execute(f"update mails set password = \'{password}\'where mail_id = \'{mail_id}\';")

    cur_obj.close()
    instance.commit()
    instance.close()

def get_mail_credentials(mail_id):
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()
    cur_obj.execute(f"select * from mails where mail_id = \'{mail_id}\';")
    credentials = cur_obj.fetchone()
    cur_obj.close()
    instance.commit()
    instance.close()
    return credentials

def get_mails():
    instance = sqlite3.connect("shaurya_database.db")
    cur_obj = instance.cursor()
    cur_obj.execute(f"select * from mails;")
    credentials = cur_obj.fetchall()
    cur_obj.close()
    instance.commit()
    instance.close()
    if len(credentials)<1:
        return None
    return credentials


