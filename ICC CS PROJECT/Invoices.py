import os, sys, sqlite3, datetime
import menu, dbconnect, popupmessage
from info import root, logo, pixel, userdetails
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def invoicemenu(type):
    '''
    Creates the tkinter labels for the invoice input Menu
    '''
    root.title("Invoices")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    #Changes the title text depending on the type of invoice you are looking for
    if type == "booth":
        info = "Enter the name of the company\nthe booth was booked under"
    elif type == "event":
        info = "Enter the event name"

    titleLabel = Label(frame, text=info, font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    nInput = Entry(frame, width=20, font=("Calibri", 24))
    nInput.grid(row=2,column=0,columnspan=2)

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 14),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=7,column=0)

    Confirm = Button(frame, text="Confirm", command=lambda: check(nInput.get(),entryError,type), font=("Calibri", 14),image=pixel, width=200,compound="c",borderwidth=5)
    Confirm.grid(row=7,column=1)

    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()
    entryError.pack()

def check(name,entryError,type):
    '''
    Checks the input and counts the amount of booths/events attached
    '''
    connection, cursor = dbconnect.c()
    if type == "booth":
        cursor.execute("SELECT COUNT(1) from companies WHERE name=?", (name,)) #searches for company with matching name
    elif type == "event":
        cursor.execute("SELECT COUNT(1) from events WHERE eventname=?", (name,)) #searches for company with matching name
    nametest = cursor.fetchone()
    nametest = nametest["COUNT(1)"]
    if nametest == 1: #If there is 1 name it will continue like normal
        if type == "booth":
            cursor.execute("SELECT * from companies WHERE name=?", (name,))
            companyinfo = cursor.fetchone()
            cursor.execute("SELECT COUNT(1) from booths WHERE companyid=?", (companyinfo["id"],)) #searches for company with matching name
            nametest = cursor.fetchone()
            nametest = nametest["COUNT(1)"]
            if nametest == 1:
                cursor.execute("SELECT * from booths WHERE companyid=?", (companyinfo["id"],))
                info = cursor.fetchone()
                showinvoice(info,companyinfo,"booth")
            elif nametest > 1:
                cursor.execute("SELECT * from booths WHERE companyid=?", (companyinfo["id"],))
                boothlist = cursor.fetchall()
                connection.close()
                multiname(boothlist,"boothmulti")
            elif nametest == 0:
                errorLabel = Label(entryError, text="Company has not booked any booths", fg="red", font=("Calibri", 16))
                errorLabel.grid(row=0,column=0)

        elif type == "event":
            cursor.execute("SELECT * from events WHERE eventname=?", (name,))
            eventinfo = cursor.fetchone()
            cursor.execute("SELECT * from hosts WHERE id=?", (eventinfo["hostid"]))
            hostinfo = cursor.fetchone()
            connection.close()
            showinvoice(eventinfo,hostinfo,"event")

    elif nametest > 1: #If more than one entry with the same name is returned, fromat and move to multiname()
        cursor = connection.cursor()
        if type == "booth":
            cursor.execute("SELECT * from companies WHERE name=?", (name,))
            postlist = cursor.fetchall()
            connection.close()
            multiname(postlist,type)
        elif type =="event":
            cursor.execute("SELECT * from events WHERE eventname=?", (name,))
            passlist = cursor.fetchall()
            connection.close()
            multiname(passlist,type)
    else: #If no host is found show error
        errorLabel = Label(entryError, text="No record with that name on file", fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)

