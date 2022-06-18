######################################-PRE-DEFINED MODULES-############################
from tkinter import *
from tkinter import PhotoImage
from tkinter.font import Font
import time
from threading import Thread
import webbrowser
from fontTools.ttLib import TTFont#used in main function(donot remove this code)
######################################-USER-DEFINED MODULES-############################
import listen_n_speak as lns
from Applications.clock import *
from Applications.database import *
import features
from utility.sys_info import *
import network
import commander

###############################################################################################
######################################-MAIN FILE CONFIG-#######################################
###############################################################################################

# MAIN WINDOW
window = Tk()
window.title("Shaurya - Personal Asssistant")
window.config(background="white")
window.geometry("800x450+250+100")
window.resizable(0,0)
icon = PhotoImage(file = './images/images/bot_icon.png')
window.iconphoto(False, icon)

###############################################################################################
###############################################################################################

#GLOBAL VARIABLES
keyboard_img = PhotoImage(file="./images/button images/keyboard_btn.png")
mic_img = PhotoImage(file="./images/button images/mic_btn.png")

listening_img=PhotoImage(file="./images/label images/listening_inactive.png")
listening_img2=PhotoImage(file="./images/label images/listening_active.png")

reco_img=PhotoImage(file="./images/label images/recognizing_inactive.png")
reco_img2=PhotoImage(file="./images/label images/recognizing_active.png")

typemode_img=PhotoImage(file="./images/label images/typing_inactive.png")
typemode_img2=PhotoImage(file="./images/label images/typing_active.png")

SEARCH_BOX= StringVar()
SEARCH_BOX.set("Search What ever you want to search?")

COMMAND_BOX= StringVar()
COMMAND_BOX.set("Type your Command...")


#labels-8
task_label1= None
task_label2= None
task_label3= None
task_label4= None
task_label5= None
task_label6= None
task_label7= None
task_label8= None
task_label9= None
task_label10= None
task_label11= None
task_label12= None

task_label_counter= 0

##############################--label images--##########################

#   alarm :: label-5
alarm_img = PhotoImage(file="./images/label images/alarm/alarm_inactivated.png")
alarm_img_active = PhotoImage(file="./images/label images/alarm/alarm_activated.png")

    #battery :: label-11
        #charging_{percentage}
charging_10 = PhotoImage(file="./images/label images/battery_info_imgs/battery_10_charging.png")
charging_25 = PhotoImage(file="./images/label images/battery_info_imgs/battery_25_charging.png")
charging_50 = PhotoImage(file="./images/label images/battery_info_imgs/battery_50_charging.png")
charging_75 = PhotoImage(file="./images/label images/battery_info_imgs/battery_75_charging.png")
charging_100 = PhotoImage(file="./images/label images/battery_info_imgs/battery_full.png")

        #not charging_{percentage}
battery_10 = PhotoImage(file="./images/label images/battery_info_imgs/battery_10.png")
battery_25 = PhotoImage(file="./images/label images/battery_info_imgs/battery_25.png")
battery_50 = PhotoImage(file="./images/label images/battery_info_imgs/battery_50.png")
battery_75 = PhotoImage(file="./images/label images/battery_info_imgs/battery_75.png")
battery_100 = PhotoImage(file="./images/label images/battery_info_imgs/battery_full.png")


#status lights
listen_light_cyan= None
reco_light_green= None
typing_light_orange= None

#command status label - Bottom frame 2
command_status_label= None

#mic listening
mic = 'on'

# GLOBAL FUNCTIONS 

#status light imags
def get_imgs():
    global listening_img
    global listening_img2
    global reco_img
    global reco_img2
    imgs=(
        listening_img,
        listening_img2,
        reco_img,
        reco_img2
    )
    return imgs

#status light labels
def get_status_labels():
    global listen_light_cyan
    global reco_light_green

    status_labels=(
        listen_light_cyan,
        reco_light_green
    )

    return status_labels

