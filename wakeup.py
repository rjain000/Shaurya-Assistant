import os
from listen_n_speak import listen
from tkinter import *
from tkinter import PhotoImage
from tkinter.font import Font
from PIL import ImageTk, ImageSequence, Image
from threading import Thread
import time


wakeup = False
WAKE_COMMAND = ['breakup', 'break up', 'stright up']

def filter_command(query):
    for corr in WAKE_COMMAND:
        if corr in query:
            query= query.replace(corr, "wake up")
            break
    return query

def listening():
    global wakeup
    global window
    while wakeup == False:
        command= listen()
        print(command)
        query = filter_command(command)
        print(query)
        if "wake up" in query or "wake-up" in query or "wakeup" in query:
            os.startfile(os.getcwd()+"/Shaurya.py")
            wakeup = True




def gifimg(label, imgs, refresh_rate=0):
    """Animation : Play Gifs"""
    print("gifimg() called....")
    global wakeup
    
    while wakeup == False:
        for img in ImageSequence.Iterator(imgs):
            img_frame = ImageTk.PhotoImage(img)
            label.config(image = img_frame)
            window.update()
            time.sleep(0.06)
    window.destroy()


window = Tk()
window.title("Shaurya - Personal Asssistant")
window.config(background="white")
window.geometry("768x300+350+250")
window.resizable(0,0)
window.overrideredirect(True)



text_font = Font(family = "RocknRoll One",size = 16, weight='bold')
btn_font = Font(family = "RocknRoll One",size = 16, weight='bold')

text_label=Label(window, background="white", text = "Wake Me Up !", fg="#3f9ae1", font= text_font)
text_label.place(x=134, y=10, width=500, height=35)

close_btn = Button(window, bg="#3f9ae1", fg="white", activebackground="#3f9ae1", activeforeground="white", text = "X", font = btn_font, relief= FLAT, command = window.destroy, bd=0)
close_btn.place(x=718, y=5, width=52, height=25)

Thread(target= listening).start()

giflabel=Label(window, background="white")
giflabel.place(x=0, y=56, width=768, height=244)

imgpath = "./images/gifs/sleeping_mode.gif"
resolution = (768,244)
imgs=Image.open(imgpath)
imgs.resize(resolution)

gifimg(giflabel, imgs)

window.mainloop()