import os, sys, sqlite3
import dbconnect, menu, newEvent
from info import dbname, root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def newHost():
    '''
    Displays a menu where the user can inpt information for a new host
    '''
    root.title("New Host")
    for i in root.pack_slaves():
        i.destroy()

    #Creates the tkinter assets

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="New Host", font=("Calibri", 40)).grid(row=0, column=0, sticky=W)
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(6, minsize=20)
    frame.columnconfigure(3, minsize=20)

    nameLabel = Label(frame,text="Name:", font=("Calibri", 18)).grid(row=2,column=0,sticky=W)
    surnameLabel = Label(frame,text="Surname:", font=("Calibri", 18)).grid(row=3,column=0,sticky=W)
    phoneLabel = Label(frame,text="Phone:", font=("Calibri", 18)).grid(row=4,column=0,sticky=W)
    emailLabel = Label(frame,text="Email:", font=("Calibri", 18)).grid(row=5,column=0,sticky=W)

    nInput = Entry(frame, width=20, font=("Calibri", 24))
    nInput.grid(row=2,column=1,columnspan=2)
    sInput = Entry(frame, width=20, font=("Calibri", 24))
    sInput.grid(row=3,column=1,columnspan=2)
    pInput = Entry(frame, width=20, font=("Calibri", 24))
    pInput.grid(row=4,column=1,columnspan=2)
    eInput = Entry(frame, width=20, font=("Calibri", 24))
    eInput.grid(row=5,column=1,columnspan=2)


    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=2,column=4,rowspan=4)

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=7,column=0)
    Confirm = Button(frame, text="Confirm", command=lambda: addNewHost(nInput.get(),sInput.get(),pInput.get(),eInput.get(),entryError), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=7,column=1,columnspan=2)

    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def addNewHost(name,surname,phone,email,entryError):
    '''
    Validates and adds the host to the database
    '''
    for i in entryError.grid_slaves():
        i.destroy()

    error = ""
    haserror = False

    #Check input data
    try:
        int(phone)+1    #Checks to make sure that the phone is a number
    except ValueError:
        error = "Phone number must be a valid number"
        haserror = True
    if name == "" or surname == "" or phone =="" or email == "":    #Checks if any of the inputs are empty
        error = "Data missing from input field"
        haserror = True
    elif "@" not in email:  #Checks if the email has an @ sumbol in it
        error = "Not a valid email"
        haserror = True


    if haserror == False:   #If there are no errors, add them to the database
        connection, cursor = dbconnect.c()
        cursor.execute("INSERT INTO hosts (name, surname, phone, email) VALUES (?, ?, ?, ?)", (name, surname, phone, email))
        connection.commit()
        cursor.execute("SELECT id from hosts WHERE name=? AND surname = ? AND phone = ?", (name,surname,phone))
        hostinfo = cursor.fetchone()
        hostID = hostinfo["id"]
        connection.close()
        newEvent.newEvent(hostID)
    else:   #If there is an error, display it
        #creates the error message
        errorLabel = Label(entryError, text=error, fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)