#send command function
def commander_processor(command, source = "typing"):
    global mic
    if "terminate" in command or "quit" in command or "exit" in command or 'terminator' in command:
        command_status_label.config(text="Terminating in 3 seconds")
        lns.speak("Terminating in 3 seconds")
        command_status_label.config(text="3")
        lns.speak("3")
        command_status_label.config(text="2")
        lns.speak("2")
        command_status_label.config(text="1")
        lns.speak("1")        
        command_status_label.config(text="Terminated...")
        lns.speak("Terminated")
        close()

    elif 'sleep' in command:
        command_status_label.config(text="Going for Sleep in 3 seconds")
        lns.speak("Going For sleep in 3 seconds")
        command_status_label.config(text="3")
        lns.speak("3")
        command_status_label.config(text="2")
        lns.speak("2")
        command_status_label.config(text="1")
        lns.speak("1")        
        command_status_label.config(text="Sleep Mode Activated...")
        lns.speak("Wake me Up When you need.")
        os.startfile(os.getcwd()+"/wakeup.py")
        close()

    if source == "mic" and mic=="off":
        print("mic command is ignored...")
        return
    commander.mycommand(command)

#typing function
def type_command():
    command=COMMAND_BOX.get()
    commander_processor(command, source="typing")
    COMMAND_BOX.set("")
    

#listening function
def listen_command():
    global command_status_label
    global mic
    imgs= get_imgs()
    status_labels= get_status_labels()
    while True:
        time.sleep(0.5)
        mic_status = None
        mic_status = fetch_device_status("mic")
        print("mic_status : ", mic_status)
        if fetch_device_status("terminate") == "on":
            print('Listing Sharuya.py Functions Ends')
            return ""
        if network.isConnected() == True:
            try:
                if mic == 'off' or mic_status=="off":
                    command_status_label['text'] = "Mic is Off..."
                    print("mic is off") 
                    break
                print("mic is on")
                command = lns.listen(command_status_label, status_labels, imgs)
                mic_status = Thread(target=fetch_device_status, args=("mic",)).start()
                commander_processor(command, source="mic")
            except:
                continue
        else:
            command_status_label['text'] = "Connection Lost..."
    print("loop breaked")
    if fetch_device_status("terminate") == "off":
        listen_command()
    


def change_command_input_type_to(input_type):
    global mic
    global bottom_frame1
    global bottom_frame2
    if input_type == "typing":
        mic = 'off'
        time.sleep(1)
        print("Typing mode on...")
        bottomframe2()
    elif input_type == "audio":
        mic = 'on'
        print("Listening mode on...")
        bottomframe1()
        # Thread(target=listen_command).start()
    else:
        pass

def focus_bar():
    typing_light_orange.config(image=typemode_img2)
    COMMAND_BOX.set("")


def close():
    global mic    
    mic = "off"
    set_device_status('mic',"off")
    set_device_status('terminate',"on")
    window.destroy()

# MAIN FRAME FUNCTION-------------------------
main_frame = None
about_us_frame = None

