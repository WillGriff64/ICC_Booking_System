import os, sys, menu, dbconnect, info
from info import root, logo, pixel
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

def login():
    '''
    Dsiplays the login screen for the user
    '''
    root.title("Log In")
    for i in root.pack_slaves():
        i.destroy()

    #displays the company logo
    logoLabel = Label(root,image=logo,borderwidth=2,relief="solid")
    logoLabel.pack()

    #makes a frame that all assets are put in, then pack it to center everything+
    frame = LabelFrame(root,highlightthickness=0,borderwidth=0)
    frame.pack()

    usernameLabel = Label(frame,text="Username:", font=("Calibri", 18)).grid(row=1,column=0,sticky=W)
    passwordLabel = Label(frame,text="Password:", font=("Calibri", 18)).grid(row=3,column=0,sticky=W)

    frame.rowconfigure(0, minsize=20)
    frame.rowconfigure(2, minsize=10)
    frame.rowconfigure(4, minsize=10)

    uInput = Entry(frame, width=20, font=("Calibri", 24))
    uInput.grid(row=1,column=1,columnspan=2,padx=(0,115))
    pInput = Entry(frame, width=20, font=("Calibri", 24),show="*")
    pInput.grid(row=3,column=1,columnspan=2,padx=(0,115))

    Confirm = Button(frame, text="Log In", command=lambda: loginattempt(uInput.get(),pInput.get(),loginError), font=("Calibri", 18),image=pixel, width=310,compound="c",borderwidth=5)
    Confirm.grid(row=5,column=1,padx=(0,115))

    Exitbutton = Button(frame, text="Exit", command=lambda: [root.destroy(), quit()], font=("Calibri", 18),image=pixel, width=100,compound="c",borderwidth=5)
    Exitbutton.grid(row=5,column=0)

    loginError = LabelFrame(root,highlightthickness=0,borderwidth=0)
    loginError.pack()

def loginattempt(username,password,loginError):
    '''
    Checks the users inputted login info and checks if it is validates
    '''
    username = username.lower()
    connection, cursor = dbconnect.c()
    cursor.execute("SELECT COUNT(1) as found from staff WHERE username=? AND password = ?", (username,password))
    logtest = cursor.fetchone()["found"]
    if logtest > 0: #If the count of users with matching username and password is more than 0, save their user details and send them to the main menu
        cursor.execute("SELECT * from staff WHERE username=? AND password = ?", (username,password))
        logdetails = cursor.fetchone()
        for i in logdetails:
            info.userdetails[i] = logdetails[i]
        menu.menu()
    else:   #If there isnt an account with that username and password show the error message
        errorLabel = Label(loginError, text="Invalid Log In Credentials", fg="red", font=("Calibri", 16))
        errorLabel.grid(row=0,column=0)
