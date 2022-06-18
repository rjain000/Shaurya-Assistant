from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import database
import os
import requests
import smtplib as smtp
from network import *
import pyttsx3 as tts
import time
from email.message import EmailMessage as email
from threading import Thread
######################################-GUI-#########################


# MAIN WINDOW
window = Tk()
window.title("Shaurya - Mail Sender")
window.config(background="white")
window.geometry("800x450+250+100")
window.resizable(0,0)
icon = PhotoImage(file = './images/images/bot_icon.png')
window.iconphoto(False, icon)

####code starts here
#font head

head_label_font= Font(family= "RocknRoll One", size= 15, weight= 'bold')
entry_font= Font(family= "RocknRoll One", size= 13, weight= 'normal')

head_label=Label(window, text="Personal Mail Sender", font=head_label_font, fg="white", bg="#008c7d")
head_label.place(x=25, y=10, width=750, height=35)

#from section

from_label = Label(window, text="From : ", font=head_label_font, fg="#008c7d", bg="white", anchor='e')
from_label.place(x=25, y=55, width=125, height=35)

#emails option box

From = None
To = None
To_mail = StringVar()
to_mail_list = []
mail_text="Mails CC\n"
mail_subject = StringVar()
Subject = None
mail_body = StringVar()
Body = None

#getting mails----------------------------------------------
saved_mails = database.get_mails()

if saved_mails == None:
    os.startfile(os.getcwd()+"\\Applications\\mailsetup.py")
    exit()
    
mail_creds = {}

for mail in saved_mails:
    mail_creds[mail[0]] = mail[1]

mail_ids = list(mail_creds.keys())
#getting mails----------------------------------------------

###################-functions

def isValidMail(mail_id):
    """Checks for a valid mail using api key"""
    api_key = "666f93e9-f7bb-4751-a21e-1e1b9689f83b"
    
    response = requests.get(
    "https://isitarealemail.com/api/email/validate",
    params = {'email': mail_id},
    headers = {'Authorization': "Bearer " + api_key })

    status = response.json()['status']

    if status == "valid":
      return True
    elif status == "invalid":
        return False
    else:
      return None


def mail_selected(event):
    global From
    From= mails_options.get()

counter=0

def add_to_mail_list():
    global counter
    global To
    global to_mail_list
    global To_mail
    global mails_added

    To = To_mail.get()
    To_mail.set("")

    if isValidMail(To) == True:
        to_mail_list.append(To)
        mails_added.insert(counter, To)
        counter+=1
    else:
        messagebox.showerror("Mail Validator", "This Mail Doesnot Exist...")

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


status_label= Label(window, text="Gmail SSL AND TLS SUPPORT Is Active", font=head_label_font, fg="white", bg="#008c7d")
status_label.place(x=25, y=340, width=745, height=42)

def send_mail():
    global To
    global To_mail
    global From
    global to_mail_list
    global Subject
    global mail_subject
    global Body
    global mail_body
    global status_label

    Subject = mail_subject.get()
    Body = mail_body.get()

    if From==None:
        messagebox.showerror("Mail Validator","Please select Sender Mail...")

    elif To=="" and len(to_mail_list)<1:
        messagebox.showerror("Mail Validator","Please add atleast 1 Receiver's Mail...")

    else:
        if len(to_mail_list)<1:
            To = To_mail.get()
            if isValidMail(To) == True:
                status_label.config(text="Sending mail to : "+To)
            else:
                statement="This Mail doesnot Exist in real World..."
                status_label.config(text=statement)
                Thread(target=speak, args=("This Mail doesnot Exist in real World...",)).start()
                messagebox.showerror("Mail Validator",f"To: \'{To}\' \nThis Mail doesnot Exist in real World...")
        else:
            status_label.config(text="Sending mail to : "+str(list(to_mail_list)))

        print(Subject)
        print(Body)

        #code to send mail
        if isConnected() == False:
            statement = "You are not connected to network"
            status_label.config(text=statement)
            time.sleep(1)
            exit()


        msg = email()

        msg['From'] = From

        if len(to_mail_list)<=1:
            msg['To'] = To
        else:
            msg['To'] = to_mail_list

        msg['Subject'] = Subject

        msg.set_content(Body)

        try:
            mail_obj = smtp.SMTP_SSL("smtp.gmail.com", 465)
            status_label.config(text="Starting SSL Secure Connection...")
        except:
            mail_obj = smtp.SMTP("smtp.gmail.com", 587)
            mail_obj.ehlo()
            mail_obj.starttls()
            status_label.config(text="Starting TLS Connection...")
            mail_obj.ehlo()

        finally:
            mail_obj.login(From, mail_creds[From])
            statement = "Connecting to your Mail Server..."
            status_label.config(text=statement)
            speak(statement)

            try:
                mail_obj.send_message(msg)
                statement = "Mail Send Successfully..."
                speak(statement)
                status_label.config(text=statement)
                mail_obj.quit()
            except:
                statement = "Failed to connect to mail server..."
                speak(statement)
                status_label.config(text=statement)
                messagebox.showerror("Mail Server", "Failed to connect to mail server")


