import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
            ('simran', 'simran@gmail.com', 'simmi', 'simran')
            )

cur.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
            ('mansi', 'mansi@gmail.com', 'mansiji', 'mansi')
            )

connection.commit()
connection.close()
