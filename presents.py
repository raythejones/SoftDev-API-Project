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


my_app = Flask (__name__)
my_app.secret_key = os.urandom(100)


f = "presents.db"
db = sqlite3.connect(f, check_same_thread=False)  #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

my_data = [];
my_username = "";
friends = [];
requests = {}; #dictionary in the form (username: name, age, gender, hobbies)

#==========================================================

#helper methods for login, logout, and create_user

def login(username, password):
    user = db_tool.get_user_by_username(username)
    if user:
        if check_password(user['id'], password):
            session['user_id'] = user['id']
            my_username = user['id']
            return 0
        return 1
    return 2

def logged_in():
    try:
        return session['user_id'] is not None
    except KeyError:
        return False

def logout():
    if logged_in():
        session.pop('user_id')

def check_password(user_id, password_to_check):
    return db_tool.get_password(user_id) == hashlib.sha224(password_to_check).hexdigest()

def set_password(user_id, new_password):
    db_tool.set_password(user_id, hashlib.sha224(new_password).hexdigest())

def create(username, password1, password2):
    if not username in db_tool.get_users():
        if password1 == password2:
            user_id = db_tool.add_user(username)
            set_password(user_id, password1)
            login(username, password1)
            return 0
        return 1
    return 2
     
@my_app.route('/', methods=['POST', 'GET'])
def login():
    if logged_in():
        flash('User is already logged in.')
        return redirect(url_for('profile'))
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
    
@my_app.route('/index')
def home():
    return render_template('index.html', user = my_username, fr = requests)
    
@my_app.route('/edit')
def edit():
    my_data = c.execute("SELECT user FROM users WHERE user = %s"%(my_username))
    return render_template('edit.html', data = my_data, fr = requests)
    
@my_app.route('/friends')
def friends():
    return render_template('findfriends.html', user = my_username, fr = requests)
    
@my_app.route('/profile')
def profile():
    return render_template('profile.html', user = my_username, fr = requests)
    
@my_app.route('/add', methods =['GET','POST'])
def add():
    if request.args.get('search') == 'Submit':
        items =searchWalmart(requests.args.get('lookup'))
        return render_template('addwish.html', stuff = items, user = my_username, fr = requests)
    else:
        flash('Please search something')
        return render_template('addwish.html', user = my_username, fr = requests)
    
@my_app.route('/product')
def product():
    return render_template('product.html', user = my_username, fr = requests)
    
if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
    
#==========================================================
db.commit() #save changes
db.close()  #close database
