#################################-PRE-DEFINED MODULES-############################
import json #for dict
from difflib import get_close_matches #to find close match
from pynput.keyboard import Controller
import time
from threading import Thread
import playsound
import random
#################################-USER-DEFINED MODULES-###########################
import network
import listen_n_speak as lns
from utility.sys_info import *
import features
import os
from Applications.database import *
import listen_n_speak as lns
#####################################-GLOBAL VARIABLES-################################

IP=[['what', 'is', 'my', 'ip'],['what', 'my', 'ip'],["whats","ip", 'my']]
system_volume_up = [["system","volume","up"],["system","volume", "increase"]]
system_volume_down = [["system","volume","down"],["system","decrease","volume"]]
system_volume_mute = [["system","volume","mute"],["system","decrease","mute"]]
system_volume_unmute = [["system","volume","unmute"],["system","decrease","unmute"],['system','volume','and mute']]
alarm = [["set", "alarm"], ["add", "alarm"]]
send_mail = [["send", "mail"], ["send", "mails"], ["sender", "mail"], ["sender", "mails"]]
read_mail = [["read", "mail"], ["read", "mails"], ["update", "mails"]]
OPEN = ['open']
yt = [['search','on youtube'],['on','youtube']]
sendWA = [['send','whatsapp'],['whatsapp']]
TDLM = [['add','in','to do list'],['make','to do list'],['remember']]
TDLR = [['what','is in to do list'],['show','to do list']]
TIMER = [['set','timer','of'],['timer','of'],['set','timer','for']]
NEWS = [['latest','news'],['news']]
JOKE = [['jokes'],['joke']]
GOOGLE = [['search','on','google']]
GAME = [['i','am','bored'],['game'],['i','feeling','bored'],['i','feeling','boring'],['flip','coin'],['toss','coin'],['roll','dice']]
MAPS = [['direction'],['directions'],['destination']]
MAP = [['where','is']]
COVID19 = [['covid'],['covid 19']]
CALCULATOR = [['calculate'],['perform']]
TYPE = [['start typing'],['type'],['typing']]
IOT = [['turn','on'],['turn','off'],['turn','of'],['turn','plug'],['turn','device'],['turn','light'],['turn','fan'],['plug'],['light'],['fan']]
SYSTEM_INFO = [["system","info"],["system","information"],["system","configration"],["system","details"]]
BATTERY = [["battery","info"],["battery","information"],["battery","level"],["battery","status"],['battery','percentage']]
TIME = [["time","what"], ["time","whats"],['time','today'],["tell","time"]]
DATE = [["date","what","today"], ["date","whats","the"],['date','today'],["tell","date"]]
DATE_AND_TIME=[["time","date","what"], ["time","date","whats"],['time','today',"date"],["tell","time","date"]]
NETWORK_STATUS=[["network","status"],['internet','connected'],['am','i','connected','network'],['network','connected']]
ADD_MAIL=[['add',"mail"],['new','mail','add'],['save','mail'],["set", "mail"], ["set", "mails"], ["setup", "mail"], ["setup", "mails"]]
TEMP = [['temperature'],['temp'],['weather'],['whether']]

#############################-Functions-###########################################


def typing():
    lns.speak("Listening in 2 seconds")
    keyboard = Controller()
    from keyboard import press_and_release
    stop = False
    while stop == False:
        try:
            string = lns.listen()
            if "stop type" in string or "stop typing" in string or "top typing" in string:
                stop = True
                lns.speak("Typing mode off.")
                return ''
            elif "hit enter" in string:
                press_and_release('enter')

            elif "space bar" in string:
                press_and_release('spacebar')

            elif "hit backspace" in string:
                press_and_release('backspace')

            elif string != None:
                print(string)
                text = string + ' '
                for char in text:
                    keyboard.type(char)
                    time.sleep(0.02)
        except:
            lns.speak('Restarting typing mode.. or say stop typing')
            typing()


