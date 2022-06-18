from tkinter import *
from tkinter.font import Font
import time
from PIL import ImageTk, ImageSequence, Image
from threading import Thread
import os
import pyttsx3 as tts
import datetime as dt
import time
import listen_n_speak as lns

# WELCOME SPLASH SCREEN

window = Tk()
window.title("Shaurya - Personal Assistant")
window.config(background="grey")
window.geometry("600x300+400+200")
window.resizable(0,0)
window.overrideredirect(True)


def greet(user):
    """ This Function greets the user whenever the user logins to the Shaurya Assistant. """

    hour = dt.datetime.now().hour

    daytime = ""
    if hour >= 0 and hour < 12:
        daytime = "good morning"
    elif hour >= 12 and hour < 17:
        daytime = "good afternoon"
    elif hour >= 17 and hour < 19:
        daytime = "good evening"
    elif hour >= 19 and hour < 24:
        daytime = "good night"
   
    greet = f" {daytime} {user}, please wait, i am getting ready. "
    lns.speak(greet)
    


def clear_frame():
    global welcome_screen
    for widgets in welcome_screen.winfo_children():
        widgets.destroy()


def speak(audio_data):
    """Speak the string value"""
    try:
        audio_engine = tts.init()
        voices = audio_engine.getProperty('voices')
        audio_engine.setProperty("voice", voices[0].id)
        audio_engine.setProperty("rate", 160)
    except:
        pass
    audio_engine.say(audio_data)
    audio_engine.runAndWait()



def proceed():
    Thread(target = os.startfile, args=("shaurya.py",)).start()
    time.sleep(8)
    Thread(target = clear_frame, args=()).start()
    window.destroy()
    

def gifimg(label, imgs, refresh_rate=0):
    """Animation : Play Gifs"""
    print("gifimg() called....")

    try:
        while True:
            for img in ImageSequence.Iterator(imgs):
                img_frame = ImageTk.PhotoImage(img)
                label.config(image = img_frame)
                window.update()
                time.sleep(0.045)
    except:
        pass


def next_frame():
    welcome_screen_frame()


label_img=PhotoImage(file="./images/label images/welcome_label.png")
btn_img=PhotoImage(file="./images/button images/takeoff_button.png")

def welcome_screen_frame():
    global welcome_screen
    global label_img
    global btn_img
    global user_name
    
    welcome_screen = Frame(window, background="white")
    welcome_screen.place(x=300,y=0, width=300, height=300)

    label1_text_font = Font(family = "RocknRoll One",size = 14, weight='normal')
    label2_text_font = Font(family = "RocknRoll One",size = 12, weight='normal')
    
    uname = user_name.get()
    uname = uname.split(" ")
    textlabel1=Label(welcome_screen, background="white", text=f"Hi {uname[0]}, I am Shaurya", foreground="#161467", font=label1_text_font)
    textlabel1.place(x=0, y=50, width=280, height=40)

    textlabel2=Label(welcome_screen, background="white", text="I am Your Personal Assistant", foreground="#161467", font=label2_text_font)
    textlabel2.place(x=0, y=90, width=280, height=40)

    textlabel3=Label(welcome_screen, image=label_img, background="white")
    textlabel3.place(x=0, y=140, width=280, height=40)

    greet(uname[0])
    time.sleep(1)
    statement=f"Hi {uname[0]}, I am Shaurya, your personal assistant. ready for the takeoff. lets go"
    speak_thread=Thread(target=speak, args=(statement,))
    speak_thread.start()

    proceed_btn = Button(welcome_screen, background="white", image=btn_img, activebackground="white", borderwidth=0, relief=FLAT,command = proceed)
    proceed_btn.place(x=60, y=200, width=200, height=40)


def user_intro_screen_frame():
    global user_intro_screen
    global label_img
    global btn_img
    global user_name

    user_name = StringVar()

    user_intro_screen = Frame(window, background="white")
    user_intro_screen.place(x=0,y=0, width=600, height=300)

    label1_text_font = Font(family = "RocknRoll One",size = 15, weight='bold')
    label2_text_font = Font(family = "RocknRoll One",size = 14, weight='normal')
    entry_text_font = Font(family = "RocknRoll One",size = 13, weight='normal')
    close_btn_font = Font(family = "RocknRoll One",size = 15, weight='bold')
    btn_text_font = Font(family = "RocknRoll One",size = 13, weight='normal')


    textlabel1=Label(user_intro_screen, background="white", text="Shaurya Assistant", foreground="#161467", font=label1_text_font)
    textlabel1.place(x=300, y=30, width=280, height=40)

    close_btn = Button(user_intro_screen, bg="#161467", fg= "white", activebackground="#161467", activeforeground="white", text = 'X', font=close_btn_font, command= window.destroy)
    close_btn.place(x=550, y=5, width=55, height=30)

    textlabel1=Label(user_intro_screen, background="white", text="Welcome, Lets Move...", foreground="#161467", font=label2_text_font)
    textlabel1.place(x=300, y=70, width=280, height=40)

    name_btn = Button(user_intro_screen, text = "Take My Name", fg="white", activeforeground="white",  background="#161467", activebackground="#1091ca", borderwidth=0, relief=FLAT, font = btn_text_font,  command= next_frame, state = DISABLED)
    name_btn.place(x=370, y=200, width=150, height=40)

    name_entry = Entry(user_intro_screen, textvariable= user_name, background="#1091ca", foreground="white", font=entry_text_font, relief= FLAT)
    name_entry.place(x=300, y=135, width=280, height=40)
    name_entry.bind('<FocusIn>', lambda e: name_btn.config(state=NORMAL))
    name_entry.bind('<Return>', lambda e: next_frame())
    name_entry.bind('<Button>', lambda e: user_name.set(""))
    user_name.set("  Your Name...")

    statement="Hi user, can you please tell me your name?"
    speak_thread=Thread(target=speak, args=(statement,))
    speak_thread.start()

    giflabel=Label(user_intro_screen, background="white")
    giflabel.place(x=0, y=22, width=300, height=225)

    imgpath = "./images/gifs/takeoff.gif"
    resolution = (300,225)
    imgs=Image.open(imgpath)
    imgs.resize(resolution)
    gifimg(giflabel, imgs)



user_intro_screen_frame()


window.mainloop()
mainloop()