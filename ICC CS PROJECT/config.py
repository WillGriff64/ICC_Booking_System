import os, sys
import menu, dbconnect
from info import root, logo, pixel, userdetails
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def config():
    '''
    Displays a menu where the user can change important information regarding the company
    '''
    root.title("Change Important Info")
    for i in root.pack_slaves():
        i.destroy()

    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * from config")
    oldconfig = cursor.fetchone()
    connection.close()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Change Important Information", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    frame.rowconfigure(1, minsize=10)

    entries = []
    #Defines a list for every input box
    entryinfo = [["CEO Name:","ceo"],["Bank Account Number","banknum"],["Database Path","dbpath"],["Standard Booth Cost (per day):","sbcost"],["Large Booth Cost (per day):","lbcost"],["XL Booth Cost (per day):","xbcost"],["Water Utility Cost (per day):","watercost"],["Electricity Utility Cost (per day):","electricitycost"]]

    entryrow = 1
    entrycolumn = 0
    for i in entryinfo: #Creates an entry box for every item in the entryinfo list
        configLabel = Label(frame,text=i[0], font=("Calibri", 18)).grid(row=entryrow,column=0,sticky=W,columnspan=2)
        configEntry = Entry(frame, width=20, font=("Calibri", 24))
        configEntry.grid(row=entryrow,column=1,columnspan=2)
        configEntry.insert(0,oldconfig[i[1]])
        entries.append(configEntry)
        entryrow += 1

    buttonframe = LabelFrame(frame,highlightthickness=0,borderwidth=0)
    buttonframe.grid(row=entryrow+1,column=0)

    Confirm = Button(buttonframe, text="Confirm", command=lambda: infocheck(entries[0].get(),entries[1].get(),entries[2].get(),entries[3].get(),entries[4].get(),entries[5].get(),entries[6].get(),entries[7].get(),ErrorFrame), font=("Calibri", 18),image=pixel, width=220,compound="c",borderwidth=5)
    Confirm.grid(row=0,column=0)

    Cancel = Button(buttonframe, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=220,compound="c",borderwidth=5)
    Cancel.grid(row=0,column=1)

    ErrorFrame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    ErrorFrame.pack()

def infocheck(ceoname,banknum,dbpath,sbcost,lbcost,xbcost,watercost,electricitycost,ErrorFrame):

    '''
    Validates the new config info
    '''
    for i in ErrorFrame.grid_slaves():
        i.destroy()

    haserror = False

    if ceoname == "" or banknum == "" or dbpath == "" or sbcost == "" or lbcost == "" or xbcost == "" or watercost == "" or electricitycost == "" or ErrorFrame == "": #If any of the inputs are empty raise an error with the user
        error = "Data missing from input field"
        haserror = True
    else:
        numlist = [["Bank Account Number",banknum],["Standard Booth Cost (per day):",sbcost],["Large Booth Cost (per day):",lbcost],["XL Booth Cost (per day):",xbcost],["Water Utility Cost (per day):",watercost],["Electricity Utility Cost (per day):",electricitycost]]  #List of all entries that should be numbers
        for i in numlist:
            try:    #Checks if all entries in numlist an numbers
                float(i[1]) + 1
            except ValueError:
                error = str(i[0])+" Should be a number"
                haserror = True

    if haserror == False:   #If there is no error, save the new info and return to menu.
        connection, cursor = dbconnect.c()
        cursor.execute("DELETE FROM config")
        cursor.execute("INSERT INTO config (ceo, banknum, sbcost, lbcost, xbcost, dbpath, watercost, electricitycost) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ceoname,banknum,sbcost,lbcost,xbcost,dbpath,watercost,electricitycost))
        connection.commit()
        connection.close()
        menu.menu()
    else:
        errorLabel = Label(ErrorFrame, text=error, fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)
