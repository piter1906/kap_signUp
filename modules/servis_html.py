from flask import flash, request, redirect, url_for
from flask_login import login_required, current_user
from website import db
from modules.check_module import *
from website.models import Year, Blacklist, Events, Signup, Person, Turnament, Winter, Older, Basic
import datetime 

def date_from_str(date):
    if len(date) == 10:
        year = int(date[:4])
        month = int(date[5:7]) if date[5] == '1' else int(date[6])
        day = int(date[8:]) if int(date[8]) != 0 else int(date[9])
        return datetime.date(year=year, month=month, day=day)

def get_form_val(lst):
	dic = {}
	if lst:
		for val in lst:
			dic[val] = request.form.get(val)
	return dic

def db_add_new_sigup(dic, event):
	if event.temp_id == 1:
		signup = Signup(event_id=event.id)
		db.session.add(signup)
		db.session.commit()
		person = Person(signup_id=signup.id, name=dic['name'], email=dic['email'], 
				adress=dic['adress'], year=dic['year'], telNum=dic['telNum'], selectSize=dic['selectSize'])
		db.session.add(person)
		db.session.commit()
		basic = Basic(signup_id=signup.id, howMany=dic['howMany'], whereKnew=dic['whereKnew'], intro=dic['intro'])
		db.session.add(basic)
		db.session.commit()
		flash('Udało się zapisać!', category='success')
	else:
		flash(f'To nie to id{event.id}', category='error')

def db_add_new_blacklist(email, number):
    new_item = Blacklist(email=email, number=number)
    db.session.add(new_item)
    db.session.commit()
    flash('Dodano do czarnej listy', category='success')

def db_add_year(name, event_num, years):
	if not years:
		new_year = Year(name=name, event_num=event_num)
		db.session.add(new_year)
		db.session.commit()
	else:
		for item in years:
			item.is_active = False
		db.session.commit()
		new_year = Year(name=name, event_num=event_num)
		db.session.add(new_year)
		db.session.commit()

def db_update_event(event):
	dic = {}
	name = request.form.get('name')
	date = date_from_str(request.form.get('date'))
	mail_temp = request.form.get('mail_temp')
	tup = check_event(name=name, date=date, template="test", mail_temp=mail_temp, num=event.id)
	if tup[0]:
		event.name = name
		event.date = date
		event.mail_temp = mail_temp
		db.session.commit()
		flash(f'Zaktualizowano {event.name}', category='success')
		return True
	else:
		return False

def db_new_event(year):
	check = True
	name = request.form.get('name')
	date = date_from_str(request.form.get('date'))
	template = request.form.get('template')
	mail_temp = request.form.get('mail_temp')
	tup = check_event(name=name, date=date, template=template, mail_temp=mail_temp, num='nowa')
	if tup[0]:
		if template == 'Szablon 1':
			temp_id = 1
			event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
		elif template == 'Szablon 2':
			temp_id = 2
			event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
		elif template == 'Szablon 3':
			temp_id = 3
			event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)

		elif template == 'Szablon 4':
			temp_id = 4
			event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)

		elif template == 'Szablon 5':
			temp_id = 5
			event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)

		elif template == 'Szablon 6':
			temp_id = 6
			event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)

		db.session.add(event)
		db.session.commit()
		flash(f'Dodano {event.name} do wydarzeń', category='success')
		backup = False
	else:
		backup = tup[1]
		check = False
	return (check, backup)

def db_add_event(year):
	dic = {}
	lst_event = []
	check = True
	for i in range(year.event_num):
		name = request.form.get(f'name{i+1}')
		template = request.form.get(f'template{i+1}')
		date = date_from_str(request.form.get(f'date{i+1}'))
		mail_temp = request.form.get(f'mail_temp{i+1}')
		tup = check_event(name, date, template, mail_temp, i+1)
		if tup[0]:
			if template == 'Szablon 1':
				temp_id = 1
				new_event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
				lst_event.append(new_event)
			elif template == 'Szablon 2':
				temp_id = 2
				new_event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
				lst_event.append(new_event)
			elif template == 'Szablon 3':
				temp_id = 3
				new_event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
				lst_event.append(new_event)
			elif template == 'Szablon 4':
				temp_id = 4
				new_event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
				lst_event.append(new_event)
			elif template == 'Szablon 5':
				temp_id = 5
				new_event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
				lst_event.append(new_event)
			elif template == 'Szablon 6':
				temp_id = 6
				new_event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
				lst_event.append(new_event)
			dic[i+1] = new_event
		else:
			dic[i+1] = tup[1]
			check = False 
	if check:
		for event in lst_event:
			db.session.add(event)
			db.session.commit()
		year.first_add = True
		db.session.commit()
		flash('Dodano akcje do wybranego roku', category='success')
	return (dic, check)



