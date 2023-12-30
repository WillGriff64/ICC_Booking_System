import os, sys, sqlite3, datetime
import dbconnect, menu
from tkcalendar import *
from info import dbname, root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def changeEvent():
    '''
    Displays a menu where the user can input an event password to allow them to change event details
    '''
    root.title("Change Event Details")
    for i in root.pack_slaves():
        i.destroy()

    #makes a frame that all assets are put in, then pack it to center everything+
    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Enter Event Password", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=3)

    eventpassword = Label(frame,text="Event Password:", font=("Calibri", 18)).grid(row=1,column=0,sticky=W)

    frame.rowconfigure(0, minsize=20)
    frame.rowconfigure(2, minsize=10)
    frame.rowconfigure(4, minsize=10)

    epInput = Entry(frame, width=20, font=("Calibri", 24))
    epInput.grid(row=1,column=1,columnspan=2,padx=(0,115))

    Confirm = Button(frame, text="Confirm", command=lambda: checkEvent(epInput.get(),errorbox), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=5,column=1,padx=(0,115))

    cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=100,compound="c",borderwidth=5)
    cancel.grid(row=5,column=0)

    errorbox = LabelFrame(root,highlightthickness=0,borderwidth=0)
    errorbox.pack()

def checkEvent(eventpass,errorbox):
    '''
    Checks the inputted event password to see if its valid
    '''
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT COUNT(1) as found from events WHERE eventpass=?", (eventpass,))
    eventtest = cursor.fetchone()["found"]
    if eventtest == 0:  #If it returns as 0, no event with that password was found
        errorLabel = Label(errorbox, text="No event found with this password", fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)
        connection.close()
    else:
        cursor.execute("SELECT * from events WHERE eventpass=?", (eventpass,))  #Grab the events information and move on to changedetails()
        eventdetails = cursor.fetchone()
        changedetails(eventdetails)

def changedetails(details):
    '''
    Displays the screen that allows the user to change an events details
    '''
    for i in root.pack_slaves():
        i.destroy()

    #Creates a frame for all assets to be put inside
    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    #Creates a title label
    titleLabel = Label(frame, text="Change Event Details", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)

    #Row/column configures to make the screen look better
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(6, minsize=20)
    frame.columnconfigure(3, minsize=20)

    nameLabel = Label(frame,text="Event Name:", font=("Calibri", 18)).grid(row=2,column=0,sticky=W)
    lengthLabel = Label(frame,text="Event Length (days):", font=("Calibri", 18)).grid(row=3,column=0,sticky=W)

    nInput = Entry(frame, width=20, font=("Calibri", 24))
    nInput.grid(row=2,column=1,columnspan=2)
    LInput = Entry(frame, width=20, font=("Calibri", 24))
    LInput.grid(row=3,column=1,columnspan=2)
    nInput.insert(0,details["eventname"])   #Inserts the pre-existing information into the input boxes
    LInput.insert(0,details["length"])      #x2

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=2,column=4,rowspan=4)

    booked = datetime.datetime.strptime(details["date"],"%Y-%m-%d").date()

    cal = Calendar(frame, selectmode="day", year=booked.year, month=booked.month, day=booked.day, date_pattern="mm/dd/yyyy")
    cal.grid(row=5,column=0,columnspan=2,rowspan=4,sticky=W)

    connection, cursor = dbconnect.c()
    eventID = details["id"]
    cursor.execute("SELECT * from events where id != ?", (eventID,))
    eventlist = cursor.fetchall()   #Returns a list of all booked events
    for i in eventlist:     #Displays each booked event in the calendar
        startdate = i["date"]
        elen = i["length"]
        current = startdate
        current = datetime.datetime.strptime(current, "%Y-%m-%d").strftime("%m/%d/%Y")
        current = datetime.datetime.strptime(current, "%m/%d/%Y").date()
        for j in range(int(elen)):
            cal.calevent_create(current,i["eventname"],tags=[" "])
            current = current + datetime.timedelta(days=1)
    connection.close()

    cal.tag_config(" ", background='red', foreground='white')

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=9,column=0)
    Confirm = Button(frame, text="Confirm", command=lambda: newDetailCheck(nInput.get(),LInput.get(),cal.get_date(),cal,entryError,details), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=9,column=1,columnspan=2)

    frame.rowconfigure(4, minsize=5)

    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def newDetailCheck(name,length,booked,cal,entryError,details):
    '''
    Validates the newly inputted information
    '''
    for i in entryError.grid_slaves():
        i.destroy()

    booked = datetime.datetime.strptime(booked,"%m/%d/%Y").date()

    name = name.lower()
    name = name.strip()
    length = length.strip()
    error = ""
    haserror = False

    #Check input data
    if name == "" or length == "": #Check for missing input fields
        error = "Data missing from input field"
        haserror = True
    elif booked < datetime.datetime.today().date(): #Check if chosen date is in the past
        error = "must enter a date after today"
        haserror = True
    else:
        try:
            int(length)
        except ValueError:
            error = "length must be a whole number" #Ensure that the event length is a number
            haserror = True
        else:
            if int(length) <= 0: #Check that the event length is at least 1 day long
                error = "event length must be at least 1 day long"
                haserror = True
            elif int(length) > 99: #Check that event length is no longer than 99 days long
                error = "event cant be longer than 99 days"
                haserror = True
            else:
                for i in range(int(length)):
                    daycheck = booked + datetime.timedelta(days=i)
                    check = list(cal.get_calevents(date=daycheck))
                    if check:
                        error = "Selected date already has a booking"
                        haserror = True
                        break

    if haserror == False:   #If no errors, moves on to next screen
        appendDeets(name,booked,length,details)
    else:   #Displays any errors to the user
        errorLabel = Label(entryError, text=error, fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)

def appendDeets(name,booked,length,details):
    '''
    saves the updated information to the database
    '''
    eventid = details["id"]
    connection, cursor = dbconnect.c()
    cursor.execute("UPDATE events SET eventname = ? WHERE id = ?", (name,eventid))
    cursor.execute("UPDATE events SET date = ? WHERE id = ?", (booked,eventid))
    cursor.execute("UPDATE events SET length = ? WHERE id = ?", (length,eventid))
    connection.commit()
    connection.close()
    menu.menu()
