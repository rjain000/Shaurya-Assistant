######################################-PRE-DEFINED MODULES-############################
import time
import os
from tkinter import *
from typing import final
from bs4 import BeautifulSoup
import requests
import webbrowser
from youtube_search import YoutubeSearch
from datetime import datetime, date
from time import sleep
import re
import playsound
from tkinter import *
import imaplib as imap
from keyboard import press_and_release
import email as imap_email
import psutil
import wmi
######################################-USER-DEFINED MODULES-############################
from Applications.web import web_open
from Applications.database import *
from network import isConnected
from utility import sys_info
import listen_n_speak as lns
#########################-FUNCTIONS ON SHAURYA-##########################


def search_bar(search_content):
    web_open(search_content)


###################################-ALARM CODE-###############################

def check_alarm(alarm_img_label, alarm_label_imgs, alarm_label_info):
    # imgs[0] ----> not active
    # imgs[1] ----> active
    status_return = True
    while status_return:
        try:
            alarms = fetch_alarms()
            if alarms == None:
                alarm_img_label['image'] = alarm_label_imgs[0]
                # alarm_label_info['text'] = "Alarm Off"
                time.sleep(3)
            else:
                alarm_img_label['image'] = alarm_label_imgs[1]
                alarm_label_info['text'] = "Alarm On"
                time.sleep(3)

                latest_alarm = get_first_alarm()

                if latest_alarm != None and latest_alarm[-1] == 'stop':
                    os.startfile(r""+os.getcwd()+"\Applications\\ring_alarm.py")
                    print(
                        "*********************************software started**********************")
                    change_alarm_status(
                        set_state="running",
                        alarm_name=latest_alarm[0],
                        status=latest_alarm[1],
                        time=latest_alarm[2],
                        daylight=latest_alarm[3],
                        date=latest_alarm[4],
                        )
        except:
            pass
        finally:
            if fetch_device_status("terminate") == "on":
                print("Check Alarm function ends")
                status_return = False
                return ""


def get_IOT_Box_status(plug1datalist, plug2datalist):
    # list[0]     ----> label
    # list[1]     ----> imgs 1 on
    # list[2]     ----> imgs 2 off
    # list[3]     ----> status
    
    status_return = True
    while status_return:
        try:
            req_status1 = str(requests.get('http://192.168.1.220/plug1status'))
            req_status2 = str(requests.get('http://192.168.1.220/plug2status'))

            #########plug1 status########
            if(req_status1=="<Response [201]>"):
                plug1datalist[0]['image'] = plug1datalist[2]
                plug1datalist[3]['text'] = "Plug 1 Off"
                
            elif (req_status1=="<Response [202]>"):
                plug1datalist[0]['image'] = plug1datalist[1]
                plug1datalist[3]['text'] = "Plug 1 On"
                

            #######plug2 status########
            if(req_status2=="<Response [201]>"):
                plug2datalist[0]['image'] = plug2datalist[2]
                plug2datalist[3]['text'] = "Plug 2 Off"
                
            elif (req_status2=="<Response [202]>"):
                plug2datalist[0]['image'] = plug2datalist[1]
                plug2datalist[3]['text'] = "Plug 2 On"
            
        except:
            plug1datalist[0]['image'] = plug1datalist[2]
            plug1datalist[3]['text'] = "Detecting..."
            plug2datalist[0]['image'] = plug2datalist[2]
            plug2datalist[3]['text'] = "Detecting..."

        finally:
            if fetch_device_status("terminate") == "on":
                print("IOT Plugs fun end")
                status_return = False
                return ""

        # time.sleep(2)


