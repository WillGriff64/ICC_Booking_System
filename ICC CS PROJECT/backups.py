import os, sys, shutil, datetime
import menu, popupmessage, startup
from info import root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def backups():
    '''
    Creates the tkinter menu for the backup system
    '''
    root.title("Manage Backups")
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Manage Backups", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=3)
    frame.columnconfigure(1, minsize=20)

    Create = Button(frame, text="Create New Backup", command=lambda: popupmessage.popupmessage("Are you sure you want to make\na new backup?",2,"Yes","No",None,"backups.new()","backups.backups()",None), font=("Calibri", 18),image=pixel, width=300,compound="c",borderwidth=5)
    Create.grid(row=1,column=0)

    Load = Button(frame, text="Load Backup", command=lambda: popupmessage.popupmessage("Are you sure you want to load an old backup?\n(This could result in a loss of data)",2,"Yes","No",None,"backups.selectnew()","backups.backups()",None), font=("Calibri", 18),image=pixel, width=300,compound="c",borderwidth=5)
    Load.grid(row=2,column=0)

    frame.rowconfigure(3, minsize=10)

    Cancel = Button(frame, text="Cancel", command=lambda: menu.menu(), font=("Calibri", 18),image=pixel, width=300,compound="c",borderwidth=5)
    Cancel.grid(row=4,column=0)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=1,column=2,rowspan=4)

def new():
    '''
    Creates a new backup
    '''
    source = os.getcwd() #Gets the path of the souce folder
    try:
        folder = os.mkdir("Backups") #Makes a folder called Backups if one doesnt exist
    except FileExistsError:
        pass
    folder = source+"/Backups"  #Formatting the folder path for future use

    shutil.copy("ICC.db",folder)    #Copies ICC.db to the backups folder
    filepath = os.path.join(folder,"ICC.db")    #gets the path for the new ICC.db
    newname = os.path.join(folder, str(datetime.datetime.today().strftime('%Y%m%d'))+" ICC.db") #Formats the new name as "YYYMMDD ICC.db" - Do this because sorting in the future would be easier (bigger number = more recent)
    try:
        os.rename(filepath, newname)    #Tries to rename the file, if it fails the ICC.db wont be renamed but next backup it will be replaced anyway
    except FileExistsError:
        popupmessage.popupmessage("Backup for "+str(datetime.datetime.today().strftime('%d/%m/%Y'))+" already exists",1,"ok",None,None,None,None,None)
        backups()
    else:
        popupmessage.popupmessage("Backup successfully created! \n ("+str(datetime.datetime.today().strftime('%Y%m%d'))+" ICC.db"+")",1,"ok",None,None,None,None,None)


def selectnew():
    '''
    Displays possible backups to select and then load
    '''
    source = os.getcwd() #Gets the path of the souce folder
    try:
        folder = os.mkdir("Backups") #Makes a folder called Backups if one doesnt exist
    except FileExistsError:
        pass
    folder = source+"/Backups" #Create folder path

    backuplist = os.listdir(folder) #Sets contents of Backups folder to a list
    if not backups: #Check if folder is empty
        popupmessage.popupmessage("No backups found (place any existing backups in "+str(folder)+")",1,"ok",None,None,None,None,None)
        backups.backups()

    backuplist.sort(reverse=True) #Sorts the list in order of "most recent" (since all files are YYYYMMDD we just sort it in descending order)
    for i in root.pack_slaves():
        i.destroy()

    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="Select the backup to load", font=("Calibri", 40)).grid(row=0, column=0, sticky=W,columnspan=2)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=1,column=1,rowspan=5)

    buttonrow = 1
    amount = 0
    for i in backuplist:    #Makes a button for each file in backups
        bname = Button(frame, text=i, command=lambda file=i: loadbackup(file), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5) #Creates the button
        bname.grid(row=buttonrow,column=0) #Add button to grid
        buttonrow += 1 #increase row number for next button
        amount += 1
        if amount >= 5:
            AmountError = Label(frame, text="Too many backups in backups folder,\nshowing 5 most recent", fg="red", font=("Calibri", 16))   #If there are more than 5 backups, it stops to avoid them spilling off screen
            AmountError.grid(row=buttonrow,column=0)
            break

    Cancel = Button(frame, text="Cancel", command=lambda: backups(), font=("Calibri", 18),image=pixel, width=300,compound="c",borderwidth=5)
    Cancel.grid(row=buttonrow+1,column=0)

def loadbackup(file):
    '''
    Copies the selected backup and renames it
    '''
    start = os.getcwd()+"\\Backups\\"
    destination = os.getcwd()
    shutil.copy(str(start)+str(file),destination)    #Copies selected file to the main folder
    os.rename("ICC.db", "OLD ICC.db")   #Renames old file
    os.rename(file, "ICC.db")   #Renames new file
    popupmessage.popupmessage("For the backup to initalize\nthe program needs to restart",1,"Restart",None,None,None,None,None)
    startup.start()
