#######################-Creation of tables-################################
import sqlite3
import os
import pickle

print("Some Problem Occur...")
print("Repairing Database...")


# try:

os.remove("global_variables.pkl")
os.remove("shaurya_database.db")
#######-run only once-######
global_vars = {}
pkl_obj = open("global_variables.pkl","wb")
pickle.dump(global_vars,pkl_obj)
pkl_obj.close()

db_instance = sqlite3.connect("shaurya_database.db")
cur_obj = db_instance.cursor()

cur_obj.execute("create table alarms(alarm_name varchar(20), status varchar(3) CHECK(status = 'on' OR status = 'off' ), time text, daylight varchar(2) CHECK(daylight = 'AM' OR daylight = 'PM' ), date text, state text CHECK(state = 'running' OR state = 'stop'));")

cur_obj.execute("create table device_control(device_name text, status text CHECK(status = 'on' or status = 'off'));")
cur_obj.execute("insert into device_control values('mic', 'on')")
cur_obj.execute("insert into device_control values('terminate', 'off')")

cur_obj.execute("create table mails(mail_id varchar unique, password text);")


cur_obj.close()
db_instance.commit()
db_instance.close()

# except:
#     print("repair function failed to exeecute")

print("Database Repaired...")