def mainframe():
    global main_frame
    main_frame= Frame(window, background="#272244")
    main_frame.place(x=0, y=70, width=800, height=320)

    global task_label1
    global task_label2
    global task_label3
    global task_label4
    global task_label5
    global task_label6
    global task_label7
    global task_label8
    global task_label9
    global task_label10
    global task_label11
    global task_label12

    global charging_10
    global charging_25
    global charging_50
    global charging_75
    global charging_100

    global battery_10
    global battery_25
    global battery_50
    global battery_75
    global battery_100

    battery_imgs=(
        (
            charging_10,
            charging_25,
            charging_50,
            charging_75,
            charging_100
        ),
        (
            battery_10,
            battery_25,
            battery_50,
            battery_75,
            battery_100
        )
        
    )
    ###############################- function code starts here - ############################
    search_bar_font= Font(family = "RocknRoll One", size = 15, weight='normal')

    search_bar=Entry(main_frame, textvariable=SEARCH_BOX)
    search_bar.place(x=20, y=15, width=515, height=35)
    search_bar.config(font=search_bar_font)
    search_bar.bind("<FocusIn>", lambda e:SEARCH_BOX.set(""))
    search_bar.bind("<Return>", lambda e: Thread(target=features.search_bar, args=(SEARCH_BOX.get(),)).start())
    search_bar.bind("<FocusOut>", lambda e:SEARCH_BOX.set("Search What ever you want to search?"))


    global search_icon_img
    search_icon_img = PhotoImage(file="./images/button images/search_icon.png")
    search_icon_btn = Button(main_frame, background="#c5e6df", image=search_icon_img, activebackground="white", borderwidth=0, command= lambda : Thread(target=features.search_bar, args=(SEARCH_BOX.get(),)).start())
    search_icon_btn.place(x=530, y=12, width=40, height=40)

    #time label
    time_font= Font(family = "RocknRoll One", size = 18, weight='bold')
    time_label=Label(main_frame, background="white", foreground="#272244", font= time_font)
    time_label.place(x=630, y=7, width=140, height=40)
    Thread(target=real_time, args=(time_label,)).start()

    #date label
    date_font= Font(family = "RocknRoll One", size = 13, weight='normal')
    date_label=Label(main_frame, background="white", foreground="#272244", font= date_font)
    date_label.place(x=630, y=48, width=140, height=28)
    Thread(target=real_date, args=(date_label,)).start()

    #label imgs
    global alarm_img

    label_status_font = Font(family = "RocknRoll One", size = 14, weight='normal')
    label_status_font_text = Font(family = "RocknRoll One", size = 13, weight='normal')
    iot_status_font_text = Font(family = "RocknRoll One", size = 11, weight='normal')
    
    #task labels - 8 labels
    global plug_on_img
    global plug_off_img
    global light_bulb_on_img
    global light_bulb_off_img
    global fan_on_img
    global fan_off_img
    # first row
    plug_on_img=PhotoImage(file="./images/label images/switch/switch_on.png")
    plug_off_img=PhotoImage(file="./images/label images/switch/switch_off.png")
    
    light_bulb_on_img=PhotoImage(file="./images/label images/bulb/bulb_on.png")
    light_bulb_off_img=PhotoImage(file="./images/label images/bulb/bulb_off.png")
    
    fan_on_img=PhotoImage(file="./images/label images/fan/fan_on.png")
    fan_off_img=PhotoImage(file="./images/label images/fan/fan_off.png")
    
    #plug-1
    plug_1=Label(main_frame, background="#272244", image= plug_off_img)
    plug_1.place(x=40, y=66, width=100, height=90)

    #plug-1 info
    plug_1_info=Label(main_frame, background="#524e69", fg="white", text = "Plug 1", font=iot_status_font_text)
    plug_1_info.place(x=40, y=156, width=100, height=30)
    

    #plug-2
    plug_2=Label(main_frame, background="#272244", image= plug_off_img)
    plug_2.place(x=170, y=66, width=100, height=90)
    
    #plug-2 info
    plug_2_info=Label(main_frame, background="#524e69", fg="white", text = "Plug 2", font=iot_status_font_text)
    plug_2_info.place(x=170, y=156, width=100, height=30)
    

    #light
    light_bulb=Label(main_frame, background="#272244", image= light_bulb_off_img)
    light_bulb.place(x=300, y=66, width=100, height=90)
    
    #light_status
    light_bulb_status=Label(main_frame, background="#524e69", fg="white", font=iot_status_font_text, text="Light")
    light_bulb_status.place(x=300, y=156, width=100, height=30)

    #fan
    fan=Label(main_frame, background="#272244", image= fan_off_img)
    fan.place(x=430, y=66, width=100, height=90)

    #fan status
    fan_status=Label(main_frame, background="#524e69", fg="white", font=iot_status_font_text, text="Fan")
    fan_status.place(x=430, y=156, width=100, height=30)
    
        #iot list
    plug_1_list = [plug_1, plug_on_img, plug_off_img, plug_1_info]
    plug_2_list = [plug_2, plug_on_img, plug_off_img, plug_2_info]
    light_bulb_list= [light_bulb, light_bulb_on_img, light_bulb_off_img, light_bulb_status]
    fan_list= [fan, fan_on_img, fan_off_img, fan_status]
    #IOT FUNCTION :: IOT
    ## 1. box
    Thread(target=features.get_IOT_Box_status, args=(plug_1_list, plug_2_list)).start()
    ## 2. Borad
    Thread(target=features.get_IOT_status, args=(light_bulb_list, fan_list)).start()

    ###second row###
    #alarm image
    alarm_task=Label(main_frame, image = alarm_img, background="#272244")
    alarm_task.place(x=40, y=205, width=100, height=70)
    #alarm status
    alarm_info=Label(main_frame, background="#524e69", text="Alarm Off", font=label_status_font_text, foreground="white", justify=CENTER)
    alarm_info.place(x=40, y=275, width=100, height=30)
    #alarm_status_imgs
    alarm_imgs = [alarm_img, alarm_img_active]
    #calling function :: Alarm
    Thread(target=features.check_alarm, args=(alarm_task, alarm_imgs, alarm_info)).start()
    
    #task image :: network
    network_label=Label(main_frame, background="#272244")
    network_label.place(x=170, y=205, width=100, height=70)
    # font
    network_status_font = Font(family = "RocknRoll One", size = 12, weight='normal')
    #task status
    network_status=Label(main_frame, background="#524e69", font = network_status_font, fg="white")
    network_status.place(x=170, y=275, width=100, height=30)
    #images
    network_connected=PhotoImage(file="./images/label images/network/connected.png")
    network_not_connected=PhotoImage(file="./images/label images/network/not_connected.png")
    # imgs list
    network_imgs = [network_connected, network_not_connected]
    #calling function to check for network
    Thread(target=network_check, args=(network_label, network_imgs, network_status,)).start()

    # font
    mail_status_font = Font(family = "RocknRoll One", size = 12, weight='normal')
    #imgs :: mails
    global mail_img
    global no_mail_img
    mail_img = PhotoImage(file = "./images/label images/mail/mail.png")
    no_mail_img = PhotoImage(file = "./images/label images/mail/no_mail.png")
    imgs_mail = [mail_img, no_mail_img]
    #task image :: mails
    mail_label=Label(main_frame, background="#272244", image=no_mail_img)
    mail_label.place(x=300, y=205, width=100, height=70)
    #task status :: mails
    mail_label_info=Label(main_frame, background="#524e69", text="Mails",font=mail_status_font, fg="white")
    mail_label_info.place(x=300, y=275, width=100, height=30)

    Thread(target = features.check_mail, args=(mail_label, imgs_mail, mail_label_info)).start()

    #battery info
        #battery img
    task_label15=Label(main_frame, background="#272244", image=battery_100)
    task_label15.place(x=430, y=205, width=100, height=70)
        #battery percent
    task_label16=Label(main_frame, background="#524e69", text="N/A", font=label_status_font, foreground="white", justify=CENTER)
    task_label16.place(x=430, y=275, width=100, height=30)

    battery_task_labels = (task_label15, task_label16)
    try:
        Thread(target = battery_info, args=(battery_task_labels, battery_imgs,)).start()
    except:
        """for desktops"""
        pass

    #pc specs monitor Frame
        #headline
    temp_font = Font(family = "RocknRoll One", size = 12, weight='bold')

    headfont = Font(family = "RocknRoll One", size = 13, weight='normal')
    labelfont = Font(family = "RocknRoll One", size = 11, weight='normal')

    temp_label = Label(main_frame, bg="white", fg="#272244", text = "Temp N/A", font=temp_font)
    temp_label.place(x=630, y=80, width=140, height=30)
    Thread(target = features.temprature_check, args=(temp_label,)).start()


    head_label = Label(main_frame, bg="#524e69", fg="#85D2BF", text = "PC Manager", font=headfont)
    head_label.place(x=620, y=137, width=150, height=30)

    cpu_label = Label(main_frame, bg="#524e69", fg="#85D2BF", text = "CPU: N/A", font=labelfont, anchor='w')
    cpu_label.place(x=620, y=175, width=150, height=30)

    memory_label = Label(main_frame, bg="#524e69", fg="#85D2BF", text = "Memory: N/A", font=labelfont, anchor='w')
    memory_label.place(x=620, y=210, width=150, height=30)

    network_label = Label(main_frame, bg="#524e69", fg="#85D2BF", text = "Network: N/A", font=labelfont, anchor='w')
    network_label.place(x=620, y=245, width=150, height=30)
    Thread(target = system_config, args=(cpu_label, memory_label, network_label,)).start()

    ############################## function code ends here #######################

