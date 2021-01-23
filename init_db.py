import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
<<<<<<< HEAD

cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ('simran', 'simran@gmail.com', 'simran')
            )

cur.execute("INSERT INTO users (name, email, password) VALUES (?, ? ,?)",
            ('mansi', 'mansi@gmail.com',  'mansi')
            )

=======
# will include querries to be run initially
>>>>>>> d7c592f1d1707b3406328c2862319e800af766e2
connection.commit()
connection.close()
