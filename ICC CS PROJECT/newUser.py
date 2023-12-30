import os, sys, sqlite3
import dbconnect, login, menu
from info import dbname, root, logo, pixel, userdetails
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def newUser(forceAdmin):
    '''
    Displays the menu for creating a new user
    '''
    root.title("New User")
    for i in root.pack_slaves():
        i.destroy()

    accLev = StringVar(root, "1")   #Sets the default account level (the admin button will automatically be pressed on start)

    #Creating tkinter frame for everything to be put if __name__ == '__main__':
    #Using a tkinter frame and .pack() means everything will be centered horizontally
    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    titleLabel = Label(frame, text="New User", font=("Calibri", 40)).grid(row=0, column=0, sticky=W)
    frame.rowconfigure(1, minsize=10)
    frame.rowconfigure(6, minsize=20)
    frame.columnconfigure(3, minsize=20)

    usernameLabel = Label(frame,text="Username:", font=("Calibri", 18)).grid(row=2,column=0,sticky=W)
    passwordLabel = Label(frame,text="Password:", font=("Calibri", 18)).grid(row=3,column=0,sticky=W)
    confirmpasswordLabel = Label(frame,text="Confirm Password:", font=("Calibri", 18)).grid(row=4,column=0,sticky=W)
    accountlevelLabel = Label(frame,text="Account Level:", font=("Calibri", 18)).grid(row=5,column=0,sticky=W)

    uInput = Entry(frame, width=20, font=("Calibri", 24))
    uInput.grid(row=2,column=1,columnspan=2)
    pInput = Entry(frame, width=20, font=("Calibri", 24))
    pInput.grid(row=3,column=1,columnspan=2)
    cInput = Entry(frame, width=20, font=("Calibri", 24))
    cInput.grid(row=4,column=1,columnspan=2)

    Radiobutton(frame, text = "Admin", variable = accLev,value = 1, indicator = 0, font=("Calibri", 18),image=pixel, width=145,compound="c",borderwidth=5).grid(row=5,column=1)
    #If newUser is ran with forceAdmin being true (Happens when there are no users on file), it wont create the staff option and so the first user will be an admin
    if forceAdmin is False:
        Radiobutton(frame, text = "Staff", variable = accLev,value = 2, indicator = 0, font=("Calibri", 18),image=pixel, width=145,compound="c",borderwidth=5).grid(row=5,column=2)

    logoLabel = Label(frame,image=logo,borderwidth=2,relief="solid")
    logoLabel.grid(row=2,column=4,rowspan=4)

    #This code decides what the cancel command will do. If userdetails is empty then noone is logged in (return to login screen), if its false then someone is logged in so return to menu.
    if userdetails != "":
        cancelcommand = "menu.menu()"
    else:
        cancelcommand = "login.login()"

    Cancel = Button(frame, text="Cancel", command=lambda: eval(cancelcommand), font=("Calibri", 18),image=pixel, width=200,compound="c",borderwidth=5)
    Cancel.grid(row=7,column=0)
    Confirm = Button(frame, text="Confirm", command=lambda: addNewUser(uInput.get(),pInput.get(),cInput.get(),accLev.get(),entryError), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=7,column=1,columnspan=2)

    entryError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    entryError.pack()

def addNewUser(username,password,confirm,accLev,entryError):
    '''
    Takes the users input, validates it, and if it passes adds a new user to the database
    '''
    for i in entryError.grid_slaves():
        i.destroy()

    username = username.lower()
    error = ""
    haserror = False

    #Check if any data is missing
    if username == "" or password == "" or confirm =="":
        error = "Data missing from input field"
        haserror = True
    elif password != confirm:
        error = "Passwords do not match"
        haserror = True
    else:
        #Checks if there is already an account with that name
        connection, cursor = dbconnect.c()
        namecheck = cursor.execute("select * from staff WHERE username=?",(username,))
        row = cursor.fetchone()
        if row != None:
            error = "That username is already in use"
            haserror = True
        connection.close()

    #If there arn't any errors the function adds the new user
    if haserror == False:
        connection, cursor = dbconnect.c()
        cursor.execute("INSERT INTO staff (username, password, accountlevel) VALUES (?, ?, ?)", (username, password, accLev))
        connection.commit()
        connection.close()
        login.login()
    else:
        #If there is an error it displays the corresponding error message
        errorLabel = Label(entryError, text=error, fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)
