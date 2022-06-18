from tkinter import *
from tkinter.font import Font
import requests
import smtplib as smtp
import database


# MAIN WINDOW
window = Tk()
window.title("Shaurya - Mail Setup")
window.config(background="white")
window.geometry("800x450+250+100")
window.resizable(0,0)
icon = PhotoImage(file = './images/images/bot_icon.png')
window.iconphoto(False, icon)

#####-code starts here-#####

#global variables
mail_id = StringVar()
password = StringVar()

#font
text_font_bold = Font(family= "RocknRoll One", size= 15, weight= 'bold')
text_font_normal = Font(family= "RocknRoll One", size= 15, weight= 'normal')

#info frame
info_frame = Frame(window, bg="#009988")
info_frame.place(x=0, y=0, width=400, height=450)

#info head
info_head_label = Label(info_frame, background="white", text="Welcome to Mail Setup Wizard", font=text_font_bold, fg="#008c7d")
info_head_label.place(x=25, y=25, width=350, height=40)

#credentials head
credentials_head_label = Label(window, background="#008c7d", text="Mail Credentials", font=text_font_bold, fg="white")
credentials_head_label.place(x=425, y=25, width=350, height=40)

#text label font
label_text_font = Font(family = "RocknRoll One",size = 12, weight='bold')
#text button font
btn_text_font = Font(family = "RocknRoll One",size = 12, weight='bold')
#text label font
entry_text_font = Font(family = "RocknRoll One",size = 12, weight='normal')


#text for entry feild email
email_label= Label(
    window,
    text="Email-ID",
    background='white',
    font=label_text_font,
    foreground="#009988",
    anchor='w'
    )
email_label.place(x=440, y=100, width=100, height=30)

#entry background image - email
global email_bg
email_bg=PhotoImage(file="./images/entry images/frame2 label.png")
back_img_email = Label(
    window,
    image = email_bg,
    background="white"
    )
back_img_email.place(x=430, y=129, width=340, height=42)

#entry feild email
email_entry = Entry(
    window,
    background="#009988",
    font=entry_text_font,
    relief=FLAT,
    fg="white",
    textvariable= mail_id
    )
email_entry.place(x=450, y=130, width=300, height=40)

#########################################################################
#doc help
doc_text="""Documentation for Generating App Password for your mail\n 
1. Go to your Google Account.\n 
2. On the left navigation panel, choose Security.\n 
3. On the 'Signing in to Google' panel, choose App passwords.\n 
    # If you don’t see this option:\n 
    # 2-Step Verification is not set up for your account\n    
    # 2-Step Verification is set up for security keys only\n  
    # Your account is through work, school or other organisation\n    
    # You’ve turned on Advanced Protection for your account\n 
4. At the bottom, choose Select app as Others.\n    
5. Type 'Shaurya Assistant' in the text feild.\n    
6. Choose Generate.\n   
7. Follow the instructions to enter the app password. The app password is the 16-character code in the yellow bar on your device.\n     
8. Choose Done.
 """

info_bg = Label(info_frame, bg="white")
info_bg.place(x=25, y=85, width=350, height=350)


info_label = Text(info_frame, bg="white", fg="#009988", borderwidth=0, wrap= WORD)

info_label.insert(END, doc_text)
info_label.place(x=30, y=85, width=345, height=335)



#############################################################################

#text for entry feild password
password_label= Label(
    window,
    text="App/Mail Password",
    background='white',
    font=label_text_font,
    foreground="#009988",
    anchor='w'
    )
password_label.place(x=440, y=180, width=200, height=30)

#entry background image - APP password
global password_bg
password_bg=PhotoImage(file="./images/entry images/frame2 label.png")
back_img_password = Label(
    window,
    image = email_bg,
    background="white"
    )
back_img_password.place(x=430, y=209, width=340, height=42)


#entry feild password
password_entry = Entry(
    window,
    background="#009988",
    font=entry_text_font,
    relief=FLAT,
    fg="white",
    show="*",
    textvariable= password
    )
password_entry.place(x=450, y=210, width=300, height=40)

#button feild - login
global login_btn_regular
global login_btn_click
login_btn_regular=PhotoImage(file = "./images/button images/head_button_login_unselected.png")
login_btn_click=PhotoImage(file = "./images/button images/head_button_login_selected.png")


#functions
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

def add_btn():
    global information_label
    global mail_id
    global password

    user_email = mail_id.get()
    user_password = password.get()

    mail_id.set("")
    password.set("")
    
    email_val = isValidMail(user_email)

    if user_email == "" or user_password == "":
        information_label['text'] = "Please Enter Credentials..."
    else:
        if email_val == True:
            try:
                mail_obj = smtp.SMTP_SSL("smtp.gmail.com", 465)
            except:
                mail_obj = smtp.SMTP("smtp.gmail.com", 587)
                mail_obj.ehlo()
                mail_obj.starttls()
                mail_obj.ehlo()
            try:
                information_label['text'] = "Connecting to your Mail Server"
                mail_obj.login(user_email, user_password)
                database.add_mail(user_email, user_password)
                information_label['text'] = f"Mail \'{user_email}\' Added Successfully..."
            except:
                information_label['text'] = "Access Denied..."
        else:
            information_label['text'] = f"\'{user_email}\' is Not a Valid Mail..."


add_btn = Button(
    window,
    background='#008c7d',
    relief=FLAT,
    font = btn_text_font,
    fg="white",
    text = "Add Mail",
    activebackground="white",
    activeforeground="#008c7d",
    borderwidth=0,
    command=add_btn,
    )
add_btn.place(x=530, y=270, width=129, height=42)
add_btn.bind("<Button>", lambda e: add_btn.config(text="Adding...") )
add_btn.bind("<ButtonRelease>", lambda e: add_btn.config(text="Add Mail") )
    
    #info_label
information_label = Label(window, bg="white", fg="#008c7d", text="", font= entry_text_font, wraplength=300)
information_label.place(x=425, y=325, width=350, height=120)

#####-code ends here-#####

window.mainloop()