def get_IOT_status(light_datalist, fan_datalist):
    status_return = True
    while status_return:
        try:
            ##########-board-###########
            req_statusLight = str(requests.get('http://192.168.1.222/plug1status'))
            req_statusFan = str(requests.get('http://192.168.1.222/plug2status'))

            ########-LIGHT status-##########
            if(req_statusLight=="<Response [201]>"):
                light_datalist[0]['image'] = light_datalist[2]
                light_datalist[3]['text'] = "Light Off"
                
            elif (req_statusLight=="<Response [202]>"):
                light_datalist[0]['image'] = light_datalist[1]
                light_datalist[3]['text'] = "Light On"

            #######FAN status########
            if(req_statusFan=="<Response [201]>"):
                fan_datalist[0]['image'] = fan_datalist[2]
                fan_datalist[3]['text'] = "Fan Off"
                
            elif (req_statusFan=="<Response [202]>"):
                fan_datalist[0]['image'] = fan_datalist[1]
                fan_datalist[3]['text'] = "Fan On"
        
        except:
            light_datalist[0]['image'] = light_datalist[2]
            light_datalist[3]['text'] = "Detecting..."
            fan_datalist[0]['image'] = fan_datalist[2]
            fan_datalist[3]['text'] = "Detecting..."
        
        finally:
            if fetch_device_status("terminate") == "on":
                print("IOT baord fun end")
                status_return = False
                return ""

        # time.sleep(2)


def temprature_check(temp_label):
    search = "temperature in Amritsar"
    url = f"https://www.google.com/search?q={search}"
    status_return = True
    while status_return:
        try:
            r = requests.get(url)
            data= BeautifulSoup(r.text, "html.parser")
            temp = data.find ("div", class_="BNeawe").text
            temp_label['text'] = f"Temp {temp}"
            time.sleep(10)
        except:
            pass
        finally:
            if fetch_device_status("terminate") == "on":
                print('Temprature Function Ends')
                status_return = False
                return ""


def check_mail(label, imgs, info_label):
    mails = get_mails()
    time.sleep(1)
    if mails == None or mails == []:
        info_label['text'] = "Add Mail"
    else:
        mails = get_mails()
        mail_id= mails[0][0]
        password= mails[0][1]
        try:
            mail_obj = imap.IMAP4_SSL('imap.gmail.com','993')
            mail_obj.login(mail_id, password)
            status_return = True
            while status_return:
                time.sleep(3)
                try:
                    mail_obj.select("Inbox")
                    status, msgnums = mail_obj.search(None, "unseen")
                    mail_counter = msgnums[0].split()

                    if len(mail_counter)<1:
                        label['image']=imgs[1]
                        info_label['text'] = "No Mails"

                    elif len(mail_counter)>= 1:
                        label['image']=imgs[0]
                        info_label['text'] = f"Mails({len(mail_counter)})"

                    mail_obj.close()

                except:
                    info_label['text'] = "No Internet"

                finally:
                    if fetch_device_status("terminate") == "on":
                        print('Check mail Function ends')
                        status_return = False
                        return ""
        except:
            info_label['text'] = "Add Mails"
            time.sleep(2)
            check_mail(label, imgs, info_label)
            


