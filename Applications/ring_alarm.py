#############################-PRE DEFINED MODULES-####################
from pygame import mixer
from tkinter import *
import time
from threading import Thread
#############################-USER DEFINED MODULES-###################
from clock import *
from tkinter.font import Font
from database import *

############################-GLOBAL VARIABLES-########################
i=0
count=1
############################-FUNCTIONS CODE-##########################

def latest_alarm(alarm_list):
    return alarm_list[0]

############################-PROGRAM CODE-###########################
class alarm:
    def __init__(self) -> None:
        #music interface
        mixer.init()
        mixer.music.load("./sounds/alarm/alarm.mp3")
        #interface
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
        
    def check_alarm_time(self):
        # alarm_imgs[0]       ->not active
        # alarm_imgs[1]       ->active

        # global count

        # if count>1:
        #     self.__init__
        
        print("check alarm time")
        self.alarm = fetch_alarms()
        if self.alarm == None:
            print("no alarm found")
            return ""
        # self.alarm = latest_alarm(self.alarm_list)
        self.alarm_name = self.alarm[0][0]
        self.alarm_time = self.alarm[0][2]+" "+self.alarm[0][3]
        self.alarm_date = self.alarm[0][4]
        while True:
            realdate = actual_date()
            realtime = actual_time()
            print(f"checking for : {self.alarm_time} == {realtime} and {self.alarm_date} == {realdate}")
            print("checking for : self.alarm_time == realtime and self.alarm_date == realdate")
            if self.alarm_time == realtime and self.alarm_date == realdate :
                break
            else:
                time.sleep(10)
        self.ring_alarm()
                
    def stop_alarm(self):
        global count
        count+=1
        ALARM_NAME = self.alarm[0][0]
        ALARM_TIME = self.alarm[0][2]
        ALARM_DAYLIGHT = self.alarm[0][3]
        ALARM_DATE = self.alarm[0][4]
        delete_alarm_record(alarm_name=ALARM_NAME, time=ALARM_TIME, daylight=ALARM_DAYLIGHT, date=ALARM_DATE)
        mixer.music.stop()
        self.alarm_interface.destroy()
        # self.check_alarm_time()


    def snooze_alarm(self, img_label, label_img):
        timer_font= Font(family = "RocknRoll One", size = 10, weight='bold')
        self.onetime = 0
        if self.onetime == 0:
            mixer.music.stop()
            img_label['image'] = label_img
            self.onetime=1
        timer = Label(self.alarm_interface, bg="#043492", fg="white", font=timer_font)
        timer.place(x=35, y=5, width=140, height=30)

        if self.sec>0:
            print(self.sec)
            timer['text'] = "Ring After "+time.strftime("%M:%S", time.gmtime(self.sec))+"s"
            self.sec -= 1
            self.alarm_interface.after(ms=1000,func=lambda : self.snooze_alarm(img_label, label_img))
        else:
            self.sec=600
            timer['bg'] = "white"
            self.ring_alarm()


    def ring_alarm(self):
        mixer.music.set_volume(1.0)
        mixer.music.play(10)
        #real time label
        present_time_font= Font(family = "RocknRoll One", size = 18, weight='bold')
        time_label=Label(self.alarm_interface, background="white", font = present_time_font, foreground="#043492")
        time_label.place(x=226, y=12, width=150, height=30)
        timenow = fetch_time()
        time_label['text'] = timenow
        
        #real date label
        present_date_font= Font(family = "RocknRoll One", size = 14, weight='normal')
        present_date=Label(self.alarm_interface, background="white", foreground="#043492", font= present_date_font)
        present_date.place(x=226, y=45, width=150, height=30)
        datenow = fetch_date()
        present_date['text'] = datenow

        #img
        alarm_img = PhotoImage(file="./images/label images/alarm/a3.png./")
        imglabel = Label(self.alarm_interface, background="white", image=alarm_img)
        imglabel.place(x=20, y=40, width=175, height=139)

        #snooze button
        snooze_font= Font(family = "RocknRoll One", size = 14, weight='normal')
        alarm_img2 = PhotoImage(file="./images/label images/alarm/a1.png./")
        snooze_alarm_btn = Button(self.alarm_interface, background= "#043492", relief=FLAT, borderwidth=0, text = "SNOOZE", font= snooze_font, foreground= "white", activebackground="white", activeforeground="#043492", command=lambda : self.snooze_alarm(imglabel, alarm_img2))
        snooze_alarm_btn.place(x=233, y=90, width=136, height=40)

        #stop button
        stop_font= Font(family = "RocknRoll One", size = 14, weight='normal')
        stop_alarm_btn = Button(self.alarm_interface, background= "#043492", relief=FLAT, borderwidth=0, text = "STOP", font= stop_font, foreground= "white", command= lambda : self.stop_alarm())
        stop_alarm_btn.place(x=233, y=140, width=136, height=40)
        mainloop()



    


############-class ends-###############


alarm().check_alarm_time()