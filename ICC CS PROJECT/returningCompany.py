import os, sys, sqlite3
import menu, dbconnect, bookbooth
from info import dbname, root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def returningCompany():
    '''
    Displays a menu where the user can input details to select the correct company
    '''
    root.title("Returning Company")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Returning Company", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(6, minsize=20)
    frame.columnconfigure(3, minsize=20)

    #Creating labels and inputs for host info
    nameLabel = Label(frame,text="Company name", font=("Calibri", 18)).grid(row=2,column=0,sticky=W, columnspan=2)

    nInput = Entry(frame, width=20, font=("Calibri", 24))
    nInput.grid(row=2,column=1,columnspan=2)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=2,column=4,rowspan=4)

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=7,column=0)
    Confirm = Button(frame, text="Confirm", command=lambda: checkCompany(nInput.get(),entryError), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=7,column=1,columnspan=2)
    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def checkCompany(name,entryError):
    '''
    Checks if the company is on file, if there is more than one with the same name move onto multiCompany
    '''
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT COUNT(1) from companies WHERE name=?", (name,)) #searches for existing hosts using the data that was input
    logtest = cursor.fetchone()
    logtest = logtest["COUNT(1)"]
    if logtest == 1: #If there is 1 host then it will continue like normal
        cursor.execute("SELECT id from companies WHERE name=?", (name,))
        companyID = cursor.fetchone()
        companyID = companyID["id"]
        connection.close()
        bookbooth.chooseEvent(companyID)
    elif logtest > 1: #If more than one host with the same name is found it will then move to multiHost()
        connection.row_factory = lambda cursor, row: row[0]
        cursor = connection.cursor()
        cursor.execute("SELECT postcode from companies WHERE name=?", (name,))
        postlist = cursor.fetchall()
        connection.close()
        multiCompany(postlist)
    else: #If no host is found there has been an error
        errorLabel = Label(entryError, text="Invalid company name", fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)

def multiCompany(postlist):
    '''
    Displays a list of every postcode to let the user select the correct one
    '''
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()
    titleLabel = Label(frame, text="Select Your Companies Postcode", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    buttonrow = 1

    #Creates a button for every phone number found.
    for i in postlist:
        bname = Button(frame, text=str(i), command=lambda postcode=i: companyIDparse(postcode), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5) #Creates the button
        bname.grid(row=buttonrow,column=0) #Add button to grid
        buttonrow += 1 #increase row number for next button

    #Adding button to cancel, logo and row padding
    frame.rowconfigure(buttonrow, minsize=20)
    Cancel = Button(frame, text="Cancel", command=lambda: returningCompany(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=buttonrow+1,column=0)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=1,column=1,rowspan=999)

#Takes phone number from multiHost and gives newEvent the correct ID
def companyIDparse(postcode):
    '''
    Selects all of the company info and passes it to the book booth
    '''
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * from companies WHERE postcode = ?", (postcode,))
    companyInfo = cursor.fetchone()
    companyID = companyInfo["id"]
    connection.close()
    bookbooth.chooseEvent(companyID)
