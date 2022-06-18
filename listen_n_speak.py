############################# USER-DEFINED MODULES ####################################
import network
from utility.my_pickles import *
from utility.clean_temp import clean_cache
############################# PRE-DEFINED MODULES ####################################
import speech_recognition as sr
import pyttsx3 as tts
import sys
############################# FUNCTIONS ####################################


def listen(command_status_label=None, status_labels=None, imgs=None, time=None, return_back= None):
    """Listen for the mic input and convert it to a command and also returns the formatted command for ease but returns None if network is not connected or some other error helds"""
    clean_cache()
    if network.isConnected() == True:     
        listener = sr.Recognizer()
        listener.dynamic_energy_threshold = False
        listener.energy_threshold = 4000

        with sr.Microphone() as mic:
            listener.adjust_for_ambient_noise(mic)

            print("\nListening...")
            if status_labels !=None:
                status_lights(status_labels, imgs, active_task = "listening")
            if command_status_label != None:
                command_status_label.config(text= "Listening...")
            audio = listener.listen(mic)
    else:
        if command_status_label != None:
            command_status_label.config(text = "You are not connected to Network")
        time.sleep(2)
        return ""

    # try:
    if network.isConnected() == True:
        if status_labels != None:
            status_lights(status_labels, imgs, active_task = "recognizing")
        if command_status_label != None:
            command_status_label['text'] = "Recognizing..."
            print("\nRecognizing...")
        query = listener.recognize_google(audio, language = "en-in")
        query = query.lower()

        if "shaurya" in query:
            listwords = query.split(" ")
            sh_index = listwords.index("shaurya")
            for index in range(0,sh_index):
                try:
                    listwords.remove(listwords[index])
                except:
                    continue
        if command_status_label != None:
            command_status_label.config(text = "Command Processed...")
        print("\ncommand output...")
        return (query)
    else:
        statement = "You are not connected to network"
        if command_status_label != None:
            command_status_label.config(text = "You are not connected to Network")
        speak(statement)
        time.sleep(2)
        sys.exit()
    # except:
    #     print(Exception)
    #     statement = "Didn't get it right now...\nPlease try agian"
    #     speak(statement)
    #     return None


#id and volume changing feature must be added afterwords using picke
#getid() and getvolume() must be defined here

    
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



#assigning status light images
def status_lights(labels, imgs, active_task = None):
    """change the lights on or off"""
    #   listening_img          ->imgs[0]
    #   listening_img2         ->imgs[1]
    #   reco_img               ->imgs[2]
    #   reco_img2              ->imgs[3]

    #   listen_light_cyan      ->labels[0]
    #   reco_light_green       ->labels[1]

    if active_task == "listening":
        labels[0].config(image = imgs[1] )
        labels[1].config(image = imgs[2] )

    elif active_task == "recognizing":
        labels[0]['image']= imgs[0]
        labels[1]['image']= imgs[3]

    else:
        labels[0]['image']= imgs[0]
        labels[1]['image']= imgs[2]
