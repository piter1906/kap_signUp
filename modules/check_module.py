import re 
from flask import flash, request
from website.models import Blacklist

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
	    elif len(dic['adress']) < 10:
	        flash('Adres: wprowadzone dane są za krótkie.', category='error')
	        return False
	    elif not dic['year'].isdigit() or len(dic['year']) > 4 or not int(dic['year']) > 1970 and int(dic['year']) < 2016:
	        flash('Podaj poprawny rok urodzenia.', category='error')
	        return False
	    elif not dic['telNum'].isdigit() or len(dic['telNum']) != 9:
	        flash('Podaj 9cio cyfrowy numer telefonu.', category='error')
	        return False
	    else:
	        return True
	else:
		flash('To nie to id', category='error')
		return False

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
