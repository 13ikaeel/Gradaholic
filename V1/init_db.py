from sqlite3 import *
import hashlib


db = connect('db.db')
c = db.cursor()


###################################################################
c.execute('''
	CREATE TABLE IF NOT EXISTS Users(
		id INTEGER PRIMARY KEY NOT NULL,
		username TEXT NOT NULL,
    hashedpw TEXT NOT NULL,
    email TEXT NOT NULL,
		rp INTEGER NOT NULL,
    admin INTEGER NOT NULL
	)
''')

###################################################################################
c.execute('''
	CREATE TABLE IF NOT EXISTS Questions(
		id INTEGER PRIMARY KEY NOT NULL,
		question TEXT NOT NULL,
		qntype TEXT NOT NULL
	)
''')
##########################################################################
c.execute('''
	CREATE TABLE IF NOT EXISTS Submissions(
		id INTEGER PRIMARY KEY NOT NULL,
		qn_id INTEGER NOT NULL REFERENCES Questions(id),
		user_id INTEGER NOT NULL REFERENCES Users(id),
		essay TEXT NOT NULL,
		rating TEXT NOT NULL
	)
''')


db.commit()
db.close()
####################################################
