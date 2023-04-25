import re 
from flask import flash, request
from website.models import Blacklist
import datetime

def email_is_valid(email):
	pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if re.fullmatch(pattern, email):
		return True
	else:
		return False


def check_vals(dic, id_template):
	if id_template == 1:
	    if not email_is_valid(dic['email']):
	        flash('Podaj poprawny adres email.', category='error')
	        return False
	    elif len(dic['name']) < 5:
	        flash('Imię i nazwisko: wprowadzone dane są za krótkie.', category='error')
	        return False
	    else:
	        return True
	else:
		flash('To nie to id', category='error')
		return False

def check_year(name, event_num):
	if len(name) < 3:
		flash('Nazwa roku jest za krótka - min. 3 znaki', category='error')
		return False
	elif len(event_num) == 0 or int(event_num) < 1:
		flash('Liczba akcji jest za mała - min. 1 akcja', category='error')
		return False
	else:
		return True


class Backup():
	pass


def check_event(name, date, template, mail_temp, num):
	if len(name) < 3:
		backup = Backup()
		flash(f'Nazwa akcji nr {num} jest za krótka - min. 3 znaki', category='error')
		return (False, backup) 
	if date == None or date < datetime.date.today():
		backup = Backup()
		backup.name = name
		flash(f'Wprowadź poprawną datę dla akcji nr {num}', category='error')
		return (False, backup)
	if template == "Wybierz opcję":
		backup = Backup()
		backup.name = name
		backup.date = date
		flash(f'Wybierz szablon dla akcji nr {num}', category='error')
		return (False, backup)
	if len(mail_temp) < 10:
		backup = Backup()
		backup.name = name
		backup.date = date
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
		flash(f'Mail dla akcji nr {num} jest za krótki - min. 10 znaków', category='error')
		return (False, backup)
	
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
