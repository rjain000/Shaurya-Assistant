from tkinter import *
from pygame import mixer


class timer:
    def __init__(self) -> None:
        #music interface
        mixer.init()
        mixer.music.load("./sounds/alarm/alarm.mp3")
        #interface
        self.timer_interface = Tk()
        self.timer_interface.title("Alarm")
        self.timer_interface.config(background="white")
        self.timer_interface.geometry("400x200+475+225")
        self.timer_interface.resizable(0,0)
        self.timer_interface.overrideredirect(True)

    def set_timer(self):

        self.hour_value = StringVar()
        self.min_value = StringVar()

        hour_options = ('01','02','03','04','05','06','07','08','09','10','11','12')
        min_options = ('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59')
        
        self.head_label = Label(self.timer_interface, background = "white", font=("RocknRoll One", 20, 'bold'),foreground="#043492", text="Timer")
        self.head_label.place(x=100, y=5, width=200, height=30)

        #img label
        alarmImg = PhotoImage(file="./images/label images/alarm/alarm.png")
        img_label = Label(self.timer_interface, image=alarmImg, background="white")
        img_label.place(x=15, y=50, width=120, height=95)

        #hour label
        hour_spinbox = Spinbox(self.timer_interface, textvariable= self.hour_value, values=hour_options, background="#016CCF", borderwidth=0, font = ("RocknRoll One", 18, 'bold'), foreground="white", relief=FLAT, justify=CENTER, wrap=True)
        
        hour_spinbox.place(x=170, y=63, width=70, height=40)

        #colon label
        colon_label = Label(self.timer_interface, background="white", text = ":", font= ("RocknRoll One", 22, 'bold'), fg="#016CCF")
        colon_label.place(x=245, y=63, width=15, height=40)

        #minutes label
        minutes_label = Spinbox(self.timer_interface, textvariable= self.min_value, values= min_options, background="#016CCF", borderwidth=0, font = ("RocknRoll One", 18, 'bold'), foreground="white", relief=FLAT, justify=CENTER, wrap=True)
        minutes_label.place(x=260, y=63, width=70, height=40)

        mainloop()







timer().set_timer()