about_us_frame = None
frame_counter = 1

def change_frame():
    global about_us_frame
    global main_frame
    global frame_counter

    if frame_counter%2==0:
        main_frame.tkraise()
        about_us_button['image'] = about_us_img
        frame_counter+=1
    else:
        about_us_frame.tkraise()
        about_us_button['image'] = home_img
        frame_counter+=1



def aboutusframe():
    global about_us_frame
    global nawal_pic
    global ritish_pic

    about_us_frame = Frame(window, bg="#272244")
    about_us_frame.place(x=0, y=70, width=800, height=320)

    nawal_pic = PhotoImage(file="./images/button images/nawal_pic.png")
    ritish_pic = PhotoImage(file="./images/button images/ritish_pic.png")

    head_font = Font(family = "RocknRoll One", size = 18, weight='bold')
    sub_head_font = Font(family = "RocknRoll One", size = 15, weight='normal')
    text_font = Font(family = "RocknRoll One", size = 11, weight='normal')

    head_label = Label(about_us_frame, bg= "#272244", fg="white", font= head_font, text = "About The Developers...")
    head_label.place(x=100, y=0, width=600, height=40)

    shaurya_label = Label(about_us_frame, bg= "#272244", fg="white", font= sub_head_font, text = "Shaurya Assistant", bd=0)
    shaurya_label.place(x=300, y=40, width=200, height=35)

    
    text_str = f"""Shaurya is a Smart Assistant developed by \'Nawaldeep Singh\' and \'Ritish Jain\'. Both are students of \'D.A.V. College\', Amritsar. This assistant is capable of controlling IOT Devices as well as most of the common computer functions..."""
    shaurya_font = Font(family="Arial Narrow", size = 12, weight='normal')
    shaurya_text = Text(about_us_frame, bg="#272244", fg="white", font = shaurya_font, wrap=WORD, borderwidth=0)
    shaurya_text.place(x=275, y=80, width=250, height=125)
    shaurya_text.insert(END, text_str)
    shaurya_text.config(state=DISABLED)


    def dev_links(dev_name, platform):
        if dev_name == "Nawaldeep Singh":
            if platform == "instagram":
                webbrowser.open("https://www.instagram.com/nawaldeep_singh/")
            if platform == "github":
                webbrowser.open("https://github.com/nawaldeep-singh")
            if platform == "linkedin":
                webbrowser.open("https://www.linkedin.com/in/nawaldeep-singh/")

        elif dev_name == "Ritish Jain":
            if platform == "instagram":
                webbrowser.open("https://www.instagram.com/_ritish.jain_/")
            if platform == "github":
                webbrowser.open("https://github.com/rjain000")
            if platform == "linkedin":
                webbrowser.open("https://www.linkedin.com/in/ritish-jain-b2979a109/")
        

    global insta_img
    global git_img
    global linkedin_img

    insta_img = PhotoImage(file = "./images/label images/instagram.png")
    git_img = PhotoImage(file = "./images/label images/github.png")
    linkedin_img = PhotoImage(file = "./images/label images/linkedin.png")

    #nawal
    social_insta_nawal = Button(about_us_frame, bg="#272244", image=insta_img, activebackground="#272244", relief=FLAT, bd=0, command = lambda : dev_links("Nawaldeep Singh","instagram"))
    social_insta_nawal.place(x=127, y=210, width= 35, height= 30)

    social_github_nawal = Button(about_us_frame, bg="#272244", image=git_img, activebackground="#272244", relief=FLAT, bd=0, command = lambda : dev_links("Nawaldeep Singh","github"))
    social_github_nawal.place(x=181, y=210, width= 35, height= 30)

    social_linkdin_nawal = Button(about_us_frame, bg="#272244", image=linkedin_img, activebackground="#272244", relief=FLAT, bd=0, command = lambda : dev_links("Nawaldeep Singh","linkedin"))
    social_linkdin_nawal.place(x=232, y=210, width= 35, height= 30)

    nawal_img = Label(about_us_frame, bg= "#272244", image= nawal_pic)
    nawal_img.place(x=130, y=55, width=120, height=120)
    nawal_label = Label(about_us_frame, bg= "#272244", fg="white", font= text_font, text = "Nawaldeep Singh")
    nawal_label.place(x=106, y=170, width=165, height=25)

    #ritish
    social_insta_ritish = Button(about_us_frame, bg="#272244", image=insta_img, activebackground="#272244", relief=FLAT, bd=0, command = lambda : dev_links("Ritish Jain","instagram"))
    social_insta_ritish.place(x=550, y=210, width= 35, height= 30)

    social_github_ritish = Button(about_us_frame, bg="#272244", image=git_img, activebackground="#272244", relief=FLAT, bd=0, command = lambda : dev_links("Ritish Jain","github"))
    social_github_ritish.place(x=604, y=210, width= 35, height= 30)

    social_linkdin_ritish = Button(about_us_frame, bg="#272244", image=linkedin_img, activebackground="#272244", relief=FLAT, bd=0, command = lambda : dev_links("Ritish Jain","linkedin"))
    social_linkdin_ritish.place(x=655, y=210, width= 35, height= 30)

    ritish_img = Label(about_us_frame, bg= "#272244", image= ritish_pic)
    ritish_img.place(x=550, y=55, width=120, height=120)
    ritish_label = Label(about_us_frame, bg= "#272244", fg="white", font= text_font, text = "Ritish Jain")
    ritish_label.place(x=529, y=170, width=165, height=25)


