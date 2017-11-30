import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import sqlite3
from os import system
import hashlib

def make_database():
	db = sqlite3.connect("data/app.db") #open if f exists, otherwise create
	c = db.cursor()    #facilitate db ops
	#==========================================================
	#INSERT YOUR POPULATE CODE IN THIS ZONE

	c.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, name TEXT, age INT, gender TEXT, hobbies TEXT);")
	c.execute("CREATE TABLE friends (username TEXT , friend TEXT );")
	c.execute("CREATE TABLE requests (username TEXT , request TEXT );")
	c.execute("CREATE TABLE products (username INT , name TEXT);")

	pw1 = hashlib.sha224( "pass" ).hexdigest()
	pw2 = hashlib.sha224( "mmomi" ).hexdigest()
	pw3 = hashlib.sha224( "linux" ).hexdigest()
	pw4 = hashlib.sha224( "pen" ).hexdigest()
	pw5 = hashlib.sha224( "crazy" ).hexdigest()

	c.execute("INSERT INTO users VALUES('dw',\"%s\",'DW',0,\"\",\"\");"%(pw1))
	c.execute("INSERT INTO users VALUES('ppapi',\"%s\",'PPAPi',17,'other','coding, volleyball, dancing, eating, snowboarding');"%(pw2))
	c.execute("INSERT INTO users VALUES('comp',\"%s\",'PC',35,'male','run, cool down, shine bright like a diamond');"%(pw3))
	c.execute("INSERT INTO users VALUES('apple',\"%s\",'Apple',10,'female','read books, rot, fall');"%(pw4))
	c.execute("INSERT INTO users VALUES('banana',\"%s\",'Banana',0,\"\",\"\");"%(pw5))


	c.execute("INSERT INTO friends VALUES('dw','ppapi');")
	c.execute("INSERT INTO friends VALUES('ppapi','dw');")
	c.execute("INSERT INTO friends VALUES('dw','apple');")
	c.execute("INSERT INTO friends VALUES('apple','dw');")
	c.execute("INSERT INTO friends VALUES('ppapi','apple');")
	c.execute("INSERT INTO friends VALUES('apple','ppapi');")
	c.execute("INSERT INTO friends VALUES('comp','ppapi');")
	c.execute('INSERT INTO friends VALUES("ppapi","comp");')


	c.execute("INSERT INTO requests VALUES('dw','comp');")
	c.execute("INSERT INTO requests VALUES('apple','banana');")
	c.execute("INSERT INTO requests VALUES('apple','comp');")

        c.execute("INSERT INTO products VALUES('dw','Nintendo Switch Console Gray Joy-Con');")
        c.execute("INSERT INTO products VALUES('apple','Nintendo Switch Console Gray Joy-Con');")
        #c.execute("INSERT INTO products VALUES('dw','LEGO Disney Princess Belle\'s Enchanted Castle');")
        #41067

	#==========================================================
	db.commit() #save changes
	db.close()  #close database



# adds a new user
def add_user( username, password ):
    # create the database file and set the cursor
    db = sqlite3.connect("data/app.db")
    c = db.cursor()

    # insert into the users database
    command = "INSERT INTO users VALUES(\"%s\", \"%s\",\"\",\"\",\"\",\"\");" % ( username, password )

    c.execute(command)

    # save changes and close
    db.commit()
    db.close()


# gets the password for a given user
def get_pass( username ):
    # create the database file and set the cursor
    db = sqlite3.connect("data/app.db")
    c = db.cursor()

    # retrieves from the users database
    command = "SELECT password FROM users WHERE users.username = \"%s\";" % ( username )
    # command = "SELECT password FROM users"
    for row in c.execute(command):
        password = row[0]

    # save changes and close
    db.commit()
    db.close()

    return password


# returns a list of all registered users
def get_users():
    # create the database file and set the cursor
    db = sqlite3.connect("data/app.db")
    c = db.cursor()

    # get the list
    user_list = []
    command = "SELECT username FROM users;"
    for row in c.execute(command):
        user_list.append(row[0])

    # save changes and close
    db.commit()
    db.close()

    return user_list
    
#=====================================================================================================
if __name__ == "__main__":
    # remove the current database
    system("rm data/app.db")
    # make the new database
    make_database()

    add_user("ray", hashlib.sha224( "jones" ).hexdigest())
    add_user("jones", hashlib.sha224( "rayjones" ).hexdigest())
