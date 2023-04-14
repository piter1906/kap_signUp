from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

#--------> For admin
@auth.route('/login')
def login():
    return render_template('login.html')