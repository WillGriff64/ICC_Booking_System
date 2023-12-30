import sqlite3
from info import dbname

#format output when doing an sql querey
def dict_factory(cursor, row):
    '''
    Formats the sql querey into a dictionary, labeled with the schema columnspan
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#used when a function needs to connect to the database
def c():
    '''
    Returns the sql connection and cursor variables
    '''
    connection = sqlite3.connect(dbname)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    return connection, cursor
