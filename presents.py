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
import auth
from auth import logged_in

my_app = Flask (__name__)
my_app.secret_key = os.urandom(100)


f = "presents.db"
db = sqlite3.connect(f, check_same_thread=False)  #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

my_data = []; #array in the form [user, pass, name, age, gender, hobbies]
my_username = "";
friends = {}; #dictionary in the form (username: [name, age, gender, hobbies, [wishes]])
requests = {}; #dictionary in the form (username: [name, age, gender, hobbies])

#==========================================================

#helper methods for login, logout, and create_user

def initialize_fnfr():
    people = c.execute("SELECT friend FROM friends WHERE user = %s"%(my_username))
    for each in people:
        friend_data = c.execute("SELECT name,age,gender,hobbies FROM users WHERE user = %s"%(each[0]))
        friend_wishes = []
        temp = c.execute("SELECT id FROM products WHERE user = %s"%(each[0]))
        for wish in temp:
            friend_wishes.append(wish[0])
        friend_data.append(friend_wishes)
        friends[each[0]] = friend_data
    
    reqs = c.execute("SELECT request FROM requests WHERE user = %s"%(my_username))
    for each in reqs:
        req_data = c.execute("SELECT name,age,gender,hobbies FROM users WHERE user = %s"%(each[0]))
        requests[each[0]] = req_data
    
      
@my_app.route('/')
def index():
#    initialize_fnfr()
	if logged_in():
		return render_template('index.html', data=my_data, fr=requests, frands=friends)
	else:
		return redirect(url_for('login'))	
    	
@my_app.route('/login', methods=['POST', 'GET'])
def login():
    if logged_in():
        flash('User is already logged in.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        result = auth.login(request.form['username'], request.form['password'])
        if result == 0:
            flash('You have logged in!')
            return redirect(url_for('profile'))
        elif result == 1:
            flash('Incorrect password.')
            return redirect(url_for('login'))
        elif result == 2:
            flash('This username doesn\'t exist.')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title = 'Login')

@my_app.route('/logout')
def logout():
    if logged_in():
        auth.logout()
        flash('User been logged out.')
        return redirect(url_for('index'))
    flash('You are not logged in!')
    return redirect(url_for('login'))

@my_app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if logged_in():
        flash('You are already logged in!')
        return redirect(url_for('profile'))
    if request.method == 'POST':
        result = auth.create(request.form['username'],
                             request.form['password1'],
                             request.form['password2'])
        if result == 0:
            name = request.form['name']
            my_username = request.form['username']
            pw = request.form['password1']
            flash('Account Created')
            c.execute("INSERT INTO users VALUES (\"%s\", \"%s\", \"%s\", \"\", \"\", \"\");"%(my_username, pw, name))
            return redirect(url_for('edit'))
        elif result == 1:
            flash('Passwords do not match.')
            return redirect(url_for('create_user'))
        elif result == 2:
            flash('Username already exists.')
            return redirect(url_for('create_user'))
    else:
        return render_template('create_user.html', title = 'Create')


@my_app.route('/edit')
def edit():
#    initialize_fnfr()
    if request.method == 'POST':
        if request.form['password']==request.form['confirm']:
            name = request.form['name']
            my_username = request.form['username']
            pw = request.form['password']
            age = request.form['age']
            gender = request.form['gender']
            hobbies = request.form['hobbies']
            c.execute("INSERT INTO users VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"%(my_username, pw, name, age, gender, hobbies))
            return redirect(url_for('edit'))
        else:
            flash('Passwords do not match.')
            return redirect(url_for('edit'))
    else:
        my_data = c.execute("SELECT user FROM users WHERE user = %s"%(my_username))
        return render_template('edit.html', data=my_data, fr=requests)
    
@my_app.route('/friends')
def friends():
 #   initialize_fnfr()
    return render_template('findfriends.html', data=my_data, fr=requests)
    
@my_app.route('/profile')
def profile():
 #   initialize_fnfr()
    if request.method == "POST":
        person = request.form['person']
    else:
        return render_template('profile.html', data=my_data, fr=requests)
    
@my_app.route('/add', methods =['GET','POST'])
def add():
 #   initialize_fnfr()
    if request.args.get('search') == 'Submit':
        items =searchWalmart(requests.args.get('lookup'))
        return render_template('addwish.html', stuff=items, data=my_data, fr=requests)
    else:
        flash('Please search something')
        return render_template('addwish.html', data=my_data, fr=requests)
    
@my_app.route('/product')
def product():
 #   initialize_fnfr()
    return render_template('product.html', data=my_data, fr=requests)
    
if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
    
#==========================================================
db.commit() #save changes
db.close()  #close database