def read_mail():
    days = {"Sun":"Sunday", "Mon":"Monday", "Tue":"Tuesday", "Wed":"Wednesday", "Thu":"Thursday", "Thur":"Thursday", "Fri":"Friday","Sat":"Saturday"}
    mail_cred = get_mails()
    time.sleep(0.5)
    if mail_cred == None:
        lns.speak("You have not setup Your mail...Please Say Setup Mail to setup your gmail")    
    else:
        mail_id= mail_cred[0][0]
        password= mail_cred[0][1]

        try:
            mail_obj = imap.IMAP4_SSL('imap.gmail.com','993')
            mail_obj.login(mail_id, password)
            mail_obj.select("Inbox")
            status, msgnums = mail_obj.search(None, "unseen")
            mails = msgnums[0].split()

            if len(mails)<1:
                lns.speak("No New Mails Available")

            elif len(mails)>= 1:
            
                if len(mails) == 1:
                    statement = "You have a new mail in your inbox"
                    lns.speak(statement)


                elif len(mails) > 1:
                    statement = f"You have {len(mails)} unread messages"
                    lns.speak(statement)

                for mail in range(0,len(mails)):
                    if len(mails)==1:
                        statement = "Reading mail"
                    else:
                        statement = f"Reading mail {mail+1}...."

                    lns.speak(statement)

                    rc, data = mail_obj.fetch(mails[mail], "(RFC822)")
                    message = imap_email.message_from_bytes(data[0][1])

                    parts = message.get('From')
                    parts = parts.replace("<","")
                    parts = parts.replace(">","")
                    sender = parts
                    parts = parts.split(" ")

                    sender = sender.replace(parts[-1],"")

                    statement = f"Mail from : {sender}"
                    print(statement)
                    lns.speak(statement)


                    statement = f"Mail from Email ID : {parts[-1]}"
                    print(statement)
                    lns.speak(statement)


                    statement = f"Date of mail : {message.get('Date')}"
                    part = message.get('Date').split(" ")
                    day = part[0].replace(",","")
                    statement = statement.replace(day, days[day])
                    statement = statement.replace(part[-1],"")
                    print(statement)
                    lns.speak(statement)

                    subject = message.get('Subject')

                    if subject == '':
                        statement = "No Subject Found For This Email"
                    else:
                        statement = f"Subject : {subject}"
                    lns.speak(statement)

                    statement = "Message in Mail :"
                    lns.speak(statement)

                    for msg_data in message.walk():
                        if msg_data.get_content_type() == "text/plain":
                            mailbody = msg_data.as_string().replace("Content-Type: text/plain; charset=\"UTF-8\"","")
                            lns.speak(mailbody)

            mail_obj.close()
        except:
            statement = "Not able to connect to mail server"
            lns.speak(statement)



def youtube(query):
    query = query.replace('play',' ')
    query = query.replace('on youtube',' ')
    query = query.replace('youtube',' ')
    results = YoutubeSearch(query,max_results=1).to_dict()
    webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
    return "Enjoy Sir..."


##########-To Do List-####################
file = "txtfiles/toDoList.txt"

def createList():
    f = open(file,"w")
    present = datetime.now()
    dt_format = present.strftime("Date: " + "%d/%m/%Y"+ " Time: " + "%H:%M:%S" + "\n")
    f.write(dt_format)
    f.close()

def toDoList(text):
    if os.path.isfile(file) == False:
        createList()

    f = open(file,"r")
    x = f.read(8)
    f.close()
    y = x[6:]
    yesterday = int(y)
    present = datetime.now()
    today = int(present.strftime("%d"))
    if (today-yesterday) >= 1:
        createList()
    f = open(file,"a")
    dt_format = present.strftime("%H:%M")
    print(dt_format)
    f.write(f"[{dt_format}] : {text}\n")
    f.close()

def showtoDoList():
    if os.path.isfile(file)==False:
        return ["It looks like that list is empty"]
    
    f = open(file, 'r')
    
    items = []
    for line in f.readlines():
        items.append(line.strip())

    speakList = [f"You have {len(items)-1} items in your list:"]
    for i in items[1:]:
        speakList.append(' at ')
        speakList.append(i.capitalize())
    return speakList

###########-Timer-#######################
def startTimer(query):
    nums = re.findall(r'[0-9]+', query)
    time = 0
    if "minute" in query and "second" in query:
        time = int(nums[0])*60 + int(nums[1])
    elif "minute" in query:
        time = int(nums[0])*60
    elif "second" in query:
        time = int(nums[0])
    else: return

    print("Timer Started")
    sleep(time)
    os.startfile('timer.py')
    playsound.playsound("sounds/audios/Timer.mp3")


#########-NEWS-#########################
from bs4 import BeautifulSoup

def latestNews(news=5):
    URL = 'https://indianexpress.com/latest-news/'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    headlineLinks = []
    headlines = []

    divs = soup.find_all('div', {'class':'title'})

    count=0
    for div in divs:
        count += 1
        if count>news:
            break
        a_tag = div.find('a')
        headlineLinks.append(a_tag.attrs['href'])
        headlines.append(a_tag.text)

    # return headlines,headlineLinks
    return headlines


