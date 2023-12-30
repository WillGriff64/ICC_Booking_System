import os, sys, sqlite3
import menu, dbconnect, newEvent
from info import dbname, root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def returningHost():
    '''
    Displays a menu where the user inputs the returning host's information
    '''
    root.title("Returning Host")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Returning Host", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(6, minsize=20)
    frame.columnconfigure(3, minsize=20)

    #Creating labels and inputs for host info
    nameLabel = Label(frame,text="Enter your name", font=("Calibri", 18)).grid(row=2,column=0,sticky=W, columnspan=2)
    surnameLabel = Label(frame,text="First Name:", font=("Calibri", 18)).grid(row=3,column=0,sticky=W)
    phoneLabel = Label(frame,text="Surname:", font=("Calibri", 18)).grid(row=4,column=0,sticky=W)

    nInput = Entry(frame, width=20, font=("Calibri", 24))
    nInput.grid(row=3,column=1,columnspan=2)
    sInput = Entry(frame, width=20, font=("Calibri", 24))
    sInput.grid(row=4,column=1,columnspan=2)


    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=2,column=4,rowspan=4)

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=7,column=0)
    Confirm = Button(frame, text="Confirm", command=lambda: checkHost(nInput.get(),sInput.get(),entryError), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=7,column=1,columnspan=2)
    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def checkHost(name,surname,entryError):
    '''
    Validates and checks the info, if there is more than one host with the same name, move onto multiHost
    '''
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT COUNT(1) from hosts WHERE name=? AND surname = ?", (name,surname)) #searches for existing hosts using the data that was input
    logtest = cursor.fetchone()
    logtest = logtest["COUNT(1)"]
    if logtest == 1: #If there is 1 host then it will continue like normal
        cursor.execute("SELECT id from hosts WHERE name=? AND surname = ?", (name,surname))
        hostID = cursor.fetchone()
        hostID = hostID["id"]
        connection.close()
        newEvent.newEvent(hostID)
    elif logtest > 1: #If more than one host with the same name is found it will then move to multiHost()
        connection.row_factory = lambda cursor, row: row[0]
        cursor = connection.cursor()
        cursor.execute("SELECT phone from hosts WHERE name=? AND surname=?", (name,surname))
        phonelist = cursor.fetchall()
        connection.close()
        multiHost(phonelist)
    else: #If no host is found there has been an error
        errorLabel = Label(entryError, text="Invalid name / surname", fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)

def multiHost(phonelist):
    '''
    Displays the phone number for every host with the same name and lets the user select the correct one
    '''
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()
    titleLabel = Label(frame, text="Select Your Phone Number", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    buttonrow = 1

    #Creates a button for every phone number found.
    for i in phonelist:
        phonepart = str(str(i)[0:3]+"******"+str(i)[len(str(i))-3:len(str(i))+1]) #Creates an obfuscated number to be displayed
        bname = Button(frame, text=phonepart, command=lambda phone=i: hostIDparse(phone), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5) #Creates the button
        bname.grid(row=buttonrow,column=0) #Add button to grid
        buttonrow += 1 #increase row number for next button

    #Adding button to cancel, logo and row padding
    frame.rowconfigure(buttonrow, minsize=20)
    Cancel = Button(frame, text="Cancel", command=lambda: returningHost(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=buttonrow+1,column=0)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=1,column=1,rowspan=999)

#Takes phone number from multiHost and gives newEvent the correct ID
def hostIDparse(phone):
    '''
    retrieves the host informaion and passes it to the new event function
    '''
    phone = int(phone)
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * from hosts WHERE phone = ?", (phone,))
    hostInfo = cursor.fetchone()
    hostID = hostInfo["id"]
    connection.close()
    newEvent.newEvent(hostID)
