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


#==========================================================

@my_app.route('/')
def root():
    
@my_app.route('/home')
def home():
    
@my_app.route('/edit')
def edit():
    
@my_app.route('/friends')
def friends():
    
@my_app.route('/profile')
def profile():
    
@my_app.route('/add')
def add():
    
@my_app.route('/product')
def product():
    
#logout: removes session and redirects to root route
@my_app.route('/logout', methods=["POST", "GET"])
def logout():
    if "user" in session:
        session.pop("user")
    return redirect( url_for("root") )
    
if __name__ == '__main__':
    my_app.debug = True
    my_app.run()
    
#==========================================================
db.commit() #save changes
db.close()  #close database