def jokes():
    URL = 'https://icanhazdadjoke.com/'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    try:
        p = soup.find('p')
        return p.text
    except Exception as e:
        raise e


def googleSearch(query):
    if 'image' in query:
        query += "&tbm=isch"
    query = query.replace('images','')
    query = query.replace('image','')
    query = query.replace('search','')
    query = query.replace('show','')
    webbrowser.open("https://www.google.com/search?q=" + query)
    return "Here you go..."

def gamesOption():
    list_game="Let's Play Game... For Tic Tac Toe speak option one and for Mind Game speak Option two"
    print(list_game)
    lns.speak(list_game)
    option=lns.listen()
    if "one" in option or "1" in option or "first" in option or "tic tac toe" in option:
        webbrowser.open("https://rjain000.github.io/Tic-Tac-Toe/")
        return("please wait let me setup for tic tac toe")

    elif "second" in option or "2" in option or "two" in option or "too" in option or "to" in option or "Mind game" in option:
        webbrowser.open("https://rjain000.github.io/memorygame/")
        return("please wait let me setup for mind game")

#################-MAPS-###############################
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

def giveDirections(startingPoint, destinationPoint):
    geolocator = Nominatim(user_agent='assistant')
    if 'current' in startingPoint:
        res = requests.get("https://ipinfo.io/")
        data = res.json()
        startinglocation = geolocator.reverse(data['loc'])
    else:
        startinglocation = geolocator.geocode(startingPoint)

    destinationlocation = geolocator.geocode(destinationPoint)
    startingPoint = startinglocation.address.replace(' ', '+')
    destinationPoint = destinationlocation.address.replace(' ', '+')

    openWebsite('https://www.google.co.in/maps/dir/'+startingPoint+'/'+destinationPoint+'/')

    startinglocationCoordinate = (startinglocation.latitude, startinglocation.longitude)
    destinationlocationCoordinate = (destinationlocation.latitude, destinationlocation.longitude)
    total_distance = great_circle(startinglocationCoordinate, destinationlocationCoordinate).km #.mile
    return str(round(total_distance, 2)) + 'KM'

def maps(text):
    text = text.replace('maps', '')
    text = text.replace('map', '')
    text = text.replace('google', '')
    openWebsite('https://www.google.com/maps/place/'+text)

def openWebsite(url='https://www.google.com/'):
    webbrowser.open(url)


class COVID:
    def __init__(self):
        self.total = 'Not Available'
        self.deaths = 'Not Available'
        self.recovered = 'Not Available'
        self.totalIndia = 'Not Available'
        self.deathsIndia = 'Not Available'
        self.recoveredIndia = 'Not Available'

    def covidUpdate(self):
        URL = 'https://www.worldometers.info/coronavirus/'
        result = requests.get(URL)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')

        temp = []
        divs = soup.find_all('div', class_='maincounter-number')
        for div in divs:
            temp.append(div.text.strip())
        self.total, self.deaths, self.recovered = temp[0], temp[1], temp[2]

    def covidUpdateIndia(self):
        URL = 'https://www.worldometers.info/coronavirus/country/india/'
        result = requests.get(URL)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')

        temp = []
        divs = soup.find_all('div', class_='maincounter-number')
        for div in divs:
            temp.append(div.text.strip())
        self.totalIndia, self.deathsIndia, self.recoveredIndia = temp[0], temp[1], temp[2]

    def totalCases(self,india_bool):
        if india_bool: return self.totalIndia
        return self.total

    def totalDeaths(self,india_bool):
        if india_bool: return self.deathsIndia
        return self.deaths

    def totalRecovery(self,india_bool):
        if india_bool: return self.recoveredIndia
        return self.recovered

    def symptoms(self):
        symt = ['1. Fever',
                '2. Coughing',
                '3. Shortness of breath',
                '4. Trouble breathing',
                '5. Fatigue',
                '6. Chills, sometimes with shaking',
                '7. Body aches',
                '8. Headache',
                '9. Sore throat',
                '10. Loss of smell or taste',
                '11. Nausea',
                '12. Diarrhea']
        return symt

    def prevention(self):
        prevention = ['1. Clean your hands often. Use soap and water, or an alcohol-based hand rub.',
                        '2. Maintain a safe distance from anyone who is coughing or sneezing.',
                        '3. Wear a mask when physical distancing is not possible.',
                        '4. Donâ€™t touch your eyes, nose or mouth.',
                        '5. Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.',
                        '6. Stay home if you feel unwell.',
                        '7. If you have a fever, cough and difficulty breathing, seek medical attention.']
        return prevention

