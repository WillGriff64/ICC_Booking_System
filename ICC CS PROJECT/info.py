import os, sys, sqlite3
#sys.path.append(os.path.abspath("packages"))
from tkinter import *
from PIL import ImageTk, Image

#This file is used to store and pass variables between files

dbname = "ICC.db"

root = Tk()

#Make window appear in center of screen
#window size
w = 900
h = 550

#get screen size
ws = root.winfo_screenwidth() #width of the screen
hs = root.winfo_screenheight() #height of the screen

#calculate x and y coordinates for root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(False, False)

#Creates images to be used in the program
logo = ImageTk.PhotoImage(Image.open("logo.png"))
l1img = ImageTk.PhotoImage(Image.open("layout1.png"))
l2img = ImageTk.PhotoImage(Image.open("layout2.png"))
l3img = ImageTk.PhotoImage(Image.open("layout3.png"))

pixel = PhotoImage(width=1, height=1)

userdetails = {}
