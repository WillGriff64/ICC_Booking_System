import os, sys, sqlite3
import dbconnect, menu
from info import dbname, root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def chooseEvent(companyID):
    '''
    Displays a screen for the user to input an event password
    '''
    root.title("Book a Booth")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Enter Event Password", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    pInput = Entry(frame, width=20, font=("Calibri", 24))
    pInput.grid(row=2,column=0,columnspan=2)

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=7,column=0)

    Confirm = Button(frame, text="Confirm", command=lambda: checkEvent(pInput.get(),entryError,companyID), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=7,column=1,columnspan=2)

    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def checkEvent(eventpass,entryError,companyID):
    '''
    Checks the event password the user has inputted and finds the corresponding event
    '''
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * FROM events WHERE eventpass = ?", (eventpass,))    #Selects all events with a matching event password
    Einfo = cursor.fetchone()
    connection.close()
    if Einfo != None:   #If the retunred information is NOT empty, an event has been found and we can continue to booking a booth
        bookbooth(Einfo,companyID)
    else:
        errorLabel = Label(entryError, text="Event with password not found.", fg="red", font=("Calibri", 16))   #If no event is found display an error message to the user
        errorLabel.grid(row=0,column=0)

def bookbooth(Einfo,companyID):
    '''
    Displays the event layout and allows the user to select and book a booth
    '''
    for i in root.pack_slaves():
        i.destroy()

    #Defines each layout (Each list inside layout is a row, each entry inside the row lists is a grid space, so S would be a standard booth, l a large booth, and "" an empty space)
    if Einfo["layout"] == 1:
        Layout = [["s","s","s","st","","","","","","s","s","s"],["","","","","","","","","","","",""],["s","","","","","","","","","","","s"],["s","","l","","l","","l","","l","","","s"],["s","","l","","l","","l","","l","","","s"],["","","","","","","","","","","",""],["s","s","s","s","","","","","s","s","s","s"]]
    elif Einfo["layout"] == 2:
        Layout = [["l","","l","","l","","l","","l","","l",""],["","","","","","","","","","","",""],["s","","s","s","","xl","","","s","s","","s"],["s","","s","s","","","","","s","s","","s"],["s","","s","s","","","","","s","s","","s"],["","","","","","","","","","","",""],["s","s","s","s","","","","","s","s","s","s"]]
    elif Einfo["layout"] == 3:
        Layout = [["l","","","st","","","","","","","l",""],["","","","","","","","","","","",""],["s","","","","","","","","","","","s"],["s","","xl","","s","","","s","xl","","","s"],["s","","","","s","","","s","","","","s"],["s","","","","","","","","","","","s"],["s","","l","","","","","","l","","","s"]]

    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * FROM booths WHERE eventid = ?",(Einfo["id"],))
    boothlist = cursor.fetchall()

    boothframe = LabelFrame(root,highlightthickness=0,borderwidth=4)
    boothframe.pack()

    brow = 0
    bcolumn = 0
    boothnum = 0

    chosen = StringVar(root, 0)

    #This for loop draws the events layout
    for i in Layout:
        boothframe.rowconfigure(brow, minsize=50)
        for j in i:     #This loop handles each row of the event layout
            boothframe.columnconfigure(bcolumn, minsize=50)
            if boothlist[boothnum]["companyid"] == None:    #If the booth is already booked, dont allow the user to book it again
                isbooked = "normal"
            else:
                isbooked = "disabled"
            if j == "s":    #If an S is found display a standard booth
                boothbutton = Radiobutton(boothframe, state=isbooked, variable = chosen, value = boothlist[boothnum]["id"], indicator = 0, text="b"+str(boothlist[boothnum]["id"]), font=("Calibri", 18),image=pixel, width=50,compound="c",borderwidth=5)
                boothbutton.grid(row=brow,column=bcolumn)
                boothnum += 1
            elif j == "l":  #If an l is found display a large booth
                boothbutton = Radiobutton(boothframe, state=isbooked, variable = chosen, value = boothlist[boothnum]["id"], indicator = 0, text="b"+str(boothlist[boothnum]["id"]), font=("Calibri", 18),image=pixel, width=100,compound="c",borderwidth=5)
                boothbutton.grid(row=brow,column=bcolumn,columnspan=2)
                boothnum += 1
            elif j == "xl":  #if an xl is found display an extra large booth
                boothbutton = Radiobutton(boothframe, state=isbooked, variable = chosen, value = boothlist[boothnum]["id"], indicator = 0, text="\nb"+str(boothlist[boothnum]["id"])+"\n", font=("Calibri", 18),image=pixel, width=100,compound="c",borderwidth=5)
                boothbutton.grid(row=brow,column=bcolumn,columnspan=2,rowspan=2)
                boothnum += 1
            elif j == "st":  #if an st is found display a stage
                stage = LabelFrame(boothframe,highlightthickness=0,borderwidth=5,relief="solid")
                stage.grid(row=brow,column=bcolumn,columnspan=6,rowspan=2)
                stagelabel = Label(stage, text="Stage", font=("Calibri", 20)).pack(padx=150,pady=50)
            bcolumn += 1    #Increase the column by one for the next booth
        brow += 1   #increase the booth row by one for the next row
        bcolumn = 0 #reset the column value for the new row

    #Frames are being made to simplify the organisation of tkinter buttons
    optionframe = LabelFrame(root,highlightthickness=0,borderwidth=0)
    optionframe.pack()

    checkframe = LabelFrame(optionframe,highlightthickness=0,borderwidth=0)
    checkframe.grid(row=0,column=0)
    buttonframe = LabelFrame(optionframe,highlightthickness=0,borderwidth=0)
    buttonframe.grid(row=0,column=2)

    errorframe = LabelFrame(root,highlightthickness=0,borderwidth=0)
    errorframe.pack()

    #Creating the water and electric checkboxes
    iswater = IntVar()
    iselectric = IntVar()

    water = Checkbutton(checkframe, text="Water",font=("Calibri", 18),variable=iswater)
    water.grid(row=0,column=0)
    electric = Checkbutton(checkframe, text="Electricity",font=("Calibri", 18),variable=iselectric)
    electric.grid(row=0,column=1)

    titlelabel = Label(optionframe, text="Select a Booth", font=("Calibri", 25)).grid(row=0,column=1,padx=10)

    #Cancel button creation
    Cancel = Button(buttonframe, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=100,compound="c",borderwidth=5)
    Cancel.grid(row=0,column=0)

    #confirm button creation
    Confirm = Button(buttonframe, text="Confirm", command=lambda: confirmbook(chosen.get(),iswater.get(),iselectric.get(),companyID,errorframe), font=("Calibri", 18),image=pixel, width=100,compound="c",borderwidth=5)
    Confirm.grid(row=0,column=1)



def confirmbook(boothID,iswater,iselectric,companyid,errorframe):
    '''
    Saves and updates the selected booth as saved
    '''
    for i in errorframe.grid_slaves():
        i.destroy()

    if boothID == "0":    #if boothID is 0 no booth was selected by the user
        errorLabel = Label(errorframe, text="Please select a booth above", fg="red", font=("Calibri", 16))  #Display a message asking the user to select a booth
        errorLabel.grid(row=0,column=0)
    else:
        connection, cursor = dbconnect.c()
        cursor.execute("UPDATE booths SET companyid = ?, iswater = ?, iselectric = ? WHERE id = ?",(companyid,iswater,iselectric,boothID)) #Save the new booth information according to what the user selected
        connection.commit()
        connection.close()
        menu.menu()