def dataUpdate():
    c.covidUpdate()
    c.covidUpdateIndia()

c = COVID()
dataUpdate()

def covid(query):
    
    if "india" in query: india_bool = True
    else: india_bool = False

    if "statistic" in query or 'report' in query:
        return f"Here are the statistics...Total cases:  {c.totalCases(india_bool)}... Total Recovery:  {c.totalRecovery(india_bool)}... Total Deaths: {c.totalDeaths(india_bool)}"

    elif "symptom" in query:
        return ["Here are the Symptoms...", c.symptoms()]

    elif "prevent" in query or "measure" in query or "precaution" in query:
        return ["Here are the some of preventions from COVID-19:", c.prevention()]
    
    elif "recov" in query:
        return "Total Recovery is: " + c.totalRecovery(india_bool)
    
    elif "death" in query:
        return "Total Deaths are: " + c.totalDeaths(india_bool)
    
    else:
        return "Total Cases are: " + c.totalCases(india_bool)
        

#################-MATHS-###############################

import math

def basicOperations(text):
    if 'root' in text:
        temp = text.rfind(' ')
        num = int(text[temp+1:])
        return round(math.sqrt(num),2)

    text = text.replace('plus', '+')
    text = text.replace('minus', '-')
    text = text.replace('x', '*')
    text = text.replace('multiplied by', '*')
    text = text.replace('multiply', '*')
    text = text.replace('divided by', '/')
    text = text.replace('to the power', '**')
    text = text.replace('power', '**')
    result = eval(text)
    return round(result,2)

def bitwiseOperations(text):
    if 'right shift' in text:
        temp = text.rfind(' ')
        num = int(text[temp+1:])
        return num>>1
    elif 'left shift' in text:
        temp = text.rfind(' ')
        num = int(text[temp+1:])
        return num<<1
    text = text.replace('and', '&')
    text = text.replace('or', '|')
    text = text.replace('not of', '~')
    text = text.replace('not', '~')
    text = text.replace('xor', '^')
    result = eval(text)
    return result

def conversions(text):
    temp = text.rfind(' ')
    num = int(text[temp+1:])
    if 'bin' in text:
        return eval('bin(num)')[2:]
    elif 'hex' in text:
        return eval('hex(num)')[2:]
    elif 'oct' in text:
        return eval('oct(num)')[2:]

def trigonometry(text):
    temp = text.replace('degree','')
    temp = text.rfind(' ')
    deg = int(text[temp+1:])
    rad = (deg * math.pi) / 180
    if 'sin' in text:
        return round(math.sin(rad),2)
    elif 'cos' in text:
        return round(math.cos(rad),2)
    elif 'tan' in text:
        return round(math.tan(rad),2)

def factorial(n):
    if n==1 or n==0: return 1
    else: return n*factorial(n-1)

def isHaving(text, lst):
    for word in lst:
        if word in text:
            return True
    return False

def perform(text):
    text = text.replace('math','')
    if "factorial" in text: 
        return str(factorial(int(text[text.rfind(' ')+1:])))
    elif isHaving(text, ['sin','cos','tan']): 
        return str(trigonometry(text))
    elif isHaving(text, ['bin','hex','oct']): 
        return str(conversions(text))
    elif isHaving(text, ['shift','and','or','not']): 
        return str(bitwiseOperations(text))
    else: 
        return str(basicOperations(text))


