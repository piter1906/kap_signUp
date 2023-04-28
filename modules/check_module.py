import re 
from flask import flash, request, session
from website.models import Blacklist, Events
from website import db
import datetime

class Backup():
	pass


def check_date():
    events = Events.query.all()
    if events:
	    for event in events:
	        if event.date < datetime.date.today():
	            event.is_active = False
	            db.session.commit()


def email_is_valid(email):
	pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if re.fullmatch(pattern, email):
		return True
	else:
		return False


def check_member(telNum, email):
	blacklist = Blacklist.query.all()
	for item in blacklist:
		if item.email == email or item.number == int(telNum):
			return False
		else:
			return True


def check_vals(num, **kwargs):
	if 'name' in kwargs.keys():
		if len(kwargs['name']) < 5:
		    flash(f'Imię i nazwisko {num}: wprowadzone dane są za krótkie.', category='error')
		    return False
	if 'email' in kwargs.keys():
		if not email_is_valid(kwargs['email']):
			flash(f'Podaj poprawny adres email dla zapisu {num}.', category='error')
			return False
	if 'adress' in kwargs.keys():
		if len(kwargs['adress']) < 3:
			flash(f'Podaj poprawny adres dla zapisu {num}.', category='error')
			return False
	if 'year' in kwargs.keys():
		if len(kwargs['year']) != 4 or int(kwargs['year']) < 1970 or int(kwargs['year']) > 2012:
			flash(f'Podaj poprawny rok urodzenia (1970 - 2012) dla zapisu {num}.', category='error')
			return False
	if 'telNum' in kwargs.keys():
		if len(kwargs['telNum']) != 9:
			flash(f'Podaj poprawny numer telefonu dla zapisu {num}.', category='error')
			return False
	return True


def check_year(name, event_num):
	if len(name) < 3:
		flash('Nazwa roku jest za krótka - min. 3 znaki', category='error')
		return False
	elif len(event_num) == 0 or int(event_num) < 1:
		flash('Liczba akcji jest za mała - min. 1 akcja', category='error')
		return False
	else:
		return True


def backup_set(backup, name, date, template, mail_temp):
	if name:
		backup.name = name
	if date:
		backup.date = date
	if mail_temp:
		backup.mail_temp = mail_temp
	if template:
		if template == 'Szablon 1':
			backup.temp_id = 1
		if template == 'Szablon 2':
			backup.temp_id = 2
		if template == 'Szablon 3':
			backup.temp_id = 3
		if template == 'Szablon 4':
			backup.temp_id = 4
		if template == 'Szablon 5':
			backup.temp_id = 5
		if template == 'Szablon 6':
			backup.temp_id = 6
	return backup


def check_event(name, date, template, mail_temp, num):
	backup = Backup()
	bcup = backup_set(backup, name, date, template, mail_temp)
	if len(name) < 3:
		flash(f'Nazwa akcji nr {num} jest za krótka - min. 3 znaki', category='error')
		return (False, bcup) 
	if date == None or date < datetime.date.today():
		flash(f'Wprowadź poprawną datę dla akcji nr {num}', category='error')
		return (False, bcup)
	if template == "Wybierz opcję":
		flash(f'Wybierz szablon dla akcji nr {num}', category='error')
		return (False, bcup)
	if len(mail_temp) < 10:
		flash(f'Mail dla akcji nr {num} jest za krótki - min. 10 znaków', category='error')
		return (False, bcup)
	
	return (True, None)


def check_bl(email, number):
    if len(email) == 0 or not email_is_valid(email):
        flash('Najpierw wprowadź poprawny adres email', category='error')
        return False
    elif len(str(number)) != 9:
        flash('Najpierw wprowadź poprawny numer telefonu', category='error')
        return False
    else:
        items = Blacklist.query.all()
        for item in items:
            if str(item.number) == number:
                flash(f'Podany numer telefonu już jest w bazie pod numerem {item.id}.', category='error')
                return False
            elif item.email == email:
                flash(f'Podany email już jest w bazie pod numerem {item.id}.', category='error')
                return False
    return True