def multiname(infolist,type):
    '''
    If there is more than one booth/event display each one and let the user choose
    '''
    for i in root.pack_slaves():
        i.destroy()

    #Changes the title depending on the type of invoice you are looking for
    if type == "event":
        title="Select the correct event password"
    elif type == "booth":
        title="Select the postcode for your company"
    elif type =="boothmulti":
        title="Select the ID for your chosen booth"

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()
    titleLabel = Label(frame, text=title, font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)
    buttonrow = 1

    #Creates a button for every phone number found.
    for i in infolist:
        if type == "event":
            ivar = i["eventpass"]
            infopart = str(str(ivar)[0:3]+"******"+str(ivar)[len(str(ivar))-3:len(str(ivar))+1]) #Creates an obfuscated version of the info provided
        elif type == "booth":
            ivar = i["postcode"]
            infopart = ivar
        elif type == "boothmulti":
            infopart = str("b"+str(i["id"]))
            ivar = i["id"]
        else:
            infopart = str(i)
        bname = Button(frame, text=infopart, command=lambda infovar=ivar: infoparse(infovar,type), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5) #Creates the button
        bname.grid(row=buttonrow,column=0) #Add button to grid
        buttonrow += 1 #increase row number for next button

    #Adding button to cancel, logo and row padding
    frame.rowconfigure(buttonrow, minsize=20)
    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=buttonrow+1,column=0)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=1,column=1,rowspan=999)

def infoparse(infovar,type):
    '''
    Takes the selected event/booth from multiname(), and passes its info to showinvoice()
    '''
    connection, cursor = dbconnect.c()
    if type == "event":
        cursor.execute("SELECT * from events WHERE eventpass = ?", (infovar,))
        info = cursor.fetchone()
        cursor.execute("SELECT * from hosts WHERE id = ?", (info["hostid"],))
        hostinfo = cursor.fetchone()
        connection.close()
        showinvoice(info,hostinfo,"event")

    elif type == "booth":
        cursor.execute("SELECT * from companies WHERE postcode = ?", (infovar,))
        companyinfo = cursor.fetchone()
        cursor.execute("SELECT COUNT(1) from booths WHERE companyid=?", (companyinfo["id"],)) #searches for company with matching name
        nametest = cursor.fetchone()
        nametest = nametest["COUNT(1)"]
        if nametest == 1:
            cursor.execute("SELECT * from booths WHERE companyid=?", (companyinfo["id"],))
            info = cursor.fetchall()
            showinvoice(info,companyinfo,"booth")
        elif nametest > 1:
            cursor.execute("SELECT * from booths WHERE companyid=?", (companyinfo["id"],))
            boothlist = cursor.fetchall()
            connection.close()
            multiname(boothlist,"boothmulti")
        elif nametest == 0:
            popupmessage.popupmessage("Company has no booths booked. Returning to menu.",1,"Ok",None,None,None,None,None)
            menu.menu()

    elif type == "boothmulti":
        cursor.execute("SELECT * from booths WHERE id = ?", (infovar,))
        info = cursor.fetchone()
        cursor.execute("SELECT * from companies WHERE id = ?", (info["companyid"],))
        hostinfo = cursor.fetchone()
        connection.close()
        showinvoice(info,hostinfo,"booth")

