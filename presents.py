'''
PPAPi
SoftDev Pd9
Project 1 Chritmas Shopping
11.16.17
'''

from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3, hashlib
import os
#from utils import db
import utils.db as db
import utils.auth as auth
import utils.api as api



my_app = Flask (__name__)
my_app.secret_key = os.urandom(100)


f = "data/app.db"
db = sqlite3.connect(f, check_same_thread=False)  #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

my_data = []; #array in the form [user, pass, name, age, gender, hobbies]
friends = {}; #dictionary in the form (username: [name, age, gender, hobbies, [wishes]])
requests = {}; #dictionary in the form (username: [name, age, gender, hobbies])
strangers = {}; #dictionary in the form (username: [name, age, gender, hobbies])

#==========================================================

#helper methods for login, logout,

def print_list(l):
    ans = ""
    for each in l:
        ans += str(each)
        ans += ", "
    print ans
    
    
def initialize_fnfr():
    go1 = 0
    for each in c.execute("SELECT username FROM friends"):
        if each[0] == session['username']:
            go1 = 1
    if go1 == 1:
        people = c.execute("SELECT friend FROM friends WHERE username == \"%s\";" % (session['username']))
        temp_list = []
        friend_data = []
        friend_wishes = []
        for each in people:
            temp_list.append(each[0])
        for each in temp_list:
            friend_data = c.execute("SELECT name,age,gender,hobbies FROM users WHERE username = \"%s\";"%(each))
            print_list(friend_data)
        for each in temp_list:
            temp = c.execute("SELECT name FROM products WHERE username == \"%s\";"%(each))
            print_list(temp)
            for wish in temp:
                print each + ": " + wish[0]
                #friend_wishes.append(wish[0])
            #friend_data.append(friend_wishes)
            #friends[each[0]] = friend_data

    go2 = 0
    for each in c.execute("SELECT username FROM requests;"):
        if each[0] == session['username']:
            go2 = 1
    if go2 == 1:
        reqs = c.execute("SELECT request FROM requests WHERE username == \"%s\";"%(session['username']))
        for each in reqs:
            req_data = c.execute("SELECT name,age,gender,hobbies FROM users WHERE username = \"%s\";"%(each[0]))
            requests[each[0]] = req_data

	#this is the same thing except we're making a dictionary for non-friends now
	stranger = c.execute("SELECT user FROM users WHERE username != \"%s\";"%(session['username']))
	for each in stranger:
		#we add every user who is not the actual user in session
		strange_data = c.execute("SELECT name,age,gender,hobbies FROM users WHERE username = \"%s\";"%(each[0]))
		strangers[each[0]] = strange_data
		#we remove usernames of friends
		for each2 in friends: 
			if each == each2:
				strangers.pop(each)
		#we remove usernames of strangers who we have friend requested
		for each3 in requests:
			if each == each3:
				strangers.pop(each)
    
      
@my_app.route('/')
def index():
	if 'username' in session:
	    return render_template('index.html', data=my_data, fr=requests, frands=friends)
	else:
       	    return redirect(url_for('login'))

            
@my_app.route('/login', methods = ['POST', 'GET'] )
def login():
    # checks for post method to respond to submit button
    if request.method == 'POST':
        # LOGIN
        if request.form['type'] == 'Login':
        # uses the database method to check the login
            log_res = auth.login( request.form['usr'], request.form['pwd'] )
            # successful login
            if log_res == 0:
                session['username']= request.form['usr']
                #name = request.form['name']
                pw = request.form['pwd']
                flash("You have logged in successfully!")
                #c.execute("INSERT INTO users VALUES (\"%s\", \"%s\", \"%s\", \"\", \"\", \"\");"%(session['username'], pw, session['username']))
                initialize_fnfr()
                return redirect( url_for('index') )
            # bad password
            if log_res == 1:
                flash("Incorrect password")
                return redirect( url_for('login') )
            # unknown username
            if log_res == 2:
                flash("Unknown username")
                return redirect( url_for('login') )

        # CREATE ACCOUNT
        if request.form['type'] == 'Signup':
            cr_acc_res = auth.create_account( request.form['usr'], request.form['pwd'], request.form['pwd2'] )
            # if successful
            if cr_acc_res == 0:
                flash("Account created")
                return redirect( url_for('edit') )
            # if username already exists
            if cr_acc_res == 1:
                flash("That username already exists")
                return redirect( url_for('login') )
		# match passwords
            if cr_acc_res == 2:
                flash("Passwords don't match")
                return redirect( url_for('login') )

    # just render normally if no post
    else:
        return render_template("login.html")


@my_app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username');
    flash("You have been logged out")
    friends = {}
    requests = {}
    my_username = ""
    my_data = []
    return redirect( url_for("index"))


