import os, sys, sqlite3, datetime, random, string
import dbconnect, menu
from tkcalendar import *
from info import dbname, root, logo, pixel, l1img, l2img, l3img
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def newEvent(hostID):
    '''
    Displays the screen where the user can input information for a new event
    '''
    root.title("New Event")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="New Event", font=("Calibri", 40)).grid(row=0, column=0, sticky=W)
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(6, minsize=20)
    frame.columnconfigure(3, minsize=20)

    nameLabel = Label(frame,text="Event Name:", font=("Calibri", 18)).grid(row=2,column=0,sticky=W)
    lengthLabel = Label(frame,text="Event Length (days):", font=("Calibri", 18)).grid(row=3,column=0,sticky=W)

    nInput = Entry(frame, width=20, font=("Calibri", 24))
    nInput.grid(row=2,column=1,columnspan=2)
    LInput = Entry(frame, width=20, font=("Calibri", 24))
    LInput.grid(row=3,column=1,columnspan=2)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=2,column=4,rowspan=4)

    letters = string.ascii_uppercase
    eventpass = "".join(random.choice(letters) for i in range(10))

    def copypass(event):
        '''
        copies the event password to the users clipboard and changes the label colour
        '''
        root.clipboard_clear()
        root.clipboard_append(eventpass)
        root.update()
        passbox.config(bg="gray85")

    pbframe = LabelFrame(frame,highlightthickness=0,borderwidth=0)
    pbframe.grid(row=5,column=1,rowspan=3)

    passbox = Label(pbframe, width=20, font=("Calibri", 18), text=eventpass, bg="gray75", borderwidth=2, relief="solid")
    passbox.pack()
    passbox.bind("<1>", copypass)

    pblabel = Label(pbframe,text="Your Event Password\n(click to copy)", font=("Calibri", 18)).pack()

    cal = Calendar(frame, selectmode="day", year=datetime.datetime.today().year, month=datetime.datetime.today().month, day=datetime.datetime.today().day, date_pattern="mm/dd/yyyy")
    cal.grid(row=5,column=0,columnspan=2,rowspan=4,sticky=W)

    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * from events")
    eventlist = cursor.fetchall() #Gets a list of every event
    for i in eventlist:     #Displays every event on a calendar so the user knows what days are available
        startdate = i["date"]
        elen = i["length"]
        current = startdate
        current = datetime.datetime.strptime(current, "%Y-%m-%d").strftime("%m/%d/%Y")
        current = datetime.datetime.strptime(current, "%m/%d/%Y").date()
        for j in range(int(elen)):
            cal.calevent_create(current,i["eventname"],tags=[" "])
            current = current + datetime.timedelta(days=1)
    connection.close()

    cal.tag_config(" ", background='red', foreground='white')   #Makes the booked dates display red

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=9,column=0)
    Confirm = Button(frame, text="Confirm", command=lambda: newEventCheck(hostID,nInput.get(),LInput.get(),cal.get_date(),cal,entryError,eventpass), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=9,column=1,columnspan=2)

    frame.rowconfigure(4, minsize=5)

    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def newEventCheck(hostID,name,length,booked,cal,entryError,eventpass):
    '''
    Validates the event information
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
        chooselayout(hostID,name,booked,length,eventpass)
    else:   #Displays any errors to the user
        errorLabel = Label(entryError, text=error, fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)

def chooselayout(hostID,name,booked,length,eventpass):
    '''
    Displays a menu where the user can choose what layout they want for their event
    '''
    for i in root.pack_slaves():
        i.destroy()

    titleLabel = Label(root, text="Choose Event Layout", font=("Calibri", 40)).pack()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    l1frame = LabelFrame(frame,highlightthickness=0,borderwidth=0)
    l1frame.grid(row=0,column=0)
    l2frame = LabelFrame(frame,highlightthickness=0,borderwidth=0)
    l2frame.grid(row=0,column=1)
    l3frame = LabelFrame(frame,highlightthickness=0,borderwidth=0)
    l3frame.grid(row=0,column=2)

    l1 = Label(l1frame,image=l1img,borderwidth=2,relief="solid")
    l1.pack()
    l2 = Label(l2frame,image=l2img,borderwidth=2,relief="solid")
    l2.pack()
    l3 = Label(l3frame,image=l3img,borderwidth=2,relief="solid")
    l3.pack()

    #Creates the 3 buttons for each layout
    lchoice = StringVar(root, "1")
    Radiobutton(l1frame, text = "Layout 1", variable = lchoice, value = 1, indicator = 0, font=("Calibri", 18),image=pixel, width=145,compound="c",borderwidth=5).pack() #Radiobuttons for layout selection
    Radiobutton(l2frame, text = "Layout 2", variable = lchoice, value = 2, indicator = 0, font=("Calibri", 18),image=pixel, width=145,compound="c",borderwidth=5).pack() #
    Radiobutton(l3frame, text = "Layout 3", variable = lchoice, value = 3, indicator = 0, font=("Calibri", 18),image=pixel, width=145,compound="c",borderwidth=5).pack() #

    #Displays a label with the layouts information
    InfoLabel1 = Label(l1frame,text="28 Total Booths\n20 Standard\n8 Large\nStage Included\n", font=("Calibri", 12)).pack(side=LEFT)
    InfoLabel2 = Label(l2frame,text="33 Total Booths\n26 Standard\n6 Large\n1 XL\n", font=("Calibri", 12)).pack(side=LEFT)
    InfoLabel3 = Label(l3frame,text="20 Total Booths\n14 Standard\n4 Large\n2 XL\nStage Included", font=("Calibri", 12)).pack(side=LEFT)

    frame2 = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame2.pack()

    Cancel = Button(frame2, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=0,column=0)
    Confirm = Button(frame2, text="Confirm", command=lambda: ConfirmNewEvent(hostID,name,booked,length,lchoice.get(),eventpass), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=0,column=1)

def ConfirmNewEvent(hostID,name,booked,length,layout,eventpass):
    '''
    Saves the event information to the database
    '''
    connection, cursor = dbconnect.c()
    cursor.execute("INSERT INTO events (hostid, eventname, date, length, layout, eventpass) VALUES (?, ?, ?, ?, ?, ?)", (hostID, name, booked, length, layout, eventpass))   #Adds info into the event table
    cursor.execute("SELECT * FROM events WHERE eventpass = ?",(eventpass,))
    eventID = cursor.fetchone()["id"]

    #Depending on the layout selected, set the corresponding booth count.
    if layout == "1":
        boothcount = [20,8,0]
    elif layout == "2":
        boothcount = [26,6,1]
    elif layout == "3":
        boothcount = [14,4,2]

    #Creates the booths for the event corresponding to the boothcount
    for i in range(boothcount[0]):
        cursor.execute("INSERT INTO booths (companyid, eventid, iswater, iselectric, type) VALUES (?, ?, ?, ?, ?)", (None, eventID, False, False, "standard"))

    for i in range(boothcount[1]):
        cursor.execute("INSERT INTO booths (companyid, eventid, iswater, iselectric, type) VALUES (?, ?, ?, ?, ?)", (None, eventID, False, False, "large"))

    for i in range(boothcount[2]):
        cursor.execute("INSERT INTO booths (companyid, eventid, iswater, iselectric, type) VALUES (?, ?, ?, ?, ?)", (None, eventID, False, False, "xl"))

    connection.commit()
    connection.close()
    menu.menu()