def bottomframe1():
    """mic command"""
    global keyboard_img
    global bottom_frame1
    global listening_img
    global listening_img2
    global reco_img
    global reco_img2
    global typemode_img
    global typemode_img2
    global listen_light_cyan
    global reco_light_green
    global typing_light_orange
    global command_status_label

    bottom_frame1=Frame(window, background="white")
    bottom_frame1.place(x=0, y=390, width=800, height=60)

    #setting font
    command_status_font= Font(family = "RocknRoll One", size = 15, weight='normal')

    ################################ Function code starts here #################

    keyboard_btn= Button(bottom_frame1, background="white", command=lambda : change_command_input_type_to("typing"), activebackground="white", borderwidth=0)
    keyboard_btn.place(x=25, y=5, width=50, height=50)
    keyboard_btn.config(image=keyboard_img)
    #to set the text agian
    keyboard_btn.bind("<Button-1>", lambda e:COMMAND_BOX.set("Type your Command..."))
    
    command_status_label = Label(bottom_frame1, background="#272244", font= command_status_font, foreground="#85D2BF", justify=CENTER, text="Connecting...")
    command_status_label.place(x=106, y=8, width=484, height=45)

    #used for listening
    listen_light_cyan = Label(bottom_frame1, background="white", image=listening_img)
    listen_light_cyan.place(x=623, y=8, width=40, height=40)

    #used for recognizing
    reco_light_green = Label(bottom_frame1, background="white", image=reco_img)
    reco_light_green.place(x=681, y=8, width=40, height=40)

    #used for typing in entry box
    typing_light_orange = Label(bottom_frame1, background="white", image=typemode_img)
    typing_light_orange.place(x=738, y=8, width=40, height=40)
 

    ################################ Function code ends here #################