#############-OPEN-###############
def browser(command):
    """ Controls the browser activity"""
    print(command)
    command = command.replace('open', '')
    command = command.replace(' ', '')
    command = command.replace('shaurya', '')
    openWebsite(f'https://{command}')
    print(f"{command} opened")
    lns.speak(f"{command} opened")

def windowAuto(command):
    quey = str(command)
    if 'open setting' in quey:
        lns.speak("opening setting")
        press_and_release('windows + i')
    elif 'open search' in quey:
        press_and_release('windows + s')
    elif 'open file explorer' in quey:
        lns.speak("opening File explorer")
        press_and_release('windows + e')
    elif 'open run' in quey:
        lns.speak("opening run")
        press_and_release('windows + r')
    else:
        browser(command)

###########################-IOT on/off-#######################################
def turn_IOT(command):
    """ Turn IoT device on or off """
    if 'turn on plug 1' in command or 'turn on plug one' in command or 'plug 1 on' in command or 'plug one on' in command:
        try:
            status = str(requests.get('http://192.168.1.220/plug1status'))
            if "<Response [201]>" == status:
                requests.get('http://192.168.1.220/plug1on')
                lns.speak('Plug 1 ON!')
            elif "<Response [202]>" == status:
                lns.speak('Plug one is already on')
        except:
            lns.speak('Not connected to internet.')

    elif 'turn plug 2 on' in command or 'turn plug to on' in command or 'plug 2 on' in command or 'plug to on' in command or 'plug too on' in command or 'turn on plug too' in command or 'turn on plug 2' in command or 'turn on plug to' in command:
        try:
            status= str(requests.get('http://192.168.1.220/plug2status'))
            if "<Response [201]>" == status:
                requests.get('http://192.168.1.220/plug2on')
                lns.speak('Plug 2 ON!')
            elif "<Response [202]>" == status:
                lns.speak('Plug two is already on')
        except:
            lns.speak('Not connected to internet.')

    elif 'turn plug 1 off' in command or 'turn plug one off' in command or 'plug 1 off' in command or 'plug one off' in command or 'turn off plug 1' in command or 'turn off plug one' in command or 'turn of plug 1' in command:
        try:
            status = str(requests.get('http://192.168.1.220/plug1status'))
            if "<Response [201]>" == status:
                lns.speak('Plug one is already off')
            elif "<Response [202]>" == status:
                requests.get('http://192.168.1.220/plug1off')
                lns.speak('Plug 1 OFF!')
        except:
            lns.speak('Not connected to internet.')
    
    elif 'turn off plug 2' in command or 'turn off plug to' in command or 'plug 2 off' in command or 'plug to off' in command or 'plug too off' in command:
        try:
            status= str(requests.get('http://192.168.1.220/plug2status'))
            if "<Response [201]>" == status:
                lns.speak('Plug two is already off')
            elif "<Response [202]>" == status:
                requests.get('http://192.168.1.220/plug2off')
                lns.speak('Plug 2 OFF!')
        except:
            lns.speak('Not connected to internet.')
    
    elif 'turn on light' in command or 'light on' in command:
        try:
            status= str(requests.get('http://192.168.1.222/plug1status'))
            if "<Response [201]>" == status:
                requests.get('http://192.168.1.222/plug1on')
                lns.speak('Light is on!')
            elif "<Response [202]>" == status:
                lns.speak("Light is already on")
        except:
            lns.speak('Not connected to internet.')
            
    elif 'turn on fan' in command or 'fan on' in command:
        try:
            status= str(requests.get('http://192.168.1.222/plug2status'))
            if "<Response [201]>" == status:
                requests.get('http://192.168.1.222/plug2on')
                lns.speak('Fan is on!')
            elif "<Response [202]>" == status:
                lns.speak('Fan is already on')
        except:
            lns.speak('Not connected to internet.')
    
    elif 'turn off light' in command or 'light off' in command:
        try:
            status = str(requests.get('http://192.168.1.222/plug1status'))
            if "<Response [201]>" == status:
                lns.speak('Light is already off')
            elif "<Response [202]>" == status:
                requests.get('http://192.168.1.222/plug1off')
                lns.speak('Light is off!')
        except:
            lns.speak('Not connected to internet.')   
    
    elif 'turn off fan' in command or 'fan off' in command:
        try:
            status= str(requests.get('http://192.168.1.222/plug2status'))
            if "<Response [201]>" == status:
                lns.speak('Fan is already off')
            elif "<Response [202]>" == status:
                requests.get('http://192.168.1.222/plug2off')
                lns.speak('Fan is off!')
        except:
            lns.speak('Not connected to internet.')

    elif('turn on all plug' in command or 'turn on all devices' in command):
        statu1 = 1
        statu2 = 1
        try:
            requests.get('http://192.168.1.220/plug1on')
            requests.get('http://192.168.1.220/plug2on')
        except:
            statu1 = 0
        try:
            requests.get('http://192.168.1.222/plug1on')
            requests.get('http://192.168.1.222/plug2on')
        except:
            statu2 = 0
        
        if statu1 == 1 and statu2 == 1:
            lns.speak('All Plugs ON!')
        elif statu1==1 and statu2 == 0:
            lns.speak('Plugs are on but light and fan are not connected to internet')
        elif statu1 == 0 and statu2 == 1:
            lns.speak('Light and fan are on but plugs are not connected to intenet')
        else:
            lns.speak('Devices are not connected to internet')

    elif('turn off all plug' in command or 'turn off all device' in command):
        statu1 = 1
        statu2 = 1
        try:
            requests.get(f'http://192.168.1.220/plug1off')
            requests.get(f'http://192.168.1.220/plug2off')
        except:
            statu1 = 0
        try:
            requests.get(f'http://192.168.1.222/plug1off')
            requests.get(f'http://192.168.1.222/plug2off')
        except:
            statu2 = 0
        
        if statu1 == 1 and statu2 == 1:
            lns.speak('All Plugs OFF!')
        elif statu1==1 and statu2 == 0:
            lns.speak('Plugs are off but light and fan are not connected to internet')
        elif statu1 == 0 and statu2 == 1:
            lns.speak('Light and fan are off but plugs are not connected to internet')
        else:
            lns.speak('Devices are not connected to internet')