###################-functions


mails_options = ttk.Combobox(window, value=mail_ids, font=entry_font, background="white", foreground="#008c7d")
mails_options.config()
mails_options.set("Select Mail from List...")
mails_options.bind("<<ComboboxSelected>>", mail_selected)
mails_options.place(x=160, y=55, width=430, height=35)


to_label = Label(window, text="To : ", font=head_label_font, fg="#008c7d", bg="white", anchor='e')
to_label.place(x=25, y=100, width=125, height=35)


to_entry = Entry(window, textvariable= To_mail, font=entry_font, fg="#008c7d", bg="white", borderwidth="1px")
to_entry.place(x=160, y=100, width=375, height=35)

cc_btn = Button(window, text="CC", font=head_label_font, fg="white", bg="#008c7d", bd=0, activebackground="white", activeforeground= "#008c7d", command = add_to_mail_list)
cc_btn.place(x=540, y=100, width=53, height=35)

subject_label = Label(window, text="Subject : ", font=head_label_font, fg="#008c7d", bg="white", anchor='e')
subject_label.place(x=25, y=145, width=125, height=35)


from_entry = Entry(window, textvariable= mail_subject, font=entry_font, fg="white", bg="#008c7d", relief=FLAT)
from_entry.place(x=160, y=145, width=433, height=35)

body_entry = Entry(window, textvariable= mail_body, font=entry_font, fg="white", bg="#008c7d", relief=FLAT, justify=LEFT)
body_entry.place(x=25, y=190, width=745, height=140)

###################################-mails added list

mails_added = Listbox(window, fg="white", bg="#008c7d", selectmode=SINGLE)
mails_added.place(x=600, y=55, width=170, height=85)

######function
def remove_mail():
    global mails_added
    global to_mail_list
    print(to_mail_list)
    rm_mail_index = mails_added.curselection()[0]
    to_mail_list.pop(rm_mail_index)
    mails_added.delete(rm_mail_index)
    print(to_mail_list)


remove_btn = Button(window, text="Remove", font=head_label_font, fg="white", bg="#008c7d", bd=0, activebackground="white", activeforeground= "#008c7d", command = remove_mail)
remove_btn.place(x=600, y=145, width=170, height=35)

###################################

send_btn= Button(window, text="Send", font=head_label_font, fg="white", bg="#008c7d", bd=0, activebackground="white", activeforeground= "#008c7d", command = send_mail)
send_btn.place(x=450, y=400, width=300, height=38)
send_btn.bind("<Button>", lambda e: send_btn.config(text="Sending..."))
send_btn.bind("<ButtonRelease>", lambda e: send_btn.config(text="Send"))


close_btn = Button(window, text="Close", font=head_label_font, fg="white", bg="#008c7d", bd=0, activebackground="white", activeforeground= "#008c7d", command=window.destroy)
close_btn.place(x=50, y=400, width=300, height=38)


####code ends here

mails_options.tkraise()
window.mainloop()
#####################################################################