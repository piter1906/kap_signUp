import re 
from flask import flash, request, session
from website.models import Blacklist, Events
from website import db
import datetime
import logging

logger = logging.getLogger('check_logger')

class Backup():
	pass


def check_date():
    events = Events.query.all()
    if events:
	    for event in events:
	        if event.date and event.date < datetime.date.today():
	            event.is_active = False
	            db.session.commit()
	            logger.info(f'Zmieniono status wydarzenia {event} z powodu przestarzalej daty')


def email_is_valid(email):
	pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if re.fullmatch(pattern, email):
		return True
	else:
		return False


def check_member(telNum, email):
	blacklist = Blacklist.query.all()
	if blacklist:
		for item in blacklist:
			if item.email:
				if item.email == email:
					flash(f'Przepraszamy ale nie możesz zapisać się na to wydarzenie', category='error')
					logger.info(f'BL: Proba zapisu usera z czarnej listy, email: {item.email}')
					return False
			if item.number:
				if item.number == int(telNum):
					flash(f'Przepraszamy ale nie możesz zapisać się na to wydarzenie', category='error')
					logger.info(f'BL: Proba zapisu usera z czarnej listy, telefon: {item.number}')
					return False
	return True


def check_vals(event, num='', **kwargs):
	if f'name{num}' in kwargs.keys():
		if len(kwargs[f'name{num}']) < 5:
		    flash(f'Imię i nazwisko {num}: wprowadzone dane są za krótkie.', category='error')
		    logger.info(f'SIGNUP: name error for {event}; wpisano: ' + str(kwargs[f'name{num}']))
		    return False
	if f'email{num}' in kwargs.keys():
		if not email_is_valid(kwargs[f'email{num}']):
			flash(f'Podaj poprawny adres email dla zapisu {num}.', category='error')
			logger.info(f'SIGNUP: email error for {event}; wpisano: ' + str(kwargs[f'email{num}']))
			return False
		for sn in event.signup:
			for ps in sn.person:
				if ps.email == kwargs[f'email{num}']:
					flash(f'Podany mail dla zapisu {num} już jest w bazie uczestników tej akcji. Wprowadź inny mail.', category='error')
					logger.info(f'SIGNUP: email error for {event} - juz jest w bazie; wpisano: ' + str(kwargs[f'email{num}']))
					return False
	if f'adress{num}' in kwargs.keys():
		if len(kwargs[f'adress{num}']) < 3:
			flash(f'Podaj poprawny adres dla zapisu {num}.', category='error')
			logger.info(f'SIGNUP: adress error for {event}; wpisano: ' + str(kwargs[f'adress{num}']))
			return False
	if f'year{num}' in kwargs.keys():
		if event.temp_id != 6 or event.temp_id != 3 and num != '':
			if len(kwargs[f'year{num}']) != 4 or int(kwargs[f'year{num}']) < 1970 or int(kwargs[f'year{num}']) > 2012:
				flash(f'Podaj poprawny rok urodzenia (1970 - 2012) dla zapisu {num}.', category='error')
				logger.info(f'SIGNUP: year error for {event}; wpisano: ' + str(kwargs[f'year{num}']))
				return False
		else:
			if len(kwargs['year']) != 4 or datetime.date.today().year - int(kwargs[f'year{num}']) > 80 \
				 or datetime.date.today().year - int(kwargs[f'year{num}']) < 18:
				flash('Podaj poprawny rok urodzenia - musisz mieć minium 18 lat', category='error')
				logger.info(f'SIGNUP: year error for {event} (min. 18 lat); wpisano: ' + str(kwargs[f'year{num}']))
				return False
	if f'telNum{num}' in kwargs.keys():
		if len(kwargs[f'telNum{num}']) != 9:
			flash(f'Podaj poprawny numer telefonu dla zapisu {num}.', category='error')
			logger.info(f'SIGNUP: telefon error for {event}; wpisano: ' + str(kwargs[f'telNum{num}']))
			return False
		for sn in event.signup:
			for ps in sn.person:
				if ps.telNum == int(kwargs[f'telNum{num}']):
					flash(f'Podany telefon dla zapisu {num} już jest w bazie uczestników tej akcji. Wprowadź inny numer.', category='error')
					logger.info(f'SIGNUP: telefon error for {event} - juz jest w bazie; wpisano: ' + str(kwargs[f'telNum{num}']))
					return False
	if 'isLent' in kwargs.keys():
		if kwargs['isLent'] == 'true':
			if not kwargs['skiLent']:
				flash(f'Zaznacz co zamierzasz wyporzyczyć.', category='error')
				logger.info(f'SIGNUP: for {event} nie zaznaczono sprzetu do wyporzyczenia')
				return False
	if 'height' in kwargs.keys():
		if kwargs['isLent'] == 'true':
			if len(kwargs['height']) < 3:
				flash(f'Podaj poprawny wzrost w cm.', category='error')
				logger.info(f'SIGNUP: for {event} zly wzrost: '+ str(kwargs['height']))
				return False
	if 'weight' in kwargs.keys():
		if kwargs['isLent'] == 'true':
			if len(kwargs['weight']) < 2:
				flash(f'Podaj poprawną wagę w kg.', category='error')
				logger.info(f'SIGNUP: for {event} zla waga: '+ str(kwargs['weight']))
				return False
	if 'teamNum' in kwargs.keys():
		if int(kwargs['teamNum']) < 4:
		    flash(f'Podaj poprawną liczbę zawodników, min. 4', category='error')
		    logger.info(f'SIGNUP: for {event} zla liczba zawodnikow: '+ str(kwargs['teamNum']))
		    return False
	if 'sonNum' in kwargs.keys():
		if int(kwargs['sonNum']) < 0:
		    flash(f'Liczba synów / uczestników po opieką nie może być mniejsza od 0', category='error')
		    logger.info(f'SIGNUP: for {event} zla liczba synow / uczestnikow: '+ str(kwargs['sonNum']))
		    return False
	return True


