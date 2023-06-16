from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for, abort
from .models import User
from . import db
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import logging


auth = Blueprint('auth', __name__)
logger = logging.getLogger('auth_logger')

#--------> For admin
@auth.route('/login', methods=['GET', 'POST'])
def login():
	users = User.query.all()
	user_ip = request.remote_addr
	if users:
		if request.method == 'POST':
			login = request.form.get('login')
			password = request.form.get('password')

			for item in users:
				if item.login == login:
					user = item
				else:
					user = None
			if user:
				if check_password_hash(user.password, password):
					login_user(user, remember=True)
					flash(f'Zalogowany jako {user.login}.', category='success')
					logger.info(f'Zalogowany {user.login} | IP: {user_ip}')
					return redirect(url_for('views.dashboard'))
				else:
					flash(f'Zle haslo dla {user.login}.', category='error')
					logger.info(f'Złe hasło dla {user.login} | IP: {user_ip}')
			else:
				flash(f'Nie ma tekiego loginu.', category='error')
				logger.info(f'Nie ma tekiego loginu: {login} | IP: {user_ip}')
	else:
		flash(f'Nie ma jeszcze usera', category='error')
		return redirect(url_for('views.home'))

	return render_template('login.html', users=users, user=current_user)

@auth.route('/logout')
@login_required
def logout():
	user_ip = request.remote_addr
	logout_user()
	logger.info(f'Wylogowany  | IP: {user_ip}')
	return redirect(url_for('views.home'))


@auth.route('/addadmin', methods=['GET','POST'])
def addadmin():
	login = 'kap_zapisy_admin'
	password = generate_password_hash('Kap_Zapisy_bH2L*Ya4NDy_Scf', method='sha256')
	user = User(login=login, password=password)
	db.session.add(user)
	db.session.commit()
	flash(f'dodano {login} z haslem {password} do bazy')
	return redirect(url_for('auth.login'))