def battery_level():
    battery = psutil.sensors_battery()
    if battery.power_plugged:
        lns.speak(f"Battery status, Charging")
    lns.speak(f"Battery level is {battery.percent} %")
    

def my_system_info():
    c = wmi.WMI()  
    my_system_1 = c.Win32_LogicalDisk()[0]
    my_system_2 = c.Win32_ComputerSystem()[0]
    lns.speak(f"cpu usage is {int(psutil.cpu_percent(0.5))} %")
    lns.speak(f"memory usage is {int(psutil.virtual_memory()[2])} %")
    battery_level()
    lns.speak(f"Total Disk Space for windows is {str(round(int(my_system_1.Size)/(1024**3),2))} GB")
    lns.speak(f"Free Disk Space is {str(round(int(my_system_1.Freespace)/(1024**3),2))} GB")
    lns.speak(f"Device Model is {my_system_2.Manufacturer} {my_system_2. Model}")


def time_today():
    real_time = time.strftime("%I:%M %p")
    lns.speak(f"Time is {real_time}")

def day_today():
    days={0:"Monday", 1:"Tuesday",2:"Wednesday", 3:"Thursday",4:"Friday", 5:"Saturday",6:"Sunday"}
    present_date = date.today()
    day_of_week = present_date.weekday()
    return days[day_of_week]    

def date_today():
    date = datetime.now()
    day = day_today()
    present_date = date.strftime(f"%d %m {date.year}")
    lns.speak(f"Today date is {present_date} {day}")

def date_time():
    date_today()
    time_today()

def network():
    if isConnected() == True:
        lns.speak("You are connected to network")
    else:
        lns.speak("You are not connected to the network")

def temp():
    search = "temperature in Amritsar"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data= BeautifulSoup(r.text, "html.parser")
    temp = data.find ("div", class_="BNeawe").text
    return temp