def bottomframe2():
    """keyboard command"""
    global keyboard_img
    global bottom_frame2
    global listening_img
    global listening_img2
    global reco_img
    global reco_img2
    global typemode_img
    global typemode_img2
    global listen_light_cyan
    global reco_light_green
    global typing_light_orange

    bottom_frame2=Frame(window, background="white")
    bottom_frame2.place(x=0, y=390, width=800, height=60)

    #setting font
    entry_font= Font(family = "RocknRoll One", size = 15, weight='normal')

    ################################ Function code starts here #################
    global mic_img
    
    mic_btn= Button(bottom_frame2, background="white", command=lambda : change_command_input_type_to("audio"), activebackground="white", borderwidth=0)
    mic_btn.place(x=25, y=5, width=50, height=50)
    mic_btn.config(image=mic_img)


    
    command_status_entry = Entry(bottom_frame2, background="#272244", font=entry_font, foreground="#85D2BF", textvariable=COMMAND_BOX)
    command_status_entry.place(x=106, y=8, width=484, height=45)
    
    command_status_entry.bind("<FocusIn>", lambda e: focus_bar())
    command_status_entry.bind("<FocusOut>", lambda e:typing_light_orange.config(image=typemode_img))
    command_status_entry.bind("<Return>", lambda e:type_command())

    #used for listening
    listen_light_cyan = Label(bottom_frame2, background="white", image=listening_img)
    listen_light_cyan.place(x=623, y=8, width=40, height=40)

    #used for recognizing
    reco_light_green = Label(bottom_frame2, background="white", image=reco_img)
    reco_light_green.place(x=681, y=8, width=40, height=40)

    #used for typing in entry box
    typing_light_orange = Label(bottom_frame2, background="white", image=typemode_img)
    typing_light_orange.place(x=738, y=8, width=40, height=40)
    ################################ Function code ends here #################


