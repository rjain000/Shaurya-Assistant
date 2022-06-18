from tkinter import *


def timer():
    root = Tk()
    root.title("Timer")
    root.iconbitmap("sounds/images/timer.ico")
    w_width, w_height = 300, 150
    s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
    root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))
    root['bg'] = 'white'

    Label(root, text="Time's Up", font=("Arial Bold", 20), bg='white').pack(pady=20)
    Button(root, text="  OK  ", font=("Arial", 15), relief=FLAT, bg='#14A769', fg='white', command=lambda:quit()).pack()
    
    root.mainloop()

timer()