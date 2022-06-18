from tkinter import *
#############################-PRE DEFINED MODULES-####################
import sys
from tkinter import *
#############################-USER DEFINED MODULES-###################
from clock import *
from tkinter.font import Font
from database import *

############################-GLOBAL VARIABLES-########################
i=0
############################-FUNCTIONS CODE-##########################

def click_to_set(hour_value, min_value, day, month, year, alarm_name, switch_btn):
    alarm_hour = hour_value.get()
    alarm_min = min_value.get()
    
    alarm_day = day.get()
    alarm_month = month.get()
    alarm_year = year.get()

    alarmName= alarm_name.get()
    if alarmName == "" or alarmName == " ":
        alarmName = "Untitled"
    daylight_mode = switch_btn['text']
    time = f"{alarm_hour}:{alarm_min}"
    date= f"{alarm_day}/{alarm_month}/{alarm_year}"
    datetime = [alarmName,time, daylight_mode, date]
    
    print("Alarm set for ",[alarmName, time, daylight_mode, date])
    set_alarm(datetime) ##database module
    sys.exit()


def daytime(switch_btn):
    global i
    if i==0:
        switch_btn['text'] = "PM"
        i=1
    else:
        switch_btn['text'] = "AM"
        i=0

def latest_alarm(alarm_list):
    return alarm_list[0]

############################-PROGRAM CODE-###########################
class alarm:
    def __init__(self) -> None:
        self.alarm_interface = Tk()
        self.alarm_interface.title("Alarm")
        self.alarm_interface.config(background="white")
        self.alarm_interface.geometry("400x200+475+225")
        self.alarm_interface.resizable(0,0)
        self.alarm_interface.overrideredirect(True)
        #global variables
        self.hour_value = StringVar()
        self.min_value = StringVar()
        self.day = StringVar()
        self.month = StringVar()
        self.year = StringVar()
        self.alarm_name = StringVar()
        self.sec=600 #ten min for snooze
        
    def set_alarm_time(self):
        hour_value = self.hour_value
        min_value = self.min_value
        day = self.day
        month = self.month
        year = self.year
        alarm_name = self.alarm_name
        hour_options = ('01','02','03','04','05','06','07','08','09','10','11','12')
        min_options = ('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59')
        day_options = ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
        month_options = ('01','02','03','04','05','06','07','08','09','10','11','12')
        current_year= str(fetch_year())
        next_year= str(fetch_year()+1)
        n_year = str(fetch_year()+2)
        year_options = (current_year, next_year, n_year)

        #input font
        input_spinbox_font= Font(family = "RocknRoll One", size = 16, weight='bold')
        input_spinbox_font2= Font(family = "RocknRoll One", size = 14, weight='bold')
        input_label_font= Font(family = "RocknRoll One", size = 25, weight='normal')
        btn_font= Font(family = "RocknRoll One", size = 18, weight='normal')
        close_btn_font= Font(family = "RocknRoll One", size = 15, weight='normal')

        #head label
        head_label_font= Font(family = "RocknRoll One", size = 18, weight='bold')
        head_label = Label(self.alarm_interface, background="white", text = "Set Alarm", font = head_label_font, foreground="#043492")
        head_label.place(x=100, y=5, width=200, height=40)

        #img label
        alarmImg = PhotoImage(file="./images/label images/alarm/alarm.png")
        img_label = Label(self.alarm_interface, image=alarmImg, background="white")
        img_label.place(x=28, y=50, width=120, height=95)

        #hour label
        hour_spinbox = Spinbox(self.alarm_interface, textvariable= hour_value, values=hour_options, background="#016CCF", borderwidth=0, font = input_spinbox_font, foreground="white", relief=FLAT, justify=CENTER, wrap=True)
        
        hour_spinbox.place(x=175, y=63, width=55, height=40)

        #colon label
        colon_label = Label(self.alarm_interface, background="white", text = ":", font= input_label_font, fg="#016CCF")
        colon_label.place(x=235, y=63, width=15, height=40)

        #minutes label
        minutes_label = Spinbox(self.alarm_interface, textvariable= min_value, values=min_options, background="#016CCF", borderwidth=0, font = input_spinbox_font, foreground="white", relief=FLAT, justify=CENTER, wrap=True)
        minutes_label.place(x=255, y=63, width=55, height=40)

        #AM/PM button
        switch_btn = Button(self.alarm_interface, background="#016CCF", text="AM", command= lambda : daytime(switch_btn), font=btn_font, foreground= "white", relief=FLAT, borderwidth=0, activebackground="white", activeforeground="#016CCF")
        switch_btn.place(x=315, y=63, width=60, height=40)

        #day label
        day_label = Spinbox(self.alarm_interface, textvariable= day, values=day_options, background="#016CCF", borderwidth=0, font = input_spinbox_font2, foreground="white", relief=FLAT, justify=CENTER, wrap=True)
        day_label.place(x=175, y=110, width=60, height=40)

        #month label
        month_label = Spinbox(self.alarm_interface, textvariable= month, values=month_options, background="#016CCF", borderwidth=0, font = input_spinbox_font2, foreground="white", relief=FLAT, justify=CENTER, wrap=True)
        month_label.place(x=235, y=110, width=60, height=40)

        #year label
        year_label = Spinbox(self.alarm_interface, textvariable= year, values= year_options, background="#016CCF", borderwidth=0, font = input_spinbox_font2, foreground="white", relief=FLAT, justify=CENTER)
        year_label.place(x=295, y=110, width=80, height=40)

        #setting default values
        hour = fetch_hour()
        show_day = fetch_day()
        hour_index = hour_options.index(hour)

        if hour_index < len(hour_options)-1:
            next_hour=hour_options[hour_index+1]
        else:
            next_hour= hour_options[0]
        
        hour_value.set(next_hour)
        min_value.set(fetch_min())
        day.set(show_day)
        month.set(fetch_month())

        #alarm name
        alarm_name_input = Entry(self.alarm_interface, textvariable= alarm_name, background="#016CCF", foreground="white", font=btn_font, relief=FLAT, justify=CENTER)
        alarm_name_input.place(x=18, y=160, width=140, height=30)
        alarm_name.set("Untitled")
        alarm_name_input.bind("<FocusIn>", lambda e: alarm_name.set(""))

        #set button
        set_button = Button(self.alarm_interface, background="#016CCF", command= lambda: click_to_set(hour_value, min_value, day, month,year, alarm_name, switch_btn), text="SET", font=btn_font, fg="white", activebackground="white", activeforeground="#016CCF", borderwidth=0)
        set_button.place(x=220, y=160, width=100, height=30)

        #Cancel button
        set_button = Button(self.alarm_interface, background="#016CCF", command= self.alarm_interface.destroy, text="X", font=close_btn_font, fg="white", activebackground="white", activeforeground="#016CCF", borderwidth=0)
        set_button.place(x=350, y=5, width=50, height=30)
        mainloop()
    


############-class ends-###############

if __name__=="__main__":
    alarm().set_alarm_time()