def check_year(name, event_num):
	if len(name) < 3:
		flash('Nazwa roku jest za krótka - min. 3 znaki', category='error')
		logger.info(f'YEAR: za krotka nazwa roku: {name}')
		return False
	elif len(event_num) == 0 or int(event_num) < 1:
		flash('Liczba akcji jest za mała - min. 1 akcja', category='error')
		logger.info(f'YEAR: za mala liczba akcji: {event_num}')
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
	if template != 'Wybierz opcję' and template != 'test':
		backup.temp_id = int(template[8])
	return backup


def check_event(name, date, template, mail_temp, num):
	backup = Backup()
	bcup = backup_set(backup, name, date, template, mail_temp)
	if len(name) < 3:
		flash(f'Nazwa akcji nr {num} jest za krótka - min. 3 znaki', category='error')
		logger.info(f'EVENT_ADD: error: za krotka nazwa: {name}')
		return (False, bcup) 
	if date and date < datetime.date.today():
		flash(f'Wprowadź poprawną datę dla akcji nr {num}', category='error')
		logger.info(f'EVENT_ADD: error: bledna data: {date}')
		return (False, bcup)
	if not date and template != "Szablon 5":
		flash(f'Dla akcji bez daty można wybrać tylko szablon 5', category='error')
		logger.info(f'EVENT_ADD: error: zly szablon dla akcji bez daty: {template}')
		return (False, bcup)
	if template == "Wybierz opcję":
		flash(f'Wybierz szablon dla akcji nr {num}', category='error')
		logger.info(f'EVENT_ADD: error: nie wybrano szablonu')
		return (False, bcup)
	if len(mail_temp) < 10:
		flash(f'Mail dla akcji nr {num} jest za krótki - min. 10 znaków', category='error')
		logger.info(f'EVENT_ADD: error: za krotki mail: {mail_temp}')
		return (False, bcup)
	
	return (True, None)


def check_bl(email, number):
	items = Blacklist.query.all()
	if email:
		if not email_is_valid(email):
			flash('Najpierw wprowadź poprawny adres email', category='error')
			logger.info(f'BL: Wprowadzono niepoprawny email: {email}')
			return False
		if items:
			for item in items:
				if item.email == email:
					flash(f'Podany email już jest w bazie pod numerem {item.id}.', category='error')
					logger.info(f'BL: Proba duplikatu: {email}')
					return False
	if number:
		if len(str(number)) != 9:
			flash('Najpierw wprowadź poprawny numer telefonu', category='error')
			logger.info(f'BL: Wprowadzono niepoprawny telefon: {number}')
			return False
		if items:
			for item in items:
				if str(item.number) == number:
					flash(f'Podany numer telefonu już jest w bazie pod numerem {item.id}.', category='error')
					logger.info(f'BL: Proba duplikatu: {number}')
					return False
	if not email and not number:
		flash('Wprowadź najpierw email i / lub numer.', category='error')
		logger.info(f'BL: Proba zapisu bez danych')
		return False
	return True
