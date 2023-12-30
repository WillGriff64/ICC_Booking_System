import os, sys
import backups, bookbooth, changeEvent, dbconnect, login, menu, newHost, returningHost, newCompany, returningCompany
from info import root, logo, pixel, userdetails
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def popupmessage(message,type,button1,button2,button3,bo1,bo2,bo3):
    '''
    Creates a popup message depending on the input
    '''
    popup = Toplevel()
    popup.title("Alert")
    popup.attributes("-topmost", True)
    #Window size
    w = 440
    h = 150
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
    popupframe = LabelFrame(popup,highlightthickness=0,borderwidth=0)
    popupframe.pack()
    popup.resizable(False, False)

    if type == 1:   #popup type 1 has only one button
        messagelabel = Label(popupframe, text=message, font=("Calibri", 14)).grid(row=0,column=0)
        messagebutton = Button(popupframe, text=button1, command=eval("popup.destroy" if bo1 is None else bo1), font=("Calibri", 14),image=pixel, width=200,compound="c",borderwidth=5)
        popupframe.rowconfigure(1, minsize=10)
        messagebutton.grid(row=2,column=0)

    elif type == 2: #popup type 2 has 2 buttons
        messagelabel = Label(popupframe, text=message, font=("Calibri", 14)).grid(row=0,column=0,columnspan=3)
        b1 = Button(popupframe, text=button1, command=lambda:[popup.destroy(),eval(bo1)], font=("Calibri", 14),image=pixel, width=200,compound="c",borderwidth=5)
        b2 = Button(popupframe, text=button2, command=lambda:[popup.destroy(),eval(bo2)], font=("Calibri", 14),image=pixel, width=200,compound="c",borderwidth=5)
        popupframe.rowconfigure(1, minsize=40)
        popupframe.columnconfigure(1, minsize=10)
        b1.grid(row=2,column=0)
        b2.grid(row=2,column=2)

    #Code is modular so adding more types for future projects / other applications is not difficult
