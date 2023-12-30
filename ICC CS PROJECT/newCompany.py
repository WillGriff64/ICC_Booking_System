import os, sys, sqlite3
import dbconnect, menu, bookbooth
from info import dbname, root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def newCompany():
    '''
    Dsiplays the menu where the user can input the information for a new company
    '''
    root.title("New Company")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="New Company", font=("Calibri", 40)).grid(row=0, column=0, sticky=W, columnspan=3)
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(6, minsize=20)
    frame.columnconfigure(3, minsize=20)

    nameLabel = Label(frame,text="Company Name:", font=("Calibri", 18)).grid(row=2,column=0,sticky=W)
    phoneLabel = Label(frame,text="Phone Number:", font=("Calibri", 18)).grid(row=3,column=0,sticky=W)
    emailLabel = Label(frame,text="Email:", font=("Calibri", 18)).grid(row=4,column=0,sticky=W)
    postcodeLabel = Label(frame,text="Postcode:", font=("Calibri", 18)).grid(row=5,column=0,sticky=W)

    nInput = Entry(frame, width=20, font=("Calibri", 24))
    nInput.grid(row=2,column=1,columnspan=2)
    pInput = Entry(frame, width=20, font=("Calibri", 24))
    pInput.grid(row=3,column=1,columnspan=2)
    eInput = Entry(frame, width=20, font=("Calibri", 24))
    eInput.grid(row=4,column=1,columnspan=2)
    poInput = Entry(frame, width=20, font=("Calibri", 24))
    poInput.grid(row=5,column=1,columnspan=2)


    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=2,column=4,rowspan=4)

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=7,column=0)
    Confirm = Button(frame, text="Confirm", command=lambda: addNewCompany(nInput.get(),pInput.get(),eInput.get(),poInput.get(),entryError), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=7,column=1,columnspan=2)

    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def addNewCompany(name,phone,email,postcode,entryError):
    '''
    Validates the company information and if it passes adds it to the database
    '''
    for i in entryError.grid_slaves():
        i.destroy()

    error = ""
    haserror = False

    #Check input data
    try:
        int(phone)+1
    except ValueError:
        error = "Phone number must be a valid number"
        haserror = True
    if name == "" or phone == "" or email =="" or postcode == "":
        error = "Data missing from input field"
        haserror = True
    elif "@" not in email:
        error = "Not a valid email"
        haserror = True

    #adds data to database
    if haserror == False:
        connection, cursor = dbconnect.c()
        cursor.execute("INSERT INTO companies (name, phone, email, postcode) VALUES (?, ?, ?, ?)", (name, phone, email, postcode))
        connection.commit()
        cursor.execute("SELECT id from companies WHERE name=? AND phone = ?", (name,phone))
        companyinfo = cursor.fetchone()
        companyID = companyinfo["id"]
        connection.close()
        bookbooth.chooseEvent(companyID)
    else:
        #creates the error message
        errorLabel = Label(entryError, text=error, fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)
