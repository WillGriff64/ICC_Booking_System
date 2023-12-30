import os, sys, sqlite3
import dbconnect, login, popupmessage, newUser
from info import dbname

def start():
    '''
    Manages the creation of the sql tables if they dont exist, also forces account creation on startup if none are found
    '''
    connection, cursor = dbconnect.c()

    #Checks if tables exist in .db file, creates them if they dont
    cursor.execute("CREATE TABLE IF NOT EXISTS staff (id integer primary key autoincrement, username TEXT, password TEXT, accountlevel INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS hosts (id integer primary key autoincrement, name TEXT, surname TEXT, phone INTEGER, email TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS events (id integer primary key autoincrement, hostid TEXT, eventname TEXT, date TEXT, length INTEGER, layout INTEGER, eventpass TEXT, FOREIGN KEY(hostid) REFERENCES hosts(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS companies (id integer primary key autoincrement, name TEXT, phone INTEGER, email TEXT, postcode TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS booths (id integer primary key autoincrement, companyid INTEGER, eventid INTEGER, iswater INTEGER, iselectric INTEGER, type INTEGER, FOREIGN KEY(companyid) REFERENCES companies(id), FOREIGN KEY(eventid) REFERENCES events(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS einvoices (id integer primary key autoincrement, eventid INTEGER, paid INTEGER, cancel INTEGER, FOREIGN KEY(eventid) REFERENCES events(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS binvoices (id integer primary key autoincrement, boothid INTEGER, paid INTEGER, cancel INTEGER, FOREIGN KEY(boothid) REFERENCES booths(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS config (ceo TEXT, banknum INTEGER, sbcost INTEGER, lbcost INTEGER, xbcost INTEGER, dbpath TEXT, watercost INTEGER, electricitycost INTEGER)")

    EmptyConfigCheck = cursor.execute("select * from config")
    row = cursor.fetchone()
    if row == None:
        #Default vales for config
        ceoname = "CEO NAME"
        banknumber = 000000000000
        sbcost = 0
        lbcost = 0
        xbcost = 0
        watercost = 0
        electricitycost = 0
        dbpath = "ICC.db"
        cursor.execute("INSERT INTO config (ceo, banknum, sbcost, lbcost, xbcost, dbpath, watercost, electricitycost) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(ceoname,banknumber,sbcost,lbcost,xbcost,dbpath,watercost,electricitycost))
        connection.commit()
    #Checks to see if there are any existing user accounts
    NewUserCheck = cursor.execute("select * from staff")
    row = cursor.fetchone()
    if row == None:
        connection.close()
        #Displays a message telling the user as to why a new account is being created
        popupmessage.popupmessage("No accounts found, please make one now.\n(This account will be an administrator)",1,"Ok",None,None,"popup.destroy",None,None)
        newUser.newUser(True)
    else:
        connection.close()
        login.login()
