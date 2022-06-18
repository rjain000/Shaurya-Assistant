from tkinter import *
from tkinter.font import Font
import webbrowser
import time
import pyautogui

window = Tk()
window.title("Shaurya - Whatsapp Client")
window.config(background="white")
window.geometry("450x300")
window.resizable(0,0)
icon = PhotoImage(file = './images/images/bot_icon.png')
window.iconphoto(False, icon)

head_label_font= Font(family= "RocknRoll One", size= 15, weight= 'bold')
subhead_label_font= Font(family= "RocknRoll One", size= 13, weight= 'normal')
entry_font= Font(family= "RocknRoll One", size= 12, weight= 'normal')
btn_font= Font(family= "RocknRoll One", size= 12, weight= 'bold')

head_label= Label(window, bg="#128c7f", fg="white", font= head_label_font, text = "Whatsapp Message Client")
head_label.place(x=0, y=0, width=450, height=40)

phone_label= Label(window, bg="#128c7f", fg="white", font= subhead_label_font, text= "Phone No.")
phone_label.place(x=25, y=50, width=120, height=30)

phone_var = StringVar()
phone_entry = Entry(window, bg="#128c7f", relief=FLAT, fg="white", font= entry_font, textvariable=phone_var)
phone_entry.place(x=150, y=50, width=265, height=30)

body_label= Label(window, bg="#128c7f", fg="white", font= subhead_label_font, text= "Message")
body_label.place(x=25, y=90, width=120, height=30)

body_var = StringVar()
body_entry = Entry(window, bg="#128c7f", relief=FLAT, fg="white", font= entry_font, textvariable=body_var)
body_entry.place(x=150, y=90, width=265, height=160)

def send_message():
    global phone_var
    global body_var
    phn_no = phone_var.get()
    message = body_var.get()
    phone_no = '+91' + str(phn_no)
    webbrowser.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
    time.sleep(15)
    pyautogui.press("ENTER")
    print("enter hitted")
    

send_btn = Button(window, bg="#128c7f", relief=FLAT, fg="white", font= btn_font, bd=0, text="Send Message", activebackground="white", activeforeground="#128c7f", command = send_message)
send_btn.place(x=150, y=255, width=265, height=35)
send_btn.bind("<Button>", lambda e: send_btn.config(text="Sending"))
send_btn.bind("<ButtonRelease>", lambda e: send_btn.config(text="Send Message"))

window.mainloop()
