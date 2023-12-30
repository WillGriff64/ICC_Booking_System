import os, sys, sqlite3
import datetime
import string
import dbconnect, menu
from tkcalendar import *
from info import dbname, root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def timetable():
    '''
    Displays a menu where you can view all booked events and their information
    '''
    root.title("Event Timetable")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Event Timetable", font=("Calibri", 40)).grid(row=0, column=0, sticky=W)
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(3, minsize=10)
    frame.columnconfigure(1, minsize=10)

    #Creates an empty input box to be changed later
    infobox = LabelFrame(frame, highlightthickness=0, bg="gray75", borderwidth=2, relief="solid", height=225,width=400)
    infobox.grid(row=4,column=2,rowspan=5)
    infobox.grid_propagate(0)
    text = StringVar()
    text.set("")
    infotext = Label(infobox,textvariable=text, font=("Calibri", 16), justify=LEFT, bg="gray75").grid(row=2,column=0,sticky="W", columnspan=2)

    calbox= LabelFrame(frame, highlightthickness=0, borderwidth=2, relief="solid", height=400,width=400)
    calbox.grid(row=4,column=0,rowspan=5)
    calbox.grid_propagate(0)

    cal = Calendar(calbox, selectmode="day", year=datetime.datetime.today().year, month=datetime.datetime.today().month, day=datetime.datetime.today().day, date_pattern="mm/dd/yyyy")
    cal.pack(fill="both", expand=True)

    #This for loop fills the calendar with the events
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * from events")
    eventlist = cursor.fetchall()
    colours = ["red","orange","yellow","green","blue","magenta","cyan","pale green","maroon"] #Colours each event can choose from
    for i in eventlist:
        id = i["id"]
        startdate = i["date"]
        elen = i["length"]
        current = startdate
        current = datetime.datetime.strptime(current, "%Y-%m-%d").strftime("%m/%d/%Y")  #Format date from sql table into date object
        current = datetime.datetime.strptime(current, "%m/%d/%Y").date()
        for j in range(int(elen)):
            cal.calevent_create(current,i["eventname"],tags=[id])   #Creates the event in the calendar
            current = current + datetime.timedelta(days=1)
        cid = id - 1
        while cid > len(colours):   #If the event ID is bigger than the amount of colours, minus the amount of colours untill its smaller
            cid = cid - len(colours)
        ecolour = colours[cid]  #Chooses the event colour
        cal.tag_config(id, background=ecolour, foreground="white")  #Sets the event colour
    connection.close()

    ViewB = Button(frame, text="View Event Info", command=lambda: giveinfo(text,cal), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    ViewB.grid(row=9,column=0)

    ClearB = Button(frame, text="Clear", command=lambda: clear(text), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    ClearB.grid(row=9,column=2)

    MenuB = Button(frame, text="Menu", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    MenuB.grid(row=10,column=0)

def clear(text):
    '''sets the event infobox to empty'''
    text.set("")

def giveinfo(text,cal):
    '''Gets the info from the selected event and displays it'''
    eventlist = []
    eventviewdate = cal.selection_get() #Gets selected date
    x = cal.get_calevents(eventviewdate) #Gets the event id (not the one in the table but the event id in tkcalendar)
    devents = list(x)
    for y in devents:
        b = cal.calevent_cget(y, option="tags") #Gets the tag (in this case the real event id) from the tkcalendar event id
        eventlist.append(b)
    try:
        eventid = eventlist[0][0] #If list is empty, no event was selcted
    except IndexError:
        text.set("No event on selected day!")
    else:
        #Get info for the infobox
        connection, cursor = dbconnect.c()
        cursor.execute("SELECT * from events WHERE id=?", (eventid,)) #Get the event info
        edetails = cursor.fetchone()
        hostid = edetails["hostid"]
        cursor.execute("SELECT * from hosts WHERE id=?", (hostid,)) #Get the host info
        hdetails = cursor.fetchone()
        cursor.execute("SELECT * from booths WHERE eventid=?", (eventid,)) #Get the booth info
        boothlist = cursor.fetchall()
        count = 0
        for i in boothlist:     #Count how many booths have been booked
            if i["companyid"] != None:
                count += 1

        #Construct the string to be shown
        infotext = "Event Name: "+edetails["eventname"]+"\n"+"Host Name: "+hdetails["name"]+" "+hdetails["surname"]+"\n"+"Host Phone Number: "+str(hdetails["phone"])+"\n"+"Host Email: "+hdetails["email"]+"\n"+"Number of booths booked: "+str(count)+"\n"+"Event Password: "+edetails["eventpass"]
        text.set(infotext) #Show it