######################################-MAIN FUNCTIONS-##################################
def filter_command(command):
    """ REMOVE SHAURYA KEYWORD AND BEFORE UNNESSERY WORDS FROM COMMAND """
    wordlist = command.split(" ")
    index=0
    while index<len(wordlist):
        if wordlist[index]!="shaurya":
            wordlist.remove(wordlist[index])
            index=0
            continue
        wordlist.remove(wordlist[0])
        command=" ".join(wordlist)
        return command


def incommand(lists, command):
    found= True
    for list in lists:
        found= True
        for val in list:
            if val not in command:
                found=False
                break
        if found == True:            
            return found


def statement(string):
    print(string)
    lns.speak(string)

counter = 0
data = json.load(open("Dictionary.json"))
data = json.load(open("Dictionary.json"))

def find_best_match(word):
    global data
    word.lower()
    if len(get_close_matches(word, data.keys())) > 0:
        action = get_close_matches(word, data.keys())[0]
    else:
        action = word

    return(action)


def supporting_functions(command, counter = 0):
    """calling instances (shaurya in command)"""
    #global variables
    global IP
    global NETWORK_STATUS
    global system_volume_up
    global system_volume_down
    global system_volume_mute
    global system_volume_unmute
    global alarm
    global send_mail
    global yt
    global sendWA
    global TDLM
    global TDLR
    global TIMER
    global NEWS
    global JOKE
    global GOOGLE
    global GAME
    global MAPS
    global MAP
    global COVID19
    global CALCULATOR
    global OPEN
    global IOT
    global SYSTEM_INFO
    global BATTERY
    global TIME
    global DATE
    global DATE_AND_TIME
    global ADD_MAIL
    global TEMP


    print(f"calling main_functions({command})")

    #function
    if incommand(IP, command):
        print("command to be processed : ", command)
        ip_address = network.myIP()
        statement(f"your IP Address is {ip_address}")

    elif incommand (IOT, command):
        print("command to be processed : ", command)
        features.turn_IOT(command)

    elif incommand(NETWORK_STATUS, command):
        print("command to be processed : ", command)
        if network.isConnected() == True:
            statement("You are connected to network")
        else:
            statement("You are not connected to the network")

    elif incommand(system_volume_up, command):
        print("command to be processed : ", command)
        system_volume_control(up=True)

    elif incommand(system_volume_down, command):
        print("command to be processed : ", command)
        system_volume_control(down=True)

    elif incommand(system_volume_unmute, command):
        print("command to be processed : ", command)
        system_volume_control(unmute=True)

    elif incommand(system_volume_mute, command):
        print("command to be processed : ", command)
        system_volume_control(mute=True)

    elif incommand(alarm, command):
        print("command to be processed : ", command)
        os.startfile(r""+os.getcwd()+"\Applications\\set_alarm.py")

    elif incommand(read_mail, command):
        print("command to be processed : ", command)
        features.read_mail()

    elif incommand(send_mail, command):
        print("command to be processed : ", command)
        statement('opening mail client')
        os.startfile(r""+os.getcwd()+"\Applications\\mail_sender.py")

    
    elif incommand(TYPE, command):
        print("command to be processed : ", command)
        set_device_status("mic", "off")
        typing()
        set_device_status("mic", "on")
    
    elif incommand(yt, command):
        command = command.replace('on youtube',' ')
        command = command.replace('search',' ')
        print("command to be processed : ", command)
        stat = features.youtube(command)
        statement(stat)

    elif incommand(sendWA, command):
        print("command to be processed : ", command)
        statement('opening whatsapp client')
        os.startfile(r""+os.getcwd()+"\Applications\\whatsapp.py")

    elif incommand(TDLM, command):
        command = command.replace('make',' ')
        command = command.replace('remember',' ')
        command = command.replace('to do list',' ')
        command = command.replace('add in',' ')
        print("command to be processed : ", command)
        features.toDoList(command)
        lns.speak('Task recorded!!')

    elif incommand(TDLR, command):
        command = command.replace('what','')
        command = command.replace('what to do','')
        command = command.replace('to do list', '')
        print("command to be processed : ", command)
        stat = features.showtoDoList()
        statement(stat)

    elif incommand(TIMER, command):
        command = command.replace('set timer of','')
        command = command.replace('timer','')
        command = command.replace('set','')
        command = command.replace('for','')
        print("command to be processed : ", command)
        statement(f"timer set for {command}")
        Thread(target=features.startTimer, args=(command,)).start()

    elif incommand(NEWS, command):
        print("command to be processed : ", command)
        stat = features.latestNews()
        count = 1
        for i in stat:
            statement(f"HEADLINE {count}")
            count+=1
            statement(i)

    elif incommand(JOKE, command):
        print("command to be processed : ", command)
        statement(features.jokes())
    
    elif incommand(GOOGLE, command):
        print("command to be processed : ", command)
        command = command.replace('search about','')
        command = command.replace('searh','')
        command = command.replace('google','')
        command = command.replace('search on google','')
        statement(features.googleSearch(command))

    elif incommand(GAME, command):
        print("command to be processed : ", command)
        set_device_status("mic", "off")
        if 'roll' in command and 'dice' in command:
            statement("Rolling the dice...")
            playsound.playsound("sounds/audios/dice.mp3")
            result = random.randint(1, 6)
            statement(f"You got number {result}")
        elif 'coin' in command and 'toss' in command or 'flip a coin' in command:
            statement("Tossing the coin...")
            playsound.playsound("sounds/audios/coin.mp3")
            result = random.choice(['Heads','Tails'])
            statement(f'You got {result}')
        else:
            statement(features.gamesOption())
        set_device_status("mic", "on")

    elif incommand(MAPS, command):
        set_device_status("mic", "off")
        print("command to be processed : ", command)
        lns.speak("Please tell the starting point")
        startingPoint = lns.listen()
        lns.speak("Please tell the destination point")
        destinationPoint = lns.listen()
        features.giveDirections(startingPoint, destinationPoint)
        lns.speak(f'Here We go!! direction from {startingPoint} to {destinationPoint}')
        set_device_status("mic", "on")

    elif incommand(MAP, command):
        print("command to be processed : ", command)
        command = command.replace('where','')
        command = command.replace('is','')
        features.maps(command)
        statement(f'{command} on google maps')

    elif incommand(COVID19, command):
        print("command to be processed : ", command)
        statement(features.covid(command))

    elif incommand(CALCULATOR, command):
        command = command.replace('calculate','')
        command = command.replace('perform','')
        print("command to be processed : ", command)
        statement(features.perform(command))
    
    elif incommand (SYSTEM_INFO, command):
        print("command to be processed : ", command)
        features.my_system_info()

    elif incommand (BATTERY, command):
        print("command to be processed : ", command)
        features.battery_level()

    elif incommand (DATE_AND_TIME, command):
        print("command to be processed : ", command)
        features.date_time()

    elif incommand (DATE, command):
        print("command to be processed : ", command)
        features.date_today()

    elif incommand (TIME, command):
        print("command to be processed : ", command)
        features.time_today()

    elif incommand (ADD_MAIL, command):
        print("command to be processed : ", command)
        os.startfile(r""+os.getcwd()+"\Applications\\mailsetup.py")
    
    elif incommand (TEMP, command):
        print("command to be processed : ", command)
        statement(f"Temprature is {features.temp()}")
    
    else:
        if counter == 0:
            c_list = command.split(" ")
            new_command=""
            for word in c_list:
                new_word = find_best_match(word)
                new_command = f"{new_command} {new_word}"

            supporting_functions(new_command, counter= 1)
        else:
            pass
            

def main_functions(command, counter=0):
    """calling features of instances (shaurya not in command)"""
    print(f"calling supporting_functions({command})")
    global OPEN
    if incommand(OPEN, command):
        print("command to be processed : ", command)
        features.windowAuto(command)
    else:
        if counter == 0:
            c_list = command.split(" ")
            new_command=""
            for word in c_list:
                new_word = find_best_match(word)               
                new_command = f"{new_command} {new_word}"

            main_functions(new_command, counter= 1)
        else:
            pass
    

def mycommand(command):
    """Takes command from shaurya"""
    print("commander is active...")
    print("command =", command)
    if 'shaurya' in command:
        command= filter_command(command)
        main_functions(command)
    else:
        supporting_functions(command)
