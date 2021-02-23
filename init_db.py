import sqlite3


def initializeDB():
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()
    # will include querries to be run initially
    connection.commit()
    connection.close()