#################################################################################
#################################-Window Code-###################################
#################################################################################
    
head_font = Font(family = "RocknRoll One", size = 25, weight='bold')
head_label = Label(
    window,
    background='white',
    text="Shaurya Assistant",
    font=head_font,
    foreground="#272244"
    )
head_label.place(x=200, y=5, width=360, height=55)


# #main screen buttons on header
    #bg images of buttons
about_us_img=PhotoImage(file = "./images/button images/About Us.png")
home_img=PhotoImage(file = "./images/button images/Home.png")
power_btn=PhotoImage(file = "./images/button images/power_btn.png")


    #Power button - Header
power_button = Button(window, image = power_btn, borderwidth=0, background="white", relief=FLAT, activebackground="white", command = close)
power_button.place(x=18,y=13, width=42, height = 42)

    #About-Us button
about_us_button = Button(window, image = about_us_img, borderwidth=0, background="white", relief=FLAT, activebackground="white", command= change_frame)
about_us_button.place(x=660,y=13, width=129, height = 42)

############################# window code #######################

aboutusframe()
mainframe()

#calling bottom frame as default
bottomframe1()

#turing mic on
set_device_status("mic", "on")
set_device_status("terminate", "off")
# time.sleep(2)

while fetch_device_status("terminate") == "on":
    pass

#listen command
listen_thread = Thread(target=listen_command, daemon=True)
listen_thread.start()

#code ends here
mainloop()