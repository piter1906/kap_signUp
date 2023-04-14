from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)


#--------> For admin
@auth.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')