@my_app.route('/edit', methods = ['POST', 'GET'] )
def edit():
    if 'username' in session:
        if request.method == 'POST':
            if request.form['password']==request.form['confirm']:
                if request.form['password']!="":
                    pw_unhashed = request.form['password']
                    pw = hashlib.sha224( pw_unhashed ).hexdigest()
                    age = request.form['age']
                    gender = request.form['gender']
                    hobbies = request.form['hobbies']
                    c.execute("UPDATE users SET password = \"%s\", name = \"%s\", age = \"%d\", gender = \"%s\" hobbies = \"%s\" WHERE username = \"%s\";"%(pw, name, age, gender, hobbies, session["username"]))
                else:
                    age = request.form['age']
                    gender = request.form['gender']
                    hobbies = request.form['hobbies']
                    c.execute("UPDATE users SET age = %s, gender = \"%s\", hobbies = \"%s\" WHERE username = \"%s\";"%(age, gender, hobbies, session["username"]))
                for me in c.execute("SELECT * FROM users WHERE username = \"%s\";"%(session["username"])):
                    my_data = me
                return redirect(url_for('edit'))
            else:
                flash('Passwords do not match.')
                return redirect(url_for('edit'))
        else:
            for me in c.execute("SELECT * FROM users WHERE username = \"%s\";"%(session["username"])):
                my_data = me
            return render_template('edit.html', data=my_data, fr=requests)
    else:
        return redirect(url_for('index'))
    
@my_app.route('/friends')
def friends():
    if 'username' in session:
	    if request.method == "POST":
	    	#if statement for when user presses "accept" or "request" button on friends page
	    	if request.form['person']:
	    		person = request.form['person']
	    		#requests and friends datatables get updated
	    		if person in strangers:
	    			c.execute("INSERT INTO requests VALUES(\"%s\", \"%s\");"%(person, my_username))
	    		elif person in friends:
	    			c.execute("INSERT INTO friends VALUES(\"%s\", \"%s\");"%(my_username, person))
	    			c.execute("INSERT INTO friends VALUES(\"%s\", \"%s\");"%(person, my_username))
	    		return render_template('findfriends.html', data=my_data, fr=requests, stranger=strangers)
		#if statement for when user presses "search" button on friends page
	    	if request.form['name']:
	    		searched = {}
	    		for each in strangers:
	    			if name in each or name in each[0]:
	    				searched_data = c.execute("SELECT name,age,gender,hobbies FROM users WHERE user %s"%(each))
	    				searched[each[0]] = searched_data
	    		return render_template('findfriends.html', data=my_data, fr=requests, stranger=searched)
	    #when friends page is accessed from index
            else:
           	    return render_template('findfriends.html', data=my_data, fr=requests, stranger=strangers)
    else:
        return redirect(url_for('index'))
    
@my_app.route('/profile')
def profile():
    if 'username' in session:
        if request.method == "POST":
	    person = request.form['person']
	    #new_data is the personal information of whoever you're looking at (that isn't you)
	    new_data = []
	    new_data = c.execute("SELECT user FROM users WHERE user = %s"%(person))
	    #making a products dictionary to use in the html
	    products = []
	    for each in reqs:
		product_data = c.execute("SELECT name,id FROM users WHERE user = %s"%(person))
		products[each[0]] = product_data
	    return render_template('profile.html', data=new_data, fr=requests, product=products)
        else:
       	    #making a products dictionary to use in the html
       	    products = []
       	    for each in reqs:
		product_data = c.execute("SELECT name,id FROM users WHERE user = %s"%(my_username))
		products[each[0]] = product_data
	    return render_template('profile.html', data=my_data, fr=requests, product=products)
    else:
        return redirect(url_for('index'))
    
@my_app.route('/add', methods =['GET','POST'])
def add():
    if 'username' in session:
        if request.args.get('search') == 'Submit':
            lookup = request.args.get('lookup')
            items =api.searchWalmart(lookup)
            return render_template('addwish.html', stuff=items,query=lookup, data=my_data, fr=requests)
        else:
            flash('Please search something')
            return render_template('addwish.html', data=my_data, fr=requests)
    else:
        return redirect(url_for('index'))
   
    
@my_app.route('/product', methods=['GET','POST'])
def product():
    if 'username' in session:
        if request.method == 'GET':
            name=request.args.get('name')
            info={}
            info=api.searchWalmart(name)[0]
            info=api.productInfo(info)
            vids=api.searchYoutube(name)
            return render_template('product.html',productName=info['name'], desc=info['desc'], link=info['link'], image=info['image'], vids=vids, data=my_data, fr=requests)
    else:
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
    
#==========================================================
db.commit() #save changes
db.close()  #close database
