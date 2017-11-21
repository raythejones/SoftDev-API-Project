import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib

f="storytime.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

c.execute("CREATE TABLE users (user TEXT PRIMARY KEY, pass TEXT, name TEXT, age INT, gender TEXT, hobbies TEXT);")
c.execute("CREATE TABLE friends (user TEXT PRIMARY KEY, friend TEXT PRIMARY KEY);")
c.execute("CREATE TABLE requests (user TEXT PRIMARY KEY, request TEXT PRIMARY KEY);")
c.execute("CREATE TABLE stories (user INT PRIMARY KEY, name TEXT, id TEXT);")

#==========================================================
db.commit() #save changes
db.close()  #close database

