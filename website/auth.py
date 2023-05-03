from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from .models import User
from . import db
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


#--------> For admin
@auth.route('/login', methods=['GET', 'POST'])
def login():
	users = User.query.all()
	if users:
		if request.method == 'POST':
			login = request.form.get('login')
			password = request.form.get('password')

			for item in users:
				if item.login == login:
					user = item
			if user:
				if check_password_hash(user.password, password):
					flash(f'Zalogowany jako {user.login}.', category='success')
					login_user(user, remember=True)
					return redirect(url_for('views.dashboard'))
				else:
					flash(f'Złe hasło dla {user.login}.', category='error')
	else:
		flash(f'Nie ma jeszcze usera', category='error')
		return redirect(url_for('views.home'))

	return render_template('login.html', users=users, user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('views.home'))


@auth.route('/addadmin', methods=['GET','POST'])
def addadmin():
	login = 'admin'
	password = generate_password_hash('admin', method='sha256')
	user = User(login=login, password=password)
	db.session.add(user)
	db.session.commit()
	flash(f'dodano {login} z haslem {password} do bazy')
	return redirect(url_for('auth.login'))