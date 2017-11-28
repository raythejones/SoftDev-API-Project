import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib

f="presents.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

c.execute("CREATE TABLE users (user TEXT PRIMARY KEY, pass TEXT, name TEXT, age INT, gender TEXT, hobbies TEXT);")
c.execute("CREATE TABLE friends (user TEXT PRIMARY KEY, friend TEXT PRIMARY KEY);")
c.execute("CREATE TABLE requests (user TEXT PRIMARY KEY, request TEXT PRIMARY KEY);")
c.execute("CREATE TABLE products (user INT PRIMARY KEY, name TEXT, id TEXT);")

pw1 = hashlib.md5('pass').hexdigest()
pw2 = hashlib.md5('mmomi').hexdigest()
pw3 = hashlib.md5('linux').hexdigest()
pw4 = hashlib.md5('pen').hexdigest()
pw5 = hashlib.md5('crazy').hexdigest()
c.execute("INSERT INTO users VALUES('dw',\"%s\","DW",\"\",\"\",\"\");"%(pw1))
c.execute("INSERT INTO users VALUES('ppapi',\"%s\","PPAPi","17","other","coding, volleyball, dancing, eating, snowboarding");"%(pw2))
c.execute("INSERT INTO users VALUES('comp',\"%s\","PC","35","male","run, cool down, shine bright like a diamond");"%(pw3))
c.execute("INSERT INTO users VALUES('apple',\"%s\","Apple","10","female","read books, rot, fall");"%(pw4))
c.execute("INSERT INTO users VALUES('banana',\"%s\","Banana",\"\",\"\",\"\");"%(pw5))


c.execute("INSERT INTO friends VALUES('dw','ppapi')")
c.execute("INSERT INTO friends VALUES('ppapi','dw')")
c.execute("INSERT INTO friends VALUES('dw','apple')")
c.execute("INSERT INTO friends VALUES('apple','dw')")
c.execute("INSERT INTO friends VALUES('ppapi','apple')")
c.execute("INSERT INTO friends VALUES('apple','ppapi')")
c.execute("INSERT INTO friends VALUES('comp','ppapi')")
c.execute("INSERT INTO friends VALUES('ppapi','comp')")

c.execute("INSERT INTO requests VALUES('dw','comp')")
c.execute("INSERT INTO requests VALUES('apple','banana')")
c.execute("INSERT INTO requests VALUES('apple','comp')")

#==========================================================
db.commit() #save changes
db.close()  #close database