def showinvoice(info,masterinfo,type):
    '''
    Displays the invoice on screen buttons to manage its paid/cancelled status
    '''
    dyntitle = "Invoice for "+str(type)+" ID: "+ str(info["id"])
    root.title(dyntitle)
    for i in root.pack_slaves():
        i.destroy()

    connection, cursor = dbconnect.c()

    #Sees if the invoice for this event/booth exists, if it doesnt it creates one for it.
    if type == "booth":
        cursor.execute("SELECT COUNT(1) AS found FROM binvoices WHERE boothid = ?",(info["id"],))
    elif type == "event":
        cursor.execute("SELECT COUNT(1) AS found FROM einvoices WHERE eventid = ?",(info["id"],))
    boothcount = cursor.fetchone()["found"]
    if boothcount > 0:      #If boothcount is > 0, there is an existing invoice saved
        if type == "booth":
            cursor.execute("SELECT * FROM binvoices WHERE boothid = ?",(info["id"],))
        elif type == "event":
            cursor.execute("SELECT * FROM einvoices WHERE eventid = ?",(info["id"],))
        invoiceinfo = cursor.fetchone()
        paid = invoiceinfo["paid"]
        cancel = invoiceinfo["cancel"]
    else:
        if type == "booth":
            cursor.execute("INSERT INTO binvoices (boothid, paid, cancel) VALUES (?, ?, ?)", (info["id"], 0, 0))
        elif type == "event":
            cursor.execute("INSERT INTO einvoices (eventid, paid, cancel) VALUES (?, ?, ?)", (info["id"], 0, 0))
        paid = 0
        cancel = 0
    connection.commit()

    #Gets the info frm config for booth pricing, back account number, ect...
    cursor.execute("SELECT * FROM config")
    config = cursor.fetchone()
    connection.close()


    #The invoice 'receipt' is formatted differently depending on its type. Here is where both are made
    if type == "booth":
        total, daycost, water, electric, purecost, cancelstatus = boothcosts(info)
        cancelmessage = showcancel(cancelstatus)
        receipt = ["Company: "+str(masterinfo["name"]),"Email: "+masterinfo["email"],"Phone Number: "+str(masterinfo["phone"])," ","Booth ID: B"+str(info["id"]),"Daily Booth Cost: £"+str(daycost),"Cost Before Utilities: £"+str(purecost),"Water Cost: £"+str(water),"Electricity Cost: £"+str(electric),str(cancelmessage)+"Total: £"+str(total)," ","Please pay to:","Name: "+str(config["ceo"]),"Account Number: "+str(config["banknum"])]
    elif type == "event":
        total, daycost, discount, boothcount, bookedcount, cleaningfee, cancelstatus = eventcosts(info)
        cancelmessage = showcancel(cancelstatus)
        receipt = ["Name: "+str(masterinfo["name"])+""+str(masterinfo["surname"]),"Email: "+masterinfo["email"],"Phone Number: "+str(masterinfo["phone"])," ","Event Name: "+info["eventname"],"Number of booths: "+str(boothcount),"Number of booths booked: "+str(bookedcount),"Booked booth discount: £"+str(discount),"Daily cost: £"+str(daycost),"Cleaning Fee: £"+str(cleaningfee),str(cancelmessage)+"Total: £"+str(total)," ","Please pay to:","Name: "+config["ceo"],"Account Number: "+str(config["banknum"])]

    #Joins the receipt list into a single string. Each item in the list is a different line and this .join concatenates them with a new line between.
    fulltext = "\n".join(str(v) for v in receipt)

    #This sets the default values of paid/cancelled to whatever was previously stored (0 if its new)
    ispaid = IntVar()
    iscancelled = IntVar()
    ispaid.set(paid)
    iscancelled.set(cancel)

    #Rest of this function creates and displays the tkinter labels/buttons for the GUI
    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Invoice:", font=("Calibri", 30)).grid(row=0, column=0, sticky=W)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=1,column=1,rowspan=3,columnspan=2,sticky=N)

    paidb = Checkbutton(frame, text="Paid:",font=("Calibri", 18),variable=ispaid)
    paidb.grid(row=4,column=1)
    cancelb = Checkbutton(frame, text="Cancelled:",font=("Calibri", 18),variable=iscancelled)
    cancelb.grid(row=4,column=2)

    updatebutton = Button(frame, text="Save", command=lambda: update(info,masterinfo,ispaid.get(),iscancelled.get(),type), font=("Calibri", 18),image=pixel, width=395,compound="c",borderwidth=5)
    updatebutton.grid(row=5,column=1,columnspan=2)

    infobox = LabelFrame(frame, highlightthickness=0, bg="gray75", borderwidth=2, relief="solid", height=430,width=400)
    infobox.grid(row=1,column=0,rowspan=5)
    infobox.grid_propagate(0)
    text = StringVar()
    text.set(fulltext)
    infotext = Label(infobox,textvariable=text, font=("Calibri", 16), justify=LEFT, bg="gray75").grid(row=2,column=0,sticky="W", columnspan=2)

    MenuB = Button(frame, text="Menu", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=395,compound="c",borderwidth=5)
    MenuB.grid(row=6,column=1,columnspan=2)

    SaveB = Button(frame, text="Save as .TXT", command=lambda: savetxt(info,masterinfo,fulltext), font=("Calibri", 18),image=pixel, width=395,compound="c",borderwidth=5)
    SaveB.grid(row=6,column=0)

