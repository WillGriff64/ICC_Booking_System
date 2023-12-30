import os, sys, sqlite3
import newUser, login, backups, bookbooth, changeEvent, config, timetable, popupmessage, Invoices
from info import root, logo, pixel, userdetails
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image


def menu():
    '''
    Dsilays the menu where the user can navigate to different parts of the program
    '''
    dyntitle = str("Welcome "+userdetails["username"])  #Creates a dynamic title using the users username
    root.title(dyntitle)
    for i in root.pack_slaves():
        i.destroy()

    #Defines each button (name,function)
    staffbuttons = [["Book a Booth",lambda: popupmessage.popupmessage("Have you ever booked a booth with\nICC wales before?",2,"Yes","No",None,"returningCompany.returningCompany()","newCompany.newCompany()",None)],["Change Event Details",lambda: changeEvent.changeEvent()],["Manage Event Invoices",lambda: Invoices.invoicemenu("event")],["Manage Booth Invoices",lambda: Invoices.invoicemenu("booth")]]
    adminbuttons = [["Create New User",lambda: newUser.newUser(False)],["Create New Event",lambda: popupmessage.popupmessage("Have you ever organized an event with\nICC wales before?",2,"Yes","No",None,"returningHost.returningHost()","newHost.newHost()",None)],["Change Important Info",lambda: config.config()],["View Event Timetable",lambda: timetable.timetable()]]

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Menu", font=("Calibri", 40)).grid(row=0, column=0, sticky=W)

    def buttonmaker(buttonlist,columnchoice):
        '''
        Takes a list of buttons and creates them
        '''
        count = 0
        for i in buttonlist:
            count +=1
            menubutton = Button(frame, text=i[0], command=i[1], font=("Calibri", 18),image=pixel, width=300,compound="c",borderwidth=5)
            menubutton.grid(row=count,column=columnchoice)

    frame.columnconfigure(1, minsize=10)
    frame.rowconfigure(5, minsize=20)
    menubutton = Button(frame, text="Log Out", command=lambda: login.login(), font=("Calibri", 18),image=pixel, width=300,compound="c",borderwidth=5)
    menubutton.grid(row=6,column=0)

    buttonmaker(staffbuttons,0)
    if userdetails["accountlevel"] == 1:    #If the user is an admin, create the buttons only the admin accounts have access to
        buttonmaker(adminbuttons,2)
        menubutton = Button(frame, text="Manage Backups", command=lambda: backups.backups(), font=("Calibri", 18),image=pixel, width=300,compound="c",borderwidth=5)
        menubutton.grid(row=6,column=2)
    else:   #Otherwise just create a logo image
        logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
        logoLabel.grid(row=1,column=2,rowspan=4)
