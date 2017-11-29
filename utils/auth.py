from flask import session
import hashlib
from db import get_pass, add_user, get_users


# attempts to login the user
# returns 0 on successful login, 1 on failed password, 2 on unrecognized username
def login( username, password ):
    if username in get_users():
        if check_pass( username, password ):
            session['user'] = username
            return 0
        return 1
    return 2

# helper method: checks a password against the database
def check_pass( username, password ):
    return get_pass( username ) == hashlib.sha224( password ).hexdigest()


# returns true if the user is logged in, false otherwise
def is_logged_in():
    return 'user' in session


# logs the user out of the given session
def logout():
    if is_logged_in():
        session.pop('user')


# creates an account for the user, checking that the username is available
# returns 0 for a successful creation and 1 for the username already existing
def create_account(username, password1, password2):
    if not username in get_users():
        if password1 == password2:
           add_user( username, hashlib.sha224(password1).hexdigest())
           return 0
        return 1
    return 2