def boothcosts(info):
    '''
    Calculates the cost if the booth from the given info
    '''
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT * FROM events WHERE id = ?",(info["eventid"],))
    eventinfo = cursor.fetchone()
    cursor.execute("SELECT * FROM binvoices WHERE boothid = ?",(info["id"],))
    invoiceinfo = cursor.fetchone()
    cursor.execute("SELECT * FROM config")
    config = cursor.fetchone()

    def utilitycost(running,days,utility):      #Utilities in booths have a discount where every day, the cost goes down by £1 with a max discount of half price per day.
        '''
        Calculate the utility cost with the discount by using recursive function
        '''
        if days == 0:
            return running
        else:
            if config[utility] - days < config[utility]/2:
                daycost = config[utility]/2
            else:
                daycost = config[utility] - days
            return(running + utilitycost(daycost,days-1,utility))

    #Runs the utilitycost function if water or electricity is booked, otherwise the cost stays at £0
    water, electric = 0, 0
    if info["iswater"] == 1:
        water = utilitycost(0,eventinfo["length"],"watercost")
    if info["iselectric"] == 1:
        electric = utilitycost(0,eventinfo["length"],"electricitycost")

    #Gets the daily cost of the booth from the config info depending on booth size
    if info["type"] == "standard":
        daycost = config["sbcost"]
    elif info["type"] == "large":
        daycost = config["lbcost"]
    elif info["type"] == "xl":
        daycost = config["xlbcost"]

    purecost = eventinfo["length"]*daycost
    total = eventinfo["length"]*daycost+water+electric
    connection.close()

    cancelstatus = False
    if invoiceinfo["cancel"] == 1:
        total = total*0.1
        cancelstatus = True
    return(total,daycost,water,electric,purecost,cancelstatus)

def eventcosts(info):
    '''
    Takes the given info and calculates the event cost
    '''
    connection, cursor = dbconnect.c()
    cleaningfee = 200

    cursor.execute("SELECT COUNT(1) AS found FROM booths WHERE eventid = ?",(info["id"],))
    boothcount = cursor.fetchone()["found"]
    cursor.execute("SELECT * FROM einvoices WHERE eventid = ?",(info["id"],))
    invoiceinfo = cursor.fetchone()
    cursor.execute("SELECT * from booths WHERE eventid=?", (info["id"],)) #Get the booth info
    boothlist = cursor.fetchall()
    bookedcount = 0
    for i in boothlist:     #Count how many booths have been booked
        if i["companyid"] != None:
            bookedcount += 1
    cursor.execute("SELECT * FROM config")
    config = cursor.fetchone()

    boothcost = config["sbcost"]
    length = info["length"]

    discount = int(bookedcount) * int(boothcost) #The event gets discounted for every booth that has been successfully booked
    daycost = int(boothcount) * int(boothcost) - int(discount)
    total = int(daycost) * int(length)
    cancelstatus = False
    if invoiceinfo["cancel"] == 1:
        total = total*0.1
        cancelstatus = True
    return(total,daycost,discount,boothcount,bookedcount,cleaningfee,cancelstatus)

def savetxt(info,master,text):
    '''
    Saves the invoice as a text file for emailing/posting
    '''
    filename = str(datetime.datetime.today().strftime('%Y-%m-%d'))+" "+str(master["name"])+" "+str(info["id"])+" Invoice"+".txt"   #Formats the file name as YYY-MM-DD HostName/CompanyName eventID/boothID Invoice.txt
    file = open("Invoices/"+filename,"w")
    file.write(text)
    file.close()

def update(info,master,paid,cancel,type):
    '''
    Updates / saves the invoice and any changes
    '''
    connection, cursor = dbconnect.c()
    if type == "booth":
        cursor.execute("UPDATE binvoices SET paid = ?, cancel = ? WHERE boothid = ? ",(paid,cancel,info["id"]))
    elif type == "event":
        cursor.execute("UPDATE einvoices SET paid = ?, cancel = ? WHERE eventid = ?",(paid,cancel,info["id"]))
    connection.commit()
    connection.close()
    showinvoice(info,master,type)

def showcancel(cancelstatus):
    '''
    Displays a messgae if the invoice has been cancelled
    '''
    if cancelstatus == True:
        cancelmessage = ("10% cancelation fee will be charged. \n")
    else:
        cancelmessage = ("")
    return